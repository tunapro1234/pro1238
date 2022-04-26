from res.globals import __version__ as _ver
import json
import os

# şimdi 
# hmm
# folder olsun subject olsun
# folder subjectlerin birleşimi databasei oluştursun
# 
# 

class Folder:
	def __init__(self, name: str, version: str, sub_elements: list, data: list):
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

class Subject:
	def __init__(self, name: str, version: str, target: float, factor: float, data: list):
		self.version = version
		self.name = name

		self.target = target
		self.factor = factor
		self.data = data

	def __dict__(self):
		return {
				"version": self.version,
				"name": self.name,
				"target": self.target,
				"factor": self.factor,
				"data": [entry.__dict__() for entry in self.data] 
				}

class Entry:
	def __init__(self, _id, subject, date, correct, wrong):
		self._id = _id
		self.date = date
		self.subject = subject
	
	def __dict__(self):
		return {
				"_id": self._id,
				"date": self.date, # BURAYA DÜZENLEME LAZIM
				"correct": self.correct,
				"wrong": self.wrong
				}
				

default_structure = Folder("data", _ver, [
							Folder("tyt", _ver, [
								Subject("tr", _ver, 0, 0, {})
								]), 

							Folder("ayt", _ver, [
								Subject("mat", _ver, 0, 0, {})
								])
							])

# default_structure = Folder("data", _ver, [Subject("mat", _ver, 0, 0, {})])
default_path = "res/data"

def read_database(path: str = default_path):
	if os.path.isdir(path):
		with open(os.path.join(path, "properties.json")) as file:
			read = json.load(file)
		
		sub_elements = [read_database(os.path.join(path, element)) for element in read["sub_elements"]]
		main_folder = Folder(read["name"], read["version"], sub_elements)
		return main_folder

	elif os.path.isfile(path):
		with open(path) as file:
			read = json.load(file)
		return Subject(**read)

def write_database(path: str = default_path, structure: Folder = default_structure):
	if not os.path.exists(path): return False
	
	with open(os.path.join(path, "properties.json"), "w+") as file:
		json.dump(structure.__dict__(), file)
	
	for element in structure.sub_elements:
		if type(element) == Folder:
			os.mkdir(os.path.join(path, element.name))
			write_database(os.path.join(path, element.name), element)

		elif type(element) == Subject:
			with open(os.path.join(path, element.name + ".json"), "w+") as file:
				json.dump(element.__dict__(), file)
	return True







