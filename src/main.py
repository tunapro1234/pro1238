import readline
import json


"""
Merhabaaa...
sınav senemdeyim ve sınava yaklaşık 55 gün kaldı
    ben de kafayı yemeye başladım

ne yapacağıma dair planlama yapacağım

bayadır yazılım yapmıyorum

database sistemi klasör ve json bazlı olacak her bir klasörün kendine ait 
properties.json tarzında bir dosyaası olacak. properties.json dosyasının içinde 
tam olarak ne olacağını bilmiyorum, ama versiyon kontrolü çok önemli.

Versiyon kontrolü için aklımda ufak bir fikir var. Her kod yenilediğimde versiyon
değiştirmekle uğraşmamak için dosyaların hashini aldırmayı planlıyorum.

dosya ayrımı ders bazında yapılacak her bir ders json dosyasının içinde de tarih
bazında sıralama yapılacak.

keyword bellirlemeliyim
    reconfigure
    add 
        data

    remove
        data





"""


def parser():
    readline.set_completer(completer_generator("tuna", "pro", "test"))
    input(">>> ")
    readline.set_completer(completer_generator("deneme", "aaaaaa", "foho"))
    input(">>> ")
    

def completer_generator(*args):
    def complete(text, state):
        results = [i for i in args if i.startswith(text)] + [None]     
        return results[state]
    return complete 
    
    
def _main():
    readline.parse_and_bind("tab: complete")
    parser()
