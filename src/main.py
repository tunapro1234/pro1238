import readline
import json


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
# keyword bellirlemeliyim
#	reconfigure
#	help
# 
#	add 
#	data
#	
#	remove
#	data
# 
#






def parser():
	input(">>> ")


def completer(text, state):
	words = readline.get_line_buffer().split(" ")
	vocab = []

	if len(words) == 1:
		vocab = ["tuna", "aslı", "memedali"]
	elif len(words) == 2:
		if words[0] == "tuna":
			vocab = ["gül", "akkaya", "akyüz"]
		elif words[0] == "aslı":
			vocab = ["özler", "özlemez"]
		elif words[0] == "memedali":
			vocab = ["uçar", "uçamaz", "balon"]
		
	results = [i for i in vocab if i.startswith(text)] + [None]
	return results[state]
	
	
def _main():
	readline.parse_and_bind("tab: complete")
	readline.set_completer(completer)
	parser()






