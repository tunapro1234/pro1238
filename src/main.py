from src.database import Folder, Subject, Entry
import src.commands as cmd
import src.database as db
import res.globals as glb
import readline

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

 
# DONE
# /ty tab complete hatası
# var olan databasei yok edecek her fonksiyona check konulmalı
#
# TODO
# ls /tyt/folder seçeneklerin kısaltılması
# database için lock oluşturulmalı
#
# entry fonksiyonları
# folder/subject oluşturma fonksiyonları
#
# excel export


class Environment:
	# programla ilgili genel global 
	# değişkenlerin tutulacağı değişken classı
	def __init__(self, root=None, curdir=None):
		self.__current_path = None
		self.__last_path = None

		self.root = root
		self.curdir = curdir


	def reset(self, new_database):
		self.__current_path = None
		self.__last_path = None

		self.root = new_database
		self.curdir = self.root

	@property
	def curdir(self):
		return self.__curdir	


	@curdir.setter
	def curdir(self, value):
		if type(value) not in [Subject, Folder, type(None)]:
			raise Exception(\
				"current directory must be a Folder or a Subject")

		if value is None:
			self.__curdir = self.root
			self.__last_path = self.__current_path
			self.__current_path = None if self.root is None else "/"
		else:
			self.__curdir = value
			self.__last_path = self.__current_path
			self.__current_path = self.__get_path(value)

		
	def __get_path(self, target, internal=True):
		path = []
		current = self.get_from_path(target) \
				if type(target) == str else target

		# eğer bulunduğumuz klasörün pathini istiyorsak
		# o değeri direkt kaydettiğimizden hesaplamakla uğraşma
		if not internal and current == self.curdir:
			return self.__current_path
		
		while current != self.root:
			path = [current.name] + path
			current = current.parent
		return "/" + "/".join(path)


	def get_path(self, *args, **kwargs):
		return self.__get_path(*args, **kwargs, internal=False)


	def get_from_path(self, path):
		# Database yoksa sal
		if self.curdir is None or self.root is None: 
			raise Exception("no database found")
		# - işareti son girilen klasöre uçuracak
		if path == "-":
			# Eğer daha öncesinde açılmış bir klasör yoksa
			if self.__last_path is None: 
				# hata ver ve çık
				raise Exception("last_path not set")
			# Hedefi önceki klasörle değiştir
			path = self.__last_path
		# Eğer verilen string / ile başlıyorsa kullanacağımız
		# folderı root folder olarak ayarla
		return (self.root if path.startswith("/") else self.curdir).find_by_path(path)

	def remove(self, element):
		# Root klasördeysek
		if element.parent == element:
			raise Exception("cannot delete root folder")

		element.parent.remove_element(element)
		self.root.write(path=db.default_path)


def parser(env, input_text):
	# İllgal bir kaçış ehe
	if input_text in ["q", "quit"]: quit()

	# şimdilik sadece bu operatörü test için geliştiriyorum
	if "&&" in input_text:
		for command in input_text.split("&&"):
			parser(env, command)
		return

	# boşluklardan böl argüman olarak yedir
	argv = [i for i in input_text.split(" ") if i != ""]

	# eğer "" girilirse boşver
	if len(argv) == 0: return

	# Eğer çalıştırılmaya çalışılan fonksiyon bizim 
	# yazdığımız fonksiyonlardan değilse kabul etme
	elif argv[0] not in glb.keywords:
		return print(f"{glb.fail} command not found: {input_text}")
	
	# database yoksa ve databasee ihtiyacı 
	# olan bir fonksiyon çağırmaya çalışıyorsak
	if argv[0] in glb.database_dependent_keywords and env.root is None:
		return print(f"{glb.warn} database necessary for command: {argv[0]}")

	try:
		# fonksiyonu çağır
		eval(f"cmd._{argv[0]}(env, argv)")
	except Exception as e:
		##!##
		print(f"{glb.fail} {argv[0]}: {e}")


def check_if_path(env, path):
	# Ana fonksiyon Folder.find_by_path() ve Environment.get_from_path()
	# eğer ana fonksiyon False veriyorsa biz de False veriyoruz
	# ama eğer ana fonksiyon obje döndürüyorsa path parsing
	# işlemi başarılı olmuş demektir
	try:
		env.get_from_path(path)
	except: return False
	else: return True


def complete_path(env, word):
	# Eğer herhangi bir database bulunamadıysa salla
	if env.curdir is None or env.root is None: return []
	# Eğer / ile başlıyorsa root klasörden aramaya başla
	base = env.root if word.startswith("/") else env.curdir
	# aynı linuxtaki gibi

	# her bir / harfinden böl, // görürsen tek bir tane say.
	names = [i for i in word.split("/") if i != ""]
	# sadece "/" yazılmışsa ya da
	#	/herhangi_bi_şey yazılmışsa 
	if word == "/" or \
			(word.startswith("/") and len(names) == 1):
		nbase = env.root
		beg = "/"

	else:
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
			# geçen seferki folder içinden 
			# gelecek elemanı nbase değişkenine ver
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
	final = []
	for element in nbase.sub_elements:
		final.append(beg + element.name)
		if type(element) == Folder:
			final[-1] += "/"
	return final

		

def completer_wrapper(env):
	# aktif olarak girilen pathi kontrol edebilmemiz için
	# database ve env.curdir_element değişkenlerine de ihtiyacımız
	# var. O yüzden completer üzerine wrapper geçirdim, her 
	# komut için yeni completer fonksiyonu oluşturuluyor
	def completer(text, state):
		words = readline.get_line_buffer().split(" ")
		vocab = []

		if len(words) == 1:
			vocab = glb.keywords

		if env.curdir is not None \
				and words[0] in glb.path_user_keywords:
			vocab = complete_path(env, words[1])
			
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
	
	try:
		# Eğer database okuyabilmişsek yolla bakalım
		database = db.read_database()
	except:
		print(f"{glb.info} No database found...")
		database = None

	# environment variableları initleniyor
	env = Environment(root=database)

	while True:
		# databasete istenmeyen bir değişiklik 
		# olduysa değişikliğe ayak uydur
		if db.is_database_changed(env.root):
			print(f"{glb.warn} database lost")
			env.reset(None)
					
		# completer fonksiyonu ayarla
		readline.set_completer(completer_wrapper(env))
		# eğer database okunmuşsa içinde 
		# bulunduğumuz klasörü prompta da yazdır
		prompt = f"{glb.inpst} >> " if env.curdir is None \
				else f"tunapro1238 {env.curdir.name}]{glb.clean} >> "
		try:
			# kullanıcının girdiği inputu parsera yolla
			parser(env, input(prompt))

		except KeyboardInterrupt: 
			# aslında input olarak hiçbir şey girilmemişse 
			# ctrl c yapıldığında programdan çıkış yapabilmeyi
			# çok isterdim ama nasıl yapacağımı bulamadım :-(
			print()



def _main_tester(input_text=""):
	""" unittesting için """
	# neden readline yaptığımızı bilmiyorum
	readline.parse_and_bind("tab: complete")
	readline.set_completer_delims(" \t\n`~!@#$%^&*()-=+[]{}\\|;:\"',<>?")

	# database okumakla uğraşma direkt programa 
	# tanımlı olan boş database templateini kullan
	database = db.default_structure 
	# Environment değişkenleri ayarla
	env = Environment(root=database)

	# completer fonlsiyonu ayarla (yine neden bilmiyorum)
	readline.set_completer(completer_wrapper(env))
	return parser(env, input_text)


