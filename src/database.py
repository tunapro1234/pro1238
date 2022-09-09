from res.globals import __version__ as _ver
from pathlib import Path
import datetime
import json
import pdb
import os

# şimdi 
# hmm
# folder olsun subject olsun
# folder subjectlerin birleşimi databasei oluştursun
# 
# databasei düzenleyeyim derken ağzına sıçtım
# biraz planlama yapmam lazım
# 
# Posix patha geçmeden önce birkaç deneme yapmam lazım
# yaptım oluyor
# okey posix patha geçiyoruz
#
# write ve read database fonksiyonları res/data ile çalışacak (klasör ismi pathe dahil)
# parent değişkeni eklenecek
#
# writeta eğer parent yoksa res/data parent varsa klasör ismi olmadan yapılabilir
# hmmm
# çok sağlıklı olmaz sanırım
#
# okey subjectin writeı klasör alıyor klasörün writeı klasör isimli alıyor
# bu biraz sinir bozucu bir davranış bunu değiştirelim
# ikisi de kendi ismini de alsın
#
# folderın read fonksyonu recursive ve altındaki her şeyi okuyor
# ama write fonksiyonu recursive değil



class Folder:
	def __init__(self, name: str, version: str, sub_elements: list, 
			comment: str = "", data: list = [], parent = None):

		self.parent = parent
		self.version = version
		self.name = name

		self.sub_elements = sub_elements
		self.comment = comment
		self.data = data


	def __dict__(self):
		return {
				"version": self.version,
				"name": self.name,
				"comment": self.comment,
				"sub_elements": [(element.name if type(element) == Folder 
									else element.name + ".json")
									for element in self.sub_elements],
				"data": [entry.__dict__() for entry in self.data] 
				}


	@classmethod
	def read(cls, path):
		path = Path(path) if type(path) == str else path

		with Path(path, "properties.json").open() as file:
			read = json.load(file)

		# sub_elementsı oku ve subject/folder objesine çevir
		read["sub_elements"] = [(Subject if element_name.endswith(".json") else \
			Folder).read(Path(path, element_name)) for element_name in read["sub_elements"]]
		# data listesini oku ve entry objesine çevir
		read["data"] = Entry.undict(read["data"])
		return Folder(**read)


	def write_self(self, path):
		path = Path(path) if type(path) == str else path
		if not path.exists(): os.mkdir(path)
		with Path(path, "properties.json").open("w+") as file:
			json.dump(self.__dict__(), file)


	def write(self, path):
		self.write_self(path)
		# classmethod olan folder read recursive okuyor ama recursive yazmıyor
		# o yüzden bu fonksiyona ihtiyacımız var ama read_all çok da gerekli değil
		for element in self.sub_elements:
			write_name = element.name
			if type(element) == Subject: 
				write_name += ".json"

			element.write(Path(path, write_name))


	def remove_element(self, element):
		self.sub_elements.remove(element)


	def list_all(self):
		return {
				"version": self.version,
				"name": self.name,
				"comment": self.comment,
				"sub_elements": [element.__dict__() for element in self.sub_elements],
				"data": [entry.__dict__() for entry in self.data] 
				}


	def list_subjects(self):
		return {self.name: [(element.list_subjects() if type(element) == Folder \
			else element.__dict__()) for element in self.sub_elements]}


	def list_sub_names(self):
		return [i.name for i in self.sub_elements]

	def list_sub_names_r(self):
		return [(element.list_names_r() if type(element) == Folder \
			else element.name) for element in self.sub_elements]

	def find_by_path(self, text):
		names = [i for i in text.split("/") if i != ""]

		nbase = self
		for name in names:
			# Subjectin find_by_name fonksiyonu yok,
			# eğer folder/subject/subject tarzı bir şey yapılmaya 
			# çalışılırsa hata veriyor
			nbase = nbase.find_by_name(name)
		return nbase

	def find_by_name(self, name):
		if name == ".": return self
		if name == "..": 
			return self.parent

		arr = [i for i in self.sub_elements if i.name == name]
		if len(arr) != 1:
			raise Exception("no such file or directory")
		return arr[0]

	def add_entry(*args, **kwargs):
		return add_entry(*args, **kwargs)



class Subject:
	def __init__(self, name: str, full_name: str, version: str, factor: float, 
			target: float = 0, comment: str = "", data: list = [], parent = None):

		self.parent = parent
		self.version = version
		self.full_name = full_name
		self.name = name

		self.comment = comment
		self.factor = factor
		self.target = target
		self.data = data


	def __dict__(self):
		return {
				"version": self.version,
				"name": self.name,
				"full_name": self.full_name, 
				"factor": self.factor,
				"target": self.target,
				"comment": self.comment,
				"data": [entry.__dict__() for entry in self.data] 
				}


	@classmethod
	def read(cls, path):
		path = Path(path) if type(path) == str else path
		
		with path.open() as file:
			read = json.load(file)
		# sub_elementsı oku ve subject/folder objesine çevir
		read["data"] = Entry.undict(read["data"])
	

		# Program içinde Folderın sub elements listesindeki objelerin 
		# tipini görebildiğimiz için sonunda .json gibi bir uzantı olmasına
		# ihtiyacımız yok. O yüzden json uzantısını kaldırıyorum.
		# Bunun bize ne gibi bir avantajı olur bilmiyorum ama 
		# en başta böyle yapmışım o yüzden değiştirmekle uğraşmayacağım
		#read["name"] = ".".join(read["name"].split(".")[:-1])
		# Şimdi şöyle bir ufak problem var, problemi bilmiyorum ama bu 
		# satırı kapatmam gerekiyor
		
		return Subject(**read)


	def write(self, path):
		path = Path(path) if type(path) == str else path

		with path.open("w+") as file:
			json.dump(self.__dict__(), file)
				

	def list_all(self):
		return self.__dict__()


	def add_entry(*args, **kwargs):
		return add_entry(*args, **kwargs)

	

