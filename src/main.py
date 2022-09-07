from src.database import Folder, Subject, Entry
import src.database as ldb
import res.globals as glb
import readline
import os

# Merhabaaa...
# sınav senemdeyim ve sınava yaklaşık 55 gün kaldı
#	  ben de kafayı yemeye başladım
#
# {
#	:-( 
# 	Mezuna kaldık iyi mi
# 	Lanet olası yazılım
# }
#
#
# ne yapacağıma dair planlama yapacağım
# bayadır yazılım yapmıyorum
# 
# database sistemi klasör ve json bazlı olacak her bir klasörün kendine ait 
# properties.json tarzında bir dosyası olacak. properties.json dosyasının içinde 
# tam olarak ne olacağını bilmiyorum, ama versiyon kontrolü çok önemli.
# 
# Versiyon kontrolü için aklımda ufak bir fikir var. Her kod yenilediğimde versiyon
# değiştirmekle uğraşmamak için dosyaların hashini aldırmayı planlıyorum.
# { güzel plan ama uğraşılmaz }
# 
# dosya ayrımı ders bazında yapılacak her bir ders json dosyasının içinde de tarih
# bazında sıralama yapılacak.
# 
# keyword belirlemeliyim
# { belirlediğim neredeyse tüm keywordler değişti }

 
#	write_database ve read_database fonksiyonlarına 
#	exception handling geliştirmeleri
#	(çoğunlukla tamam)
#
#	_add_entry fonksiyonları
#
# TODO
# "" error parsing
# var olan databasei yok edecek her fonksiyona check konulmalı
# CD:
# LS:
#	ls /folder/subject
#	ls -l
#
# DATABASE:
#	check_properties()
#
# excel export
# passing sub_elements to functions??



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


def ls_recursive(target: Folder, tab="	"):
	# belirli bşr klasör altındaki tüm klasörleri görmemizi sağlıyor
	# öncelikle bulunduğumuz klasörün ismi
	output = colorize_element(target) + "\n"
	# klasörün içindeki her bir eleman için
	for element in target.sub_elements:	
		# eğer eleman klasörse o klasör için bu fonksyionu tekrar çağır
		if type(element) == Folder:
			# her bir satırı parçala ve satır başlarına tab ekle
			output += "\n".join([tab + line for line in ls_recursive(element, tab).split("\n") if line != ""]) + "\n"
		# klasör değilse
		elif type(element) == Subject:
			# başa tab at ve çıktıya ekle
			output += tab + colorize_element(element) + "\n"
	return output

def colorize_element(element):
	# verilen elemana göre renklendirme
	if type(element) == Folder:
		return glb.colorize(element.name, glb.folder_color)
	elif type(element) == Subject:
		return glb.colorize(element.name, glb.subject_color)
	else: raise Exception

def _ls(db, selected=None, arguments=None, d_arguments=None):
	# klasik default argüman şeyleri
	selected = db if selected is None else selected
	arguments = [] if arguments is None else arguments
	d_arguments = [] if d_arguments is None else d_arguments

	# eğer klasör yerine dosyayı lslemeye çalışırsak
	if type(selected) == Subject:
		print("Cannot ls into Subject")
		return db, selected, False

	# eğer hedef argüman olarak belirtildiyse
	if len(arguments) == 1:
		return _ls(db, selected.find_by_path(arguments[0]), None, d_arguments)

	# eğer birden fazla hedef argüman olarak belirtildiyse
	elif len(arguments) > 1:
		# her bir argüman için tekrar bu fonksiyonu çağırıyoruz
		for i, target in enumerate(arguments):
			print(f"{target}: ")
			# recursion işte
			_ls(db, selected.find_by_path(target), None, d_arguments)
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

def _exit(*args, **kwargs):
	quit()


def check_input(db, selected, keywords, text):
	if text == "": return False
	
	for word in text.split(" "):
		if check_if_path(db, selected, word): continue
		if word in keywords: continue
		if word == "": continue
		return False
	return True


