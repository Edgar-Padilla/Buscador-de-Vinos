import string
import json

class bigram:
    def __init__(self):
        pass
    def extraerPalabras(self,path):
        with open(path, "r") as archivo:
            mi_diccionario = json.load(archivo)
        res=set()
        for key in mi_diccionario:
            res.add(key)
        return res

    def bigramDic(self, palabras_set):
        bigramaDicc={}
        for palabra  in palabras_set:
            for j in range(len(palabra)-1):
                bigrama = palabra[j]+ palabra[j+1]
                if bigrama not in bigramaDicc:
                    bigramaDicc[bigrama]=[]
                bigramaDicc[bigrama].append(palabra)
        return bigramaDicc

    def main(self):
        palabrasSet=self.extraerPalabras("search/motor/files/posList.txt")
        bigramaDic=self.bigramDic(palabrasSet)
        with open("search/motor/files/dicNormalBigram.txt","w") as f:
            json.dump(bigramaDic,f,ensure_ascii=False)

run=bigram()
run.main()