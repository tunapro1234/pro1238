from src.database import Folder, Subject, Entry
import src.database as ldb
import res.globals as glb
import os


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
#	print(glb.warn, "PWD IMPLEMENTATION NOT COMPLETED.")
	print(f"Current folder name: {selected.name}")
	return db, selected, True


def _cd(db, selected, argv):
	argv = [] if argv is None else argv
	selected = db if selected is None else selected
	d_arguments = [i for i in argv if i.startswith("-")]

	target = [i for i in argv if not i.startswith("-") and i != argv[0]]
	# Birden fazla klasör verildiyse hata ver
	if len(target) > 1: 
		print("Too many arguments...")
		return db, selected, False
	# Eğer sadece cd yazıldıysa root klasöre geri dön
	elif len(target) == 0:
		target.append("/")
	target = target[0]

	new_selected = (db if target.startswith("/") \
			else selected).find_by_path(target)

	if new_selected == False: 
		print(f"No such file or directory: {target}")
		return db, selected, False
	return db, new_selected, True


def ls_recursive(target: Folder, tab=" "):
	# belirli bşr klasör altındaki tüm klasörleri görmemizi sağlıyor
	# öncelikle bulunduğumuz klasörün ismi
	output = colorize_element(target) + "\n"
	# klasörün içindeki her bir eleman için
	for element in target.sub_elements:	
		# eğer eleman klasörse o klasör için bu fonksyionu tekrar çağır
		if type(element) == Folder:
			# her bir satırı parçala ve satır başlarına tab ekle
			output += "\n".join([tab + line for line in \
					ls_recursive(element, tab).split("\n") if line != ""]) + "\n"
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

def _ls(db, selected=None, argv=None):
	# klasik default argüman şeyleri
	argv = [] if argv is None else argv
	selected = db if selected is None else selected
	d_arguments = [i for i in argv if i.startswith("-")]
	# Bu değişkenin ileride düzenlenmesi gerekebilir
	options = "".join(d_arguments).replace("-", "")

	# eğer klasör yerine dosyayı lslemeye çalışırsak
	if type(selected) == Subject:
		print("Cannot ls into Subject")
		return db, selected, False

	rv = True
	targets = [i for i in argv if not i.startswith("-") and i != argv[0]]
	if len(targets) > 0:
		for i, target in enumerate(targets):
			if len(targets) > 1:
				print(f"{target}: ")

			# sonsuz döngüye girmemek için 
			# argvden targetları siliyoruz
			filtered_argv = [argv[0]] + d_arguments
			# target stringini target objesine çevirip
			# ls fonksiyonuna selected olarak veriyoruz
			target_object = selected.find_by_path(target)
		
			# eğer path bulunamadıysa
			if target_object == False:
				print(f"No such file or directory: {target}")
			else:
				# eğer recursive lslerden herhangi biri 
				# false döndürürse biz de false döndüreceğiz
				if _ls(db, target_object, filtered_argv)[2] == False:
					rv = False
			# son satırda ek boşluk bırakmasın diye
			if i + 1 != len(targets): print()
		return db, selected, rv


	# eğer tüm dosta ve klasörlerim recursive bir şekilde okumak istesek
	if "r" in options: 
		print(ls_recursive(selected), end="")
	else: 
		# elemanları okuyup renklendir
		output = [colorize_element(e) for e in selected.sub_elements]
		# eğer liste halinde isteniyorsa alt alta sırala
		if "l" in options: output = "\n".join(output)
		# liste değilse boşluk yeterli
		else: output = " ".join(output)
		# yapıştır gitsin
		print(output)
	return db, selected, True

def _le(db, selected, argv):
	raise NotImplemented


def _rm(db, selected, argv):
	raise NotImplemented

def _re(db, selected, argv):
	raise NotImplemented


def _add_folder(*args, **kwargs):
	return _mkdir(*args, **kwargs)

def _mkdir(db, selected, argv):
	raise NotImplemented


def _add_subject(*args, **kwargs):
	return _mksub(*args, **kwargs)

def _mksub(db, selected, argv):
	raise NotImplemented


def _add_entry(*args, **kwargs):
	return _mkent(*args, **kwargs)

def _mkent(db, selected, argv):
	raise NotImplemented


def _clear(db, selected, *args, **kwargs):
	os.system("clear")
	return db, selected, True

def _exit(*args, **kwargs):
	quit()