def parser(input_text, database, selected_element=None):
	selected_element = database if selected_element is None else selected_element
	# Biraz illegal ama debugging kolaylaştırmak için 
	# her çıkmak istediğimde exit yazmamalıyım
	if input_text in ["q", "quit"]: quit()
	
	# verilen inputta hata yoksa
	if check_input(database, selected_element, glb.keywords, input_text):
		# inputtan koparmak istediğimiz üç farklı string/array var
		# biri arguments, sadece dosya ya da klasör ismi olabiliyor
		arguments = []
		# biri d_arguments "-" ile başlayan argümanlar için
		d_arguments = ""
		# diğeri de fonksiyon ismi
		function_name = []
		# her bir kelime için
		for word in input_text.split(" "):
			# eğer sona boşluk bırakılırsa ya da iki 
			# boşluk bırakılırsa hata çıkmasın diye
			if word == "": continue
			# eğer kelime "-" ile başlıyorsa "-"yi atıp d_argumentsa ekle
			if word.startswith("-"): 
				d_arguments += word[1:]
			# eğer kelime seçili olan klasörün altındaki 
			# bir eleman ismine eşitse argumentsa ekle
			elif check_if_path(database, selected_element, word): 
				arguments.append(word)
			# hiçbiri değilse fonksyion ismine ekle
			else: 
				function_name.append(word)

		# fonksiyon ismi uyarlaması
		function_name = "_".join(function_name).strip()
		return eval(f"_{function_name}(database, selected_element, arguments, d_arguments)")

	# Release için burası kullanılabilir
#		try:
#			rv = eval(f"_{function_name}(database, selected_element, arguments, d_arguments)")
#		except NameError: pass
#		else: return rv
			
	# Debuggingi kolaylaştırmak için
	print(f"Error parsing: {input_text}")
	return database, selected_element, False


def check_if_path(db, selected, text):
	# Ufak bir wrapper fonksiyon
	if selected is None or db is None: return False
	# Eğer verilen string / ile başlıyorsa kullanacağımız
	# folderı root folder olarak ayarla
	base = db if text.startswith("/") else selected
	# Ana fonksiyon Folder.find_by_path
	# eğer ana fonksiyon False veriyorsa biz de False veriyoruz
	# ama eğer ana fonksiyon obje döndürüyorsa path parsing
	# işlemi başarılı olmuş demektir
	return False if base.find_by_path(text) == False else True


def complete_path(db, selected, word):
	if selected is None or db is None: return []
	base = db if word.startswith("/") else selected

	# her bir / harfinden böl, // görürsen tek bir tane say.
	names = [i for i in word.split("/") if i != ""]
	# eğer verilen pathin sonunda / yoksa son kelimeyi 
	# subject/folder olarak algılama
	names = names if word.endswith("/") else names[:-1]

	# recursion gibi bi şey
	nbase = base
	for name in names:
		# Subjectin find_by_name fonksiyonu yok,
		# eğer folder/subject/subject tarzı bir şey yapılmaya 
		# çalışılırsa hata veriyor
		if type(nbase) == Subject: return []
		# geçen seferki folder içinden gelecek elemanı nbase değişkenine ver
		nbase = nbase.find_by_name(name)
		# eleman isminden bulunamazsa boşver
		if nbase == False: return []

	# son kelimeyi sil
	beg = "/".join(word.split("/")[:-1])
	# eğer verilen string tek kelimeyse yukarıdaki satırda
	# son kelimeyi sildiğimizden sonsuz / koyma döngüsüne
	# girmemesi için
	beg = beg if beg == "" else beg + "/"
	# son eleman yerine olabilecek seçenekleri yerleştir
	return [beg + e for e in nbase.list_sub_names()]
		

def completer_wrapper(db, selected):
	selected = db if selected is None else selected

	# aktif olarak girilen pathi kontrol edebilmemiz için
	# database ve selected_element değişkenlerine de ihtiyacımız
	# var. O yüzden completer üzerine wrapper geçirdim, her 
	# komut için yeni completer fonksiyonu oluşturuluyor
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
	# otomatik tamamlama için temel readline komutları
	# tab completion olcak
	readline.parse_and_bind("tab: complete")
	# bu karakterleri de normal say gibi bi şey herhalde
	readline.set_completer_delims(" \t\n`~!@#$%^&*()-=+[]{}\\|;:\"',<>?")
	# completer fonksiyonu ayarla
	# readline.set_completer(completer_wrapper(None, None))

	# aktif olarak seçili bir eleman yok
	selected = None
	
	# Eğer database okuyabilmişsek yolla bakalım
#	db = rv if (rv := ldb.read_database()) else \
#		(None, print(f"{glb.info} No database found..."))[0]

	# Eğer database okuyabilmişsek yolla bakalım
	db = ldb.read_database()
	if db == False:
		print(f"{glb.info} No database found...")
		db = None

	while True:
		try:
			# completer fonksiyonu ayarla
			readline.set_completer(completer_wrapper(db, selected))
			# kullnıcıdan input al
			input_text = input(f"tunapro1238]{glb.clean} >> ")
			# girilen inputu parsera yolla
			db, selected, rv = parser(input_text, db, selected)

		except KeyboardInterrupt: 
			# aslında input olarak hiçbir şey girilmemişse 
			# ctrl c yapıldığında programdan çıkış yapabilmeyi
			# çok isterdim ama nasıl yapacağımı bulamadım :-(
			print()





