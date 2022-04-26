from res.globals import __version__ as _ver
import datetime
import json
import os

# şimdi 
# hmm
# folder olsun subject olsun
# folder subjectlerin birleşimi databasei oluştursun
# 
# 




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

	def add_entry(self, date = None, *args, **kwargs):
		date = datetime.datetime.now() if date is None else date
		self.data.append(Entry(date, self, *args, **kwargs))
		return date


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

	def add_entry(self, date = None, *args, **kwargs):
		date = datetime.datetime.now() if date is None else date
		self.data.append(Entry(date, self, *args, **kwargs))
		return date


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
	def convert_slte(cls, str_list):
		return [Entry(**entry) for entry in str_list]



date_format = "%d/%m/%y %H:%M:%S.%f"

default_path = "res/data"
default_structure = Folder("data", _ver, [
							Folder("tyt", _ver, [
								Subject("tr", "tyt türkçe", _ver, 0, 0)
								]), 

							Folder("ayt", _ver, [
								Subject("mat", "ayt matematik", _ver, 0, 0)
								])
							])



def read_database(path: str = default_path):
	if os.path.isdir(path):
		with open(os.path.join(path, "properties.json")) as file:
			read = json.load(file)
		
		# sub_elementsı oku ve subject/folder objesine çevir
		read["sub_elements"] = [read_database(os.path.join(path, element)) for element in read["sub_elements"]]
		# data listesini oku ve entry objesine çevir
		read["data"] = Entry.convert_slte(read["data"])
		return Folder(**read)

	elif os.path.isfile(path):
		with open(path) as file:
			read = json.load(file)
		# sub_elementsı oku ve subject/folder objesine çevir
		read["data"] = Entry.convert_slte(read["data"])
		return Subject(**read)


def write_database(structure: Folder = default_structure, path: str = default_path):
	# if not os.path.exists(path): return False
	
	with open(os.path.join(path, "properties.json"), "w+") as file:
		json.dump(structure.__dict__(), file)
	
	for element in structure.sub_elements:
		element_path = os.path.join(path, element.name)
		if type(element) == Folder:
			if not os.path.exists(element_path):
				os.mkdir(element_path)
			write_database(element_path, element)

		elif type(element) == Subject:
			with open(element_path + ".json", "w+") as file:
				json.dump(element.__dict__(), file)
	return True






