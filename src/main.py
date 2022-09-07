import res.globals as glb
import src.database as ldb
import readline
import os

# Merhabaaa...
# sınav senemdeyim ve sınava yaklaşık 55 gün kaldı
#	  ben de kafayı yemeye başladım
# 
# ne yapacağıma dair planlama yapacağım
# 
# bayadır yazılım yapmıyorum
# 
# database sistemi klasör ve json bazlı olacak her bir klasörün kendine ait 
# properties.json tarzında bir dosyaası olacak. properties.json dosyasının içinde 
# tam olarak ne olacağını bilmiyorum, ama versiyon kontrolü çok önemli.
# 
# Versiyon kontrolü için aklımda ufak bir fikir var. Her kod yenilediğimde versiyon
# değiştirmekle uğraşmamak için dosyaların hashini aldırmayı planlıyorum.
# 
# dosya ayrımı ders bazında yapılacak her bir ders json dosyasının içinde de tarih
# bazında sıralama yapılacak.
# 
# keyword belirlemeliyim
#	reconfigure
#	fetch
#	init
#	help
#
#	list 
#		subject
#		folder
#		data
# 
#	add 
#		subject
#		folder
#		data
#
#	remove
#		subject
#		data
#
# şimdilik bu keywordler yeterli


 
#	write_database ve read_database fonksiyonlarına 
#	exception handling geliştirmeleri
#	(çoğunlukla tamam)
#
#	_add_entry fonksiyonları
#
#
# TODO
# var olan database i yok edecek her fonksiyona check konulmalı
# ls -l
# folder bold
# cd 
# passing sub_elements to functions
#
# keywordlerin baştan ayarlanması
# excel export
#



def _help(db, selected, *args, **kwargs):
	for key, value in glb.keywords_help.items():
		print(f"[{key}]: {value}")
	return True

def _reconfigure(db, selected, *args, **kwargs): 
	raise NotImplemented

def _init(db, selected, *args, **kwargs): 
	if (rv := ldb.write_database()) == True:
		print("Database created successfully.")
	return db, selected, rv


def _pwd(db, selected, *args, **kwargs):
	raise NotImplemented


def _cd(db, selected, arguments, d_arguments):
	raise NotImplemented


def ls_recursive(target: ldb.Folder, tab="	"):
	# belirli bşr klasör altındaki tüm klasörleri görmemizi sağlıyor
	# öncelikle bulunduğumuz klasörün ismi
	output = colorize_element(target) + "\n"
	# klasörün içindeki her bir eleman için
	for element in target.sub_elements:	
		# eğer eleman klasörse o klasör için bu fonksyionu tekrar çağır
		if type(element) == ldb.Folder:
			# her bir satırı parçala ve satır başlarına tab ekle
			output += "\n".join([tab + line for line in ls_recursive(element, tab).split("\n") if line != ""]) + "\n"
		# klasör değilse
		elif type(element) == ldb.Subject:
			# başa tab at ve çıktıya ekle
			output += tab + colorize_element(element) + "\n"
	return output

def colorize_element(element):
	# verilen elemana göre renklendirme
	if type(element) == ldb.Folder:
		return glb.colorize(glb.folder_color, element.name)
	elif type(element) == ldb.Subject:
		return glb.colorize(glb.subject_color, element.name)
	else: raise Exception

def _ls(db, selected=None, arguments=None, d_arguments=None):
	# klasik default argüman şeyleri
	selected = db if selected is None else selected
	arguments = [] if arguments is None else arguments
	d_arguments = [] if d_arguments is None else d_arguments

	# eğer klasör yerine dosyayı lslemeye çalışırsak
	if type(selected) == ldb.Subject:
		raise Exception("Cannot ls into Subject")

	# eğer hedef argüman olarak belirtildiyse
	if len(arguments) == 1:
		_ls(db, selected.find_by_name(arguments[0]), None, d_arguments)
		return db, selected, True

	# eğer birden fazla hedef argüman olarak belirtildiyse
	elif len(arguments) > 1:
		# her bir argüman için tekrar bu fonksiyonu çağırıyoruz
		for i, target in enumerate(arguments):
			print(f"{target}: ")
			# recursion işte
			_ls(db, selected.find_by_name(target), None, d_arguments)
			# son satırda ek boşluk bırakmasın diye
			if i + 1 != len(arguments): print()
		return db, selected, True


	# eğer tüm dosta ve klasörlerim recursive bir şekilde okumak istesek
	if "r" in d_arguments: 
		print(ls_recursive(selected), end="")
	else: 
		# elemanları okuyup renklendir
		output = [colorize_element(e) for e in selected.sub_elements]
		# eğer liste halinde isteniyorsa alt alta sırala
		if "l" in d_arguments: output = "\n".join(output)
		# liste değilse boşluk yeterli
		else: output = " ".join(output)
		# yapıştır gitsin
		print(output)
	return db, selected, True

