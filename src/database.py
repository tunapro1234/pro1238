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
	def __init__(self, name: str, version: str, sub_elements: list, comment: str = "", data: list = []):
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
		if not path.exists(): return False

		try:
			with Path(path, "properties.json").open() as file:
				read = json.load(file)
		except: return False

		# sub_elementsı oku ve subject/folder objesine çevir
		read["sub_elements"] = [(Subject if element_name.endswith(".json") else \
			Folder).read(Path(path, element_name)) for element_name in read["sub_elements"]]
		# eğer hata varsa yukarı aktar
		if False in read["sub_elements"]: return False
		# data listesini oku ve entry objesine çevir
		read["data"] = Entry.undict(read["data"])
		return Folder(**read)


	def write_self(self, path):
		path = Path(path) if type(path) == str else path
		if not path.parent.exists(): return False
		try:
			if not path.exists(): os.mkdir(path)
			with Path(path, "properties.json").open("w+") as file:
				json.dump(self.__dict__(), file)
		except:
			return False
		return True


	def write(self, path):
		if not os.path.exists(Path(path).parent): return False
		if not self.write_self(path): return False
		# classmethod olan folder read recursive okuyor ama recursive yazmıyor
		# o yüzden bu fonksiyona ihtiyacımız var ama read_all çok da gerekli değil
		for element in self.sub_elements:
			if type(element) == Subject: 
				element.name += ".json"
			if not element.write(Path(path, element.name)): 
				return False
		return True


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
			if type(nbase) == Subject: return False
			nbase = nbase.find_by_name(name)
			if nbase == False: return False
		return nbase

	def find_by_name(self, name):
		arr = [i for i in self.sub_elements if i.name == name]
		if len(arr) != 1: return False
		return arr[0]

	def add_entry(*args, **kwargs):
		return add_entry(*args, **kwargs)



class Subject:
	def __init__(self, name: str, full_name: str, version: str, 
			factor: float, target: float = 0, comment: str = "", data: list = []):
		self.version = version
		self.name = name
		self.full_name = full_name

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
		if not path.exists(): return False
		
		try:
			with path.open() as file:
				read = json.load(file)
		except: return False
		# sub_elementsı oku ve subject/folder objesine çevir
		read["data"] = Entry.undict(read["data"])
		# Program içinde Folderın sub elements listesindeki objelerin 
		# tipini görebildiğimiz için sonunda .json gibi bir uzantı olmasına
		# ihtiyacımız yok. O yüzden json uzantısını kaldırıyorum.
		# Bunun bize ne gibi bir avantajı olur bilmiyorum ama 
		# en başta böyle yapmışım o yüzden değiştirmekle uğraşmayacağım
		read["name"] = ".".join(read["name"].split(".")[:-1])
		return Subject(**read)


	def write(self, path):
		path = Path(path) if type(path) == str else path
		if not path.parent.exists(): return False

		try:
			with path.open("w+") as file:
				json.dump(self.__dict__(), file)
		except:
			return False
		return True
				

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
				"date": self.date.strftime(date_format),
				"subject_name": self.subject_name,
				"correct": self.correct,
				"wrong": self.wrong,
				"comment": self.comment
				}
		

	@classmethod
	# str list to entry list
	def undict(cls, str_list):
		return [Entry(**entry) for entry in str_list]



date_format = "%d/%m/%y %H:%M:%S.%f"

default_path = Path("res/data")
default_structure = \
		Folder("data", _ver, [
			Folder("tyt", _ver, [
				Subject("tr", "tyt türkçe", _ver, 0),
				Subject("mat", "tyt matematik", _ver, 0),
				Folder("sos", _ver, [
					Subject("tarih", "tyt tarih", _ver, 0),
					Subject("coğrafya", "tyt coğrafya", _ver, 0),
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


def add_entry(self, path, date = None, *args, **kwargs):
	date = datetime.datetime.now() if date is None else date
	self.data.append(Entry(date, self.name, *args, **kwargs))
	if not self.write(): return False
	return date


def read_database(path = default_path):
	return Folder.read(path)


def write_database(main_folder: Folder = default_structure, path = default_path):
	return main_folder.write(path)


# def check_properties(path, _type):
# 	return os.path.exists(os.path.join(path, "properties.json"))	# BURAYI GELİŞTİR


# def is_db_folder(path):
# 	return os.isdir(path) and \
# 			check_properties(path, Folder)
 			

# def find_databases(path):
# 	return [name for name in os.listdir(path) if is_db_folder(os.path.join(path, name))]



