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
# bu biraz sinir bozucu bir davranış bunu değiiştirelim
# ikisi de kendi ismini de alsı
#
# folderın read fonksyonu recursive ve altındaki her şeyi okuyor
# ama write fonksiyonu recursive değil



class Folder:
	def __init__(self, name: str, version: str, sub_elements: list, data: list = []):
		self.version = version
		self.name = name

		self.sub_elements = sub_elements
		self.data = data

	def __dict__(self):
		return {
				"version": self.version,
				"name": self.name,
				"sub_elements": [(element.name if type(element) == Folder 
									else element.name + ".json")
									for element in self.sub_elements],
				"data": [entry.__dict__() for entry in self.data] 
				}

	def write(self, path):
		path = Path(path) if type(path) == str else path
		if not path.parent.exists(): return False
		try:
			if not path.exists(): os.mkdir(path)
			with Path(path, "properties.json").open("w+") as file:
				json.dump(self.__dict__(), file)
		except:
			return False
		return True

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
		read["data"] = Entry.convert_sltel(read["data"])
		return Folder(**read)

	def add_entry(*args, **kwargs):
		return add_entry(*args, **kwargs)


class Subject:
	def __init__(self, name: str, full_name: str, version: str, target: float, factor: float, data: list = []):
		self.version = version
		self.name = name
		self.full_name = full_name

		self.target = target
		self.factor = factor
		self.data = data

	def __dict__(self):
		return {
				"version": self.version,
				"name": self.name,
				"full_name": self.full_name, 
				"target": self.target,
				"factor": self.factor,
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
		read["data"] = Entry.convert_sltel(read["data"])
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
		
	# str list to entry list
	@classmethod
	def convert_sltel(cls, str_list):
		return [Entry(**entry) for entry in str_list]



date_format = "%d/%m/%y %H:%M:%S.%f"

default_path = Path("res/data")
default_structure = Folder("data", _ver, [
							Folder("tyt", _ver, [
								Subject("tr", "tyt türkçe", _ver, 0, 0)
								]), 

							Folder("ayt", _ver, [
								Subject("mat", "ayt matematik", _ver, 0, 0)
								])
							])


def add_entry(self, date = None, *args, **kwargs):
	date = datetime.datetime.now() if date is None else date
	self.data.append(Entry(date, self.name, *args, **kwargs))
	return date

def read_database(path = default_path):
	return Folder.read(path)

def write_database(main_folder: Folder = default_structure, path = default_path):
	if not os.path.exists(Path(path).parent): return False
	if not main_folder.write(path): return False
	# classmethod olan folder read recursive okuyor ama recursive yazmıyor
	# o yüzden bu fonksiyona ihtiyacımız var ama read_database çok da gerekli değil
	for element in main_folder.sub_elements:
		if type(element) == Folder:
			if not write_database(element, Path(path, element.name)): return False
		elif type(element) == Subject:
			if not element.write(Path(path, element.name + ".json")): return False
		else: return False
	return True

# def check_properties(path, _type):
# 	return os.path.exists(os.path.join(path, "properties.json"))	# BURAYI GELİŞTİR
# 
# def is_db_folder(path):
# 	return os.isdir(path) and \
# 			check_properties(path, Folder)
# 			
# def find_databases(path):
# 	return [name for name in os.listdir(path) if is_db_folder(os.path.join(path, name))]