def _le(db, selected, arguments, d_arguments):
	raise NotImplemented


def _rm(db, selected, arguments, d_arguments):
	raise NotImplemented

def _re(db, selected, arguments, d_arguments):
	raise NotImplemented


def _add_folder(*args, **kwargs):
	return _mkdir(*args, **kwargs)

def _mkdir(db, selected, arguments, d_arguments):
	raise NotImplemented


def _add_subject(*args, **kwargs):
	return _mksub(*args, **kwargs)

def _mksub(db, selected):
	raise NotImplemented


def _add_entry(*args, **kwargs):
	return _mkent(*args, **kwargs)

def _mkent(db, selected):
	raise NotImplemented


def _clear(db, selected, *args, **kwargs):
	os.system("clear")
	return db, selected, True



def check_input(text, keywords, selected):
	if text == "": return False
	# keyword listesinde olan tüm kelimeler verilen stringden çıkarılıyor
	# sona herhangi bir kelime kaldıysa hata veriyor
	for keyword in keywords:
		text = text.replace(keyword, "")
	for element in selected.sub_elements:
		text = text.replace(element.name, "")

	# eğer fonksiyona gönderilmeye çalışılan bir argümansa onu da çıkar
	text = " ".join([i for i in text.split(" ") if not i.startswith("-")])
	return not bool(len(text.strip()))


def parser(input_text, database, selected_element=None):
	selected_element = database if selected_element is None else selected_element

	# verilen inputta hata yoksa
	if check_input(input_text, glb.keywords, selected_element):
		# inputtan koparmak istediğimiz üç farklı string/array var
		# biri arguments, sadece dosya ya da klasör ismi olabiliyor
		arguments = []
		# biri d_arguments "-" ile başlayan argümanlar için
		d_arguments = ""
		# diğeri de fonksiyon ismi
		function_name = []
		# her bir kelime için
		for i in input_text.split(" "):
			# eğer sona boşluk bırakılırsa ya da iki 
			# boşluk bırakılırsa hata çıkmasın diye
			if i == "": continue
			# eğer kelime "-" ile başlıyorsa "-"yi atıp d_argumentsa ekle
			if i.startswith("-"): 
				d_arguments += i[1:]
			# eğer kelime seçili olan klasörün altındaki 
			# bir eleman ismine eşitse argumentsa ekle
			elif i in selected_element.list_sub_names(): 
				arguments.append(i)
			# hiçbiri değilse fonksyion ismine ekle
			else: 
				function_name.append(i)

		# fonksiyon ismi uyarlaması
		function_name = "_".join(function_name).strip()
		return eval(f"_{function_name}(database, selected_element, arguments, d_arguments)")

#		try:
#			rv = eval(f"_{function_name}(database, selected_element, arguments, d_arguments)")
#		except NameError: pass
#		else: return rv
			
	return database, selected_element, f"Error parsing: {input_text}"


def complete_path(db, selected, word):
	if selected is None or db is None: return []
	base = db if word.startswith("/") else selected

	names = [i for i in word.split("/") if i != ""]
	names = names if word.endswith("/") else names[:-1]
	nbase = base
	for name in names:
		nbase = nbase.find_by_name(name)

	beg = "/".join(word.split("/")[:-1])
	beg = beg if beg == "" else beg + "/"
	return [beg + e for e in nbase.list_sub_names()]
		

def completer_wrapper(db, selected):
	selected = db if selected is None else selected

	def completer(text, state):
		words = readline.get_line_buffer().split(" ")
		vocab = []

		if len(words) == 1:
			vocab = glb.commands

		if words[0] == "add":
			if len(words) == 2:
				vocab = glb.command_args
			elif len(words) == 3:
				vocab = complete_path(db, selected, words[2])

		if selected is not None and words[0] in ["ls", "rm", "cd"]:
			vocab = complete_path(db, selected, words[1])
			
		results = [i for i in vocab if i.startswith(words[-1])] + [None]
		return results[state]
	return completer
	

def _main():
	readline.parse_and_bind("tab: complete")
	readline.set_completer_delims(" \t\n`~!@#$%^&*()-=+[]{}\\|;:\"',<>?")
	readline.set_completer(completer_wrapper(None, None))

	selected_element = None
	# Eğer database okuyabilmişsek yolla bakalım
	database = rv if (rv := ldb.read_database()) else \
		(None, print(f"{glb.info} No database found..."))[0]


	try:
		while True:
			readline.set_completer(completer_wrapper(database, selected_element))
			database, selected_element, rv = \
				parser(input(f"tunapro1238]{glb.clean} >> "), database, selected_element)
			if rv != True: print(rv)

	except KeyboardInterrupt: 
		print()