class Entry:
	def __init__(self, date, subject_name, correct, wrong, comment: str = ""):
		# jsondan okurken gelen tarihler str biçiminde olduğundan onları çeviriyoruz
		self.date = datetime.datetime.strptime(date, date_format) if type(date) == str else date
		self.subject_name = subject_name
		self.correct = correct
		self.wrong = wrong
		self.comment = comment
	

	def __dict__(self):
		return {
				"date": self.get_str_date(),
				"subject_name": self.subject_name,
				"correct": self.correct,
				"wrong": self.wrong,
				"comment": self.comment
				}
		
	def get_str_date(self):
		return self.date.strftime(date_format)

	@classmethod
	# str list to entry list
	def undict(cls, str_list):
		return [Entry(**entry) for entry in str_list]


date_format = "%d/%m/%y %H:%M:%S.%f"

default_path = Path("res/data")
default_structure = \
		Folder("data", _ver, [
			Folder("tyt", _ver, [
				Subject("tr", "tyt turkce", _ver, 0),
				Subject("mat", "tyt matematik", _ver, 0),
				Folder("sos", _ver, [
					Subject("tarih", "tyt tarih", _ver, 0),
					Subject("cografya", "tyt cografya", _ver, 0),
					Subject("felsefe", "tyt felsefe", _ver, 0),
					Subject("din", "tyt din", _ver, 0)
					]),
				Folder("fen", _ver, [
					Subject("fizik", "tyt fizik", _ver, 0),
					Subject("kimya", "tyt kimya", _ver, 0),
					Subject("bio", "tyt biyoloji", _ver, 0)
					])
				]), 

			Folder("ayt", _ver, [
				Subject("mat", "ayt matematik", _ver, 0),
				Folder("fen", _ver, [
					Subject("fizik", "ayt fizik", _ver, 0),
					Subject("kimya", "ayt kimya", _ver, 0),
					Subject("bio", "ayt biyoloji", _ver, 0)
					])
				])
			])



def add_entry(self, *args, path = default_path, date = None, **kwargs):
	date = datetime.datetime.now() if date is None else date
	self.data.append(Entry(date=date, subject_name=self.name, *args, **kwargs))
# 	if not self.write(): return False
	return date


def find_entry(self, date):
	# Date objelerini direkt olarak jsona kaydedemediğimiz 
	# için jsona kaydederken stringe çeviriyoruz. Eğer date 
	# parametresi str olarak verilmişse date objesine dönüştür
	# Çünkü elimizdeki subject/folder ın içindeki datada 
	# string olarak kayıtlı değil, datetime objesi
	date = datetime.datetime.strptime(date, date_format) \
			if type(date) == str else date
	
	index = [i for i, e in enumerate(self.data) if e.date == date] 
	if len(index) == 1:
		return index[0]
	return False


def read_database(path = default_path):
	# Eğer database okumada sıkıntı 
	# çıktıysa sıkıntıyı yukarıya ilet
	database = Folder.read(path)

	# Database okunduysa database 
	# oluşturmak için gerekli işlemleri yap
	meet_your_parents(database)
	return database


def write_database(main_folder: Folder = default_structure, path = default_path):
	# eğer database oluşturulmaya çalışılan klasör 
	# yoksa oluştur varsa problem yaratma
	os.makedirs(path, exist_ok=True)
	return main_folder.write(path)


def meet_your_parents(mother: Folder, first_born=True):
	# Eğer recursion başlamadıysa
	if first_born: mother.parent = mother
	# her bir alt eleman için
	for child in mother.sub_elements:
		# alt elemanın parentını 
		# şu anki folder olarak belirle
		child.parent = mother
		# eğer alt eleman Foldersa onun alt 
		# elemanları için de aynı işlemi yap
		if type(child) == Folder:
			# çocuklara haddini bildir
			meet_your_parents(child, first_born=False)

# default_structureın parentlarını ayarla
meet_your_parents(default_structure)


# def check_properties(path, _type):
# 	return os.path.exists(os.path.join(path, "properties.json"))	# BURAYI GELİŞTİR


# def is_db_folder(path):
# 	return os.isdir(path) and \
# 			check_properties(path, Folder)
 			

# def find_databases(path):
# 	return [name for name in os.listdir(path) if is_db_folder(os.path.join(path, name))]



