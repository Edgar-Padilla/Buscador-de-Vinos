import phonetics
import json
import re
from unidecode import unidecode

class soundex:
    def __init__(self):
        with open("search/motor/files/vocabulario2.txt","r", encoding="utf-8") as f:
            self.vocabulario=json.load(f)
    def isSpanishWord(self,word):
        # Expresión regular para encontrar todas las letras en la palabra
        regex = re.compile('[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+')
        # Encontrar todas las letras en la palabra y unirlas
        letters = ''.join(regex.findall(word))
        # Comparar la longitud de la palabra original con la longitud de las letras encontradas
        return len(word) == len(letters)
    def main(self):
        vocabularioEsp=list(filter(self.isSpanishWord, self.vocabulario))
        nuevoVoc=[]
        for palabra in vocabularioEsp:
            nuevaPalabra=unidecode(palabra)
            nuevoVoc.append(nuevaPalabra)
        soundexVocabulario={}
        for palabra in nuevoVoc:
            codigo=phonetics.soundex(palabra)
            soundexVocabulario[palabra]=codigo
        soundexInverVocabulario={}
        for key in soundexVocabulario:
            if soundexVocabulario[key] not in soundexInverVocabulario:
                soundexInverVocabulario[soundexVocabulario[key]]=[]
            soundexInverVocabulario[soundexVocabulario[key]].append(key)
        with open("search/motor/files/soundexVocabulario2.txt","w") as f:
                json.dump(soundexVocabulario,f,ensure_ascii=False)
        with open("search/motor/files/soundexInverVocabulario2.txt","w") as f:
                json.dump(soundexInverVocabulario,f,ensure_ascii=False)
run=soundex()
run.main()