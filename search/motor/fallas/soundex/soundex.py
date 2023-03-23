import json
import re
class soundex:
    def __init__(self):
        with open("search/motor/files/vocabulario2.txt","r", encoding="utf-8") as f:
            self.vocabulario=json.load(f)
    def soundexCode(self,word):
        if len(word)==1:
            return word.upper()+'000'
        # Convertir a mayúsculas
        word = word.upper()
        # Asignar el primer carácter de la palabra a la variable soundex_code
        soundex_code = word[0]
        # Diccionario de equivalencias de letras a números
        letter_to_number = {
            'B': '1', 'F': '1', 'P': '1', 'V': '1',
            'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
            'D': '3', 'T': '3',
            'L': '4',
            'M': '5', 'N': '5', 'Ñ': '5',
            'R': '6'
        }
        # Cambiar letras a números según el diccionario y ceros para las letras especificadas
        digits = ''
        for letter in word[1:]:
            if letter in letter_to_number:
                digit = letter_to_number[letter]
                digits += digit
            else:
                digits += '0'
        # Eliminar pares consecutivos de dígitos
        deduped_digits = digits[0]
        for digit in digits[1:]:
            if digit != deduped_digits[-1:]:
                deduped_digits += digit
        # Eliminar ceros y completar la cadena de dígitos con ceros hasta llegar a una longitud de 3 dígitos
        digits = deduped_digits.replace('0', '')
        digits += '000'
        digits = digits[:3]
        # Combinar el código Soundex y los dígitos y devolver las primeras cuatro posiciones
        return soundex_code + digits
    def isSpanishWord(self,word):
        # Expresión regular para encontrar todas las letras en la palabra
        regex = re.compile('[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+')
        # Encontrar todas las letras en la palabra y unirlas
        letters = ''.join(regex.findall(word))
        # Comparar la longitud de la palabra original con la longitud de las letras encontradas
        return len(word) == len(letters)
    def main(self):
        vocabularioEsp=list(filter(self.isSpanishWord, self.vocabulario))
        soundexVocabulario={}
        for palabra in vocabularioEsp:
            codigo=self.soundexCode(palabra)
            soundexVocabulario[palabra]=codigo
        soundexInverVocabulario={}
        for key in soundexVocabulario:
            if soundexVocabulario[key] not in soundexInverVocabulario:
                soundexInverVocabulario[soundexVocabulario[key]]=[]
            soundexInverVocabulario[soundexVocabulario[key]].append(key)
        with open("search/motor/files/soundexVocabulario.txt","w") as f:
                json.dump(soundexVocabulario,f,ensure_ascii=False)
        with open("search/motor/files/soundexInverVocabulario.txt","w") as f:
                json.dump(soundexInverVocabulario,f,ensure_ascii=False)
run=soundex()
run.main()