import res.globals as glob
import src.database as db
import readline

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


 
# TODO
# posix path kullan
# write_database ve read_database fonksiyonlarına exception handling geliştirmeleri
# keywordlerin baştan ayarlanması
# write_database fonksiyonunu classlara aktar
# _add_entry fonksiyonları
# excel export



def _help():
	for key, value in glob.keywords_help.items():
		print(f"[{key}]: {value}")
	return True

def _reconfigure(): return True

def _fetch(): return True

def _init(): return db.write_database()


def _list_subject(): return True

def _list_folder(): return db.Folder.read(db.default_path)

def _list_data(): return True


def _add_subject(): return True

def _add_subject(): return True

def _add_data(): return True


def _remove_subject(): return True

def _remove_subject(): return True

def _remove_data(): return True


def check_input(text, keywords):
	if text == "": return False
	for keyword in keywords:
		text = text.replace(keyword, "")
	return not bool(len(text.strip()))

def parser(text):
	if check_input(text, glob.keywords):
		text = " ".join([i for i in text.split(" ") if i != ""]).strip().replace(" ", "_")
		return eval(f"_{text}()")
	return f"No keyword found: {text}"

def completer(text, state):
	words = readline.get_line_buffer().split(" ")
	vocab = []

	if len(words) == 1:
		vocab = ["help", "reconfigure", "fetch", "init", "list", "add", "remove"]

	elif len(words) == 2 and words[0] in ["list", "add", "remove"]:
		vocab = ["subject", "folder", "data"]
		
	results = [i for i in vocab if i.startswith(text)] + [None]
	return results[state]
	
	
def _main():
	readline.parse_and_bind("tab: complete")
	readline.set_completer(completer)

	try: print(parser(input(">>> ")))
	except KeyboardInterrupt: print()





