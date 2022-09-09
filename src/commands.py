from src.database import Folder, Subject, Entry
import src.database as db
import res.globals as glb
import os


def _help(*args, **kwargs):
	for key, value in glb.keywords_help.items():
		print(f"[{key}]: {value}")
	return True

def _reconfigure(env, *args, **kwargs): 
	raise NotImplemented

def _init(env, *args, **kwargs): 
	if (rv := db.write_database()) == True:
		print("Database created successfully.")

	# Yeni databasei oku
	env.reset(db.read_database())
	return rv


def _pwd(env, *args, **kwargs):
	print(env.get_path(env.curdir))
	return True


def _cd(env, argv):
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-") and i != "-"]

	target = [i for i in argv if (not i.startswith("-") and i != argv[0]) or i == "-"]
	# Birden fazla klasör verildiyse hata ver
	if len(target) > 1: 
		print("Too many arguments...")
		return False
	# Eğer sadece cd yazıldıysa root klasöre geri dön
	elif len(target) == 0:
		target.append("/")
	target = target[0]
	newdir = env.get_from_path(target)

	if newdir == False: 
		print(f"No such file or directory: {target}")
		return False
	elif type(newdir) != Folder:
		print(f"Not a directory: {target}")
		return False
	env.curdir = newdir
	return True

def ls_recursive(target: Folder, tab=" "):
	# belirli bşr klasör altındaki tüm klasörleri görmemizi sağlıyor
	# öncelikle bulunduğumuz klasörün ismi
	output = [colorize_element(target)]
	# klasörün içindeki her bir eleman için
	for element in target.sub_elements:	
		# eğer eleman klasörse o klasör için bu fonksyionu tekrar çağır
		if type(element) == Folder:
			# her bir satırı parçala ve satır başlarına tab ekle
			output += [tab + line for line in ls_recursive(element, tab) if line != ""]
		# klasör değilse
		elif type(element) == Subject:
			# başa tab at ve çıktıya ekle
			output.append(tab + colorize_element(element))
	return output

def colorize_element(element):
	# verilen elemana göre renklendirme
	if type(element) == Folder:
		return glb.colorize(element.name, glb.folder_color)
	elif type(element) == Subject:
		return glb.colorize(element.name, glb.subject_color)
	elif element in "..":
		return glb.colorize(element, glb.folder_color)
	else: raise Exception

def _ls(env, argv=None):
	# klasik default argüman şeyleri
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-")]
	# Bu değişkenin ileride düzenlenmesi gerekebilir
	options = "".join(d_arguments).replace("-", "")

	# eğer klasör yerine dosyayı lslemeye çalışırsak
	if type(env.curdir) == Subject:
		print("Cannot ls into Subject")
		return False

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
			target_object = env.get_from_path(target)

			# eğer path bulunamadıysa
			if target_object == False:
				print(f"No such file or directory: {target}")
			else:
				curdir = env.curdir
				env.curdir = target_object
				# eğer recursive lslerden herhangi biri 
				# false döndürürse biz de false döndüreceğiz
				if _ls(env, filtered_argv) == False:
					rv = False
				env.curdir = curdir

			# son satırda ek boşluk bırakmasın diye
			if i + 1 != len(targets): print()
		return rv


	## Başlangıç
	# eğer tüm dosta ve klasörleri
	# recursive bir şekilde okumak istesek
	if "r" in options: 
		output = ls_recursive(env.curdir)
	else: 
		output = [colorize_element(e) for e in env.curdir.sub_elements]
	
	## Düzenleme
	# eğer hepsi okunmak isteniyorsa (ve "r" yoksa). ve .. da gösteriliyor
	if "a" in options and "r" not in options:
		output = [colorize_element("."), colorize_element("..")] + output

	## Birleştirme
	# eğer liste halinde isteniyorsa alt alta sırala
	if "l" in options: 
		output = "\n".join([f"{i}. {j}" for i, j in enumerate(output)] \
				+ [f"total {len(output)} objects"])
	# recursive güzel gözüksün diye alt alta yazdır
	elif "r" in options: output = "\n".join(output)
	# liste değilse boşluk yeterli
	else: output = "  ".join(output)
	# yapıştır gitsin
	print(output)
	return True


def _le(env, argv):
	raise NotImplemented


def _rm(env, argv):
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-")]
	options = "".join(d_arguments).replace("-", "")

	rv = True
	current_path = env.get_path(env.curdir)
	targets = [i for i in argv if not i.startswith("-") and i != argv[0]]
	for target in targets:
		target_object = env.get_from_path(target)

		if target_object == False:
			print(f"No such file or directory: {target}")
			rv = False
		else:
			target_path = env.get_path(target)		
			if target_path in current_path:
				print("Trying to delete a parent directory to current one.")
				rv = False
			else:
				_type = "Subject" if type(target_object) == Subject else "Folder"
				print(f"remove {_type} {target}? ", end="")
				if input() == "y":
					rm_rv = env.remove(target_object)
					if rm_rv: print(f"deleted {target_path}")
					else: print(rm_rv)
					
				else:
					print(f"canceled.")

	if len(targets) == 0:
		print("rm: missing target")
		rv = False

	return rv



def _re(env, argv):
	raise NotImplemented


def _add_folder(*args, **kwargs):
	return _mkdir(*args, **kwargs)

def _mkdir(env, argv):
	raise NotImplemented


def _add_subject(*args, **kwargs):
	return _mksub(*args, **kwargs)

def _mksub(env, argv):
	raise NotImplemented


def _add_entry(*args, **kwargs):
	return _mkent(*args, **kwargs)

def _mkent(env, argv):
	raise NotImplemented


def _clear(*args, **kwargs):
	os.system("clear")
	return True


def _exit(*args, **kwargs):
	quit()
	# zort
	return True

