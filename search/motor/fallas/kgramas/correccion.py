import leven
import json
class correcion:
    def __init__(self):
        pass
    #Guardar el archivo de texto en una lista
    def extraerCorpus(self,path):
        with open(path, "r") as file:
            content = file.read()
            f = content.splitlines()
        return f
    #agrega al inicio y fin de una palabra el simbolo $
    def convertirPalabra(self,palabra):
        return "$"+palabra+"$"
    #Lee un diccionario de un archivo txt y lo guarda en un diccionario en python
    def extraerDic(self,path):
        with open(path, "r") as archivo:
            mi_diccionario = json.load(archivo)
        return mi_diccionario
    #Extrae los bigramas de una palabra
    def extraerBigramas(self,palabra):
        res=[]
        for i in range(len(palabra)-1):
            bigrama = palabra[i]+ palabra[i+1]
            res.append(bigrama)
        return res
    #Crea un diccionario solo con los bigramas buscados
    def extraerDicBigramas(self,bigramas,dic_bigramas):
        res={}
        for bigrama in bigramas:
            res[bigrama]=dic_bigramas[bigrama]
        return res
    #Crea un conjunto de palabras de un diccionario de bigramas
    def extraerPalabras(self,dic):
        res=set()
        for key in dic:
            for item in dic[key]:
                res.add(item)
        return res
    #mide la distancia de leven* entre una palabra y un conjunto de palabras y crea
    #un diccionario cuayas claves son la distancia de levin* y los items las palabras
    #que tienen esta distancia
    def listLeven(self,palabra1,list_palabras):
        dic={}
        for palabra2 in list_palabras:
            dis=leven.distance(palabra1,palabra2)
            if dis not in dic:
                dic[dis]=[]
            dic[dis].append(palabra2)
        res={}
        #ordenar por distancia de menor a mayor
        for key in sorted(dic.keys()):
            res[key]=dic[key]
        return res
    def main(self):
        #Obtener los datos necesarios
        doc=self.extraerCorpus("search/motor/files/corpusChistes.txt")
        posting_list=self.extraerDic("search/motor/files/posList.txt")
        bigram_dic=self.extraerDic("search/motor/files/bigramaDic.txt")
        """
        #ingresar palabra y obtener sus bigramas
        palabra=input("ingrese la palabra:\n")
        palabra_peso=self.convertirPalabra(palabra)
        #Obtener el conjunto de palabras con la distancia minima de levem*
        list_bigramas=self.extraerBigramas(palabra_peso)
        dic_list_bigramas=self.extraerDicBigramas(list_bigramas, bigram_dic)
        set_palabras=sorted(self.extraerPalabras(dic_list_bigramas))
        dic_lev=self.listLeven(palabra_peso,set_palabras)
        min_clave=min(dic_lev.keys())
        #Imprsion de documentos
        if min_clave==0:
            for key in posting_list[palabra_peso]:
                print(doc[int(key)-1])
        else:
            print("Tal vez quiso decir:")
            print([palabra.replace("$","") for palabra in dic_lev[min_clave]])
            for palabra in dic_lev[min_clave]:
                print('\n')
                print("La palabra ", palabra.replace("$",""), " aparece en los siguientes documentos:")
                palabra=palabra.replace("$","")
                for key in posting_list[palabra]:
                    print(doc[int(key)-1])
        """

run=correcion()
run.main()