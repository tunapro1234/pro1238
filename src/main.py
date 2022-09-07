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
# "" error parsing
# üst foldera erişemiyoruz aa
# cd . && cd ..
# ls /folder/subject
# cd to subject check
# tab tamamlama / koyma
# environment
# ls -l
#
# TODO
# var olan databasei yok edecek her fonksiyona check konulmalı
# ls -lr
# pwd
#
# DATABASE:
#	check_properties()
#	_add_entry fonksiyonları
#
# excel export
# passing sub_elements to functions??


class Environment:
	# programla ilgili genel global 
	# değişkenlerin tutulacağı değişken classı
	def __init__(self, root=None, curdir=None):
		self.root = root
		self.curdir = root if curdir is None else None


def parser(env, input_text):
	# İllgal bir kaçış ehe
	if input_text in ["q", "quit"]: quit()

	# şimdilik sadece bu operatörü test için geliştiriyorum
	if "&&" in input_text:
		for command in input_text.split("&&"):
			if parser(env, command) == False: return False
		return True

	# boşluklardan böl argüman olarak yedir
	argv = [i for i in input_text.split(" ") if i != ""]

	# eğer "" girilirse boşver
	if len(argv) == 0: return True
	# Eğer çalıştırılmaya çalışılan fonksiyon bizim 
	# yazdığımız fonksiyonlardan değilse kabul etme
	elif argv[0] not in glb.keywords:
		print(f"command not found: {input_text}")
		return False
	# fonksiyonu çağır
	return eval(f"cmd._{argv[0]}(env, argv)")


def check_if_path(env, text):
	# Ufak bir wrapper fonksiyon
	if env.curdir is None or env.root is None: return False
	# Eğer verilen string / ile başlıyorsa kullanacağımız
	# folderı root folder olarak ayarla
	base = env.root if text.startswith("/") else env.curdir
	# Ana fonksiyon Folder.find_by_path
	# eğer ana fonksiyon False veriyorsa biz de False veriyoruz
	# ama eğer ana fonksiyon obje döndürüyorsa path parsing
	# işlemi başarılı olmuş demektir
	return False if base.find_by_path(text) == False else True


def complete_path(env, word):
	# Eğer herhangi bir database bulunamadıysa salla
	if env.curdir is None or env.root is None: return []
	# Eğer / ile başlıyorsa root klasörden aramaya başla
	base = env.root if word.startswith("/") else env.curdir
	# aynı linuxtaki gibi

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
			vocab = glb.commands

		if words[0] == "add":
			if len(words) == 2:
				vocab = glb.command_args
			elif len(words) == 3:
				vocab = complete_path(env, words[2])

		if env.curdir is not None and words[0] in ["ls", "rm", "cd"]:
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
	
	# Eğer database okuyabilmişsek yolla bakalım
	database = db.read_database()
	if database == False:
		print(f"{glb.info} No database found...")
		database = None
	else:
		# database okunmuşsa gerekli ayarlamaları yap
		db.meet_your_parents(database)

	# environment variableları initleniyor
	env = Environment(root=database)

	while True:
		try:
			# completer fonksiyonu ayarla
			readline.set_completer(completer_wrapper(env))
			# eğer database okunmuşsa içinde 
			# bulunduğumuz klasörü prompta da yazdır
			prompt = f"tunapro1238]{glb.clean} >> " if env.curdir is None \
					else f"tunapro1238 {env.curdir.name}]{glb.clean} >> "
			# kullanıcının girdiği inputu parsera yolla
			rv = parser(env, input(prompt))

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


