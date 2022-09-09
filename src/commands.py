from src.database import Folder, Subject, Entry
import src.database as db
import res.globals as glb
import datetime
import os


def _help(*args, **kwargs):
	for key, value in glb.keywords_help.items():
		print(f"[{key}]: {value}")
	return True

def _reconfigure(env, *args, **kwargs): 
	raise Exception("not implemented")

def _init(env, *args, **kwargs): 
	db.write_database()
	print(f"{glb.info} database created successfully")

	# Yeni databasei oku
	env.reset(db.read_database())


def _pwd(env, *args, **kwargs):
	print(env.get_path(env.curdir))


def _cd(env, argv):
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-") and i != "-"]

	target = [i for i in argv if (not i.startswith("-") and i != argv[0]) or i == "-"]
	# Birden fazla klasör verildiyse hata ver
	if len(target) > 1: 
		raise Exception("too many arguments")
	# Eğer sadece cd yazıldıysa root klasöre geri dön
	elif len(target) == 0:
		target.append("/")
	target = target[0]
	newdir = env.get_from_path(target)

	if newdir == False: 
		raise Exception(f"no such file or directory: {target}")
	elif type(newdir) != Folder:
		raise Exception(f"not a directory: {target}")

	env.curdir = newdir


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

def _ls(env, argv=None, __dir=None):
	# klasik default argüman şeyleri
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-")]
	# Bu değişkenin ileride düzenlenmesi gerekebilir
	options = "".join(d_arguments).replace("-", "")

	### Recursionı ayarlayan kısım
	# eğer fonksiyon recursion ile çağırılmamışsa
	if __dir is None:
		# hedefleri belirle
		targets = [i for i in argv if not i.startswith("-") and i != argv[0]]
		# eğer hedef varsa (ls target gibi)
		if len(targets) > 0:
			# her bir hedef klasör için
			for i, target in enumerate(targets):
				# eğer birden fazla hedef varsa hangi hedefi
				# yazdırdığını belirt
				if len(targets) > 1:
					print(f"{target}: ")

				# eğer recursive lslerden herhangi biri 
				# false döndürürse biz de false döndüreceğiz
				try:
					# target stringini target objesine çevirip
					# ls fonksiyonuna __dir olarak veriyoruz ve 
					# böylece recursion ile çağırıldığını anlıyor
					target_object = env.get_from_path(target)

					_ls(env, argv, __dir=target_object)

				except Exception as e:
					##!##
					print(f"{glb.fail} {argv[0]}: {e}")

				# son satırda ek boşluk bırakmasın ama 
				# onun dışında aradaboşluk bıraksın
				if i + 1 != len(targets): print()
			# target varsa recursionla her şeyi hallettik,
			# artık çıkabiliriz
			return
		# eğer sadece ls girildiyse, target 
		# olmuyor ve recursion da olmuyor
		# ve işleme direkt bu fonksiyondan devam ediyoruz
		__dir = env.curdir

	### Recursionın çağırdığı alt kısım, yazdırma işlemi

	## Başlangıç
	# eğer tüm dosta ve klasörleri
	# recursive bir şekilde yazdırmak istesek
	if "r" in options: 
		output = ls_recursive(__dir)
	else: 
		output = [colorize_element(e) for e in __dir.sub_elements]
	
	## Düzenleme
	# r opsiyonu a opsiyonuna göre öncelikli ve ikisi birbiriyle çakışıyor.
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


def _le(env, argv):
	print(f"{glb.warn} {argv[0]} implementation not completed")
	targets = [i for i in argv if not i.startswith("-") and i != argv[0]]

	if len(targets) == 0: 
		raise Exception("missing target")
	elif len(targets) > 1:
		raise Exception("multiple targets not supported")

	target = env.get_from_path(targets[0])
	# data yoksa boşuna boşluk bırakma
	if len(target.data) == 0: return

	print(*[ \
			f"{i}. date: {e.get_str_date()}; " + \
			f"\tD: {e.correct}, \tY: {e.wrong}, \tN: {e.correct - e.wrong/4}".expandtabs(6) \
			for i, e in enumerate(target.data)], sep="\n")


def _rm(env, argv):
	argv = [] if argv is None else argv
	d_arguments = [i for i in argv if i.startswith("-")]
	options = "".join(d_arguments).replace("-", "")

	current_path = env.get_path(env.curdir)
	targets = [i for i in argv if not i.startswith("-") and i != argv[0]]
	for target in targets:
		try:
			target_object = env.get_from_path(target)

			target_path = env.get_path(target)		
			if target_path in current_path:
				raise Exception("trying to delete a parent directory to current one")
			else:
				_type = "Subject" if type(target_object) == Subject else "Folder"
				print(f"{glb.warn} {argv[0]}: remove {_type} {target}? ", end="")
				if input() == "y":
					env.remove(target_object)
					print(f"{glb.info} {argv[0]}: deleted {target_path}")
				else:
					print(f"{glb.info} {argv[0]}: canceled")

		except Exception as e:
			##!##
			print(f"{glb.fail} {argv[0]}: {e}")

	if len(targets) == 0:
		raise Exception("missing target")



def _re(env, argv):
	raise Exception("not implemented")


def _mkdir(env, argv):
	raise Exception("not implemented")


def _mksub(env, argv):
	raise Exception("not implemented")


def _mkent(env, argv):
	print(f"{glb.warn} {argv[0]}: implementation not completed")
	targets = [i for i in argv if not i.startswith("-") and i != argv[0]]

	if len(targets) == 0: 
		raise Exception("missing target.")
	elif len(targets) > 1:
		raise Exception("multiple targets not supported")

	target = env.get_from_path(targets[0])

	get_entry_data(target)
	db.write_database(env.root)


def get_entry_data(target, date=None):
	date = datetime.datetime.now() if date is None else date
	if type(target) == Folder:
		correct, wrong = 0, 0
		for element in target.sub_elements:
			rv = get_entry_data(element)
			if rv == False: 
				try:
					correct, wrong = ask_data(target)
				except: 
					print()
					return False
				break
			
			else:
				correct += rv[0] 
				wrong += rv[1]
	
		# garanti olsun diye keyword arg olarak girdim
		target.add_entry(date=date, correct=correct, wrong=wrong)
		return correct, wrong

	elif type(target) == Subject:
		try:
			correct, wrong = ask_data(target)
		except: 
			print()
			return False
	
		# garanti olsun diye keyword arg olarak girdim
		target.add_entry(date=date, correct=correct, wrong=wrong)
		return correct, wrong
	
	else:
		raise Exception("malfunction 1")


def ask_data(target, state=None):
	if state is None:
		return ask_data(target, 0), ask_data(target, 1)

	# eğer state 0 sa doğru sayısını iste 
	# değilse yanlış sayısını iste
	# evet biraz kafa karıştırıcı biliyorum
	val = "D" if state == 0 else "Y"
	print(f"{target.name}: {val} > ", end="")
	inp = input()

	# eğer bir şey girilmemişse hata ver
	if inp.strip() == "": raise Exception("Skipped")
	# eğer sayı girilmemişse hata ver
	if inp.isnumeric() != True: raise Exception("Input Error")
	return int(inp)


def _clear(*args, **kwargs):
	os.system("clear")
	return True


def _exit(*args, **kwargs):
	quit()
	# zort
	return True

