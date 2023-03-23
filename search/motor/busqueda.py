from search.motor.fallas.kgramas.leven import distance
import math
class busqueda:
#-------------Metodos--------------------------------------------------------------
    #Cargar archivos
    def __init__(self,frecPosList,vocabulario, doc, posList, dicSinonimos, sinoExpanDic, bigramDic):
        self.vocabulario=vocabulario
        self.bigramDic=bigramDic
        self.doc=doc
        self.posList=posList
        self.dicSinonimos=dicSinonimos
        self.sinoExpanDic=sinoExpanDic
        self.frecPosList=frecPosList
#Operador near
    def near_operator(self,p1, p2, k):
        answer = []
        key1=set(p1.keys())
        key2=set(p2.keys())
        inter=key1.intersection(key2)
        for key in inter:
            pos1=p1[key]
            pos2=p2[key]
            index1=0
            while index1<len(pos1):
                index2=0
                while index2<len(pos2):
                    if pos1[index1]<pos2[index2]:
                        if (pos2[index2]-pos1[index1])<=k:
                            answer.append(key)
                    index2=index2+1
                index1=index1+1
        return answer
#Correccion gramatical por bigramas
    #Convertir la palabra a  $palabra$
    def convertirPalabra(self,palabra):
        return "$"+palabra+"$"
    #Obtner lista de bigramas de $palabra$
    def crearListaBigramas(self,palabra):
        res=[]
        for i in range(len(palabra)-1):
            bigrama = palabra[i]+ palabra[i+1]
            res.append(bigrama)
        return res
    #Obtener diccionario de bigramas
    def extraerDicBigramas(self,bigramas):
        res={}
        for bigrama in bigramas:
            if bigrama in self.bigramDic:
                res[bigrama]=self.bigramDic[bigrama]
        return res
    #Extraer lista de palabras del diccionario de bigramas
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
            dis=distance(palabra1,palabra2)
            if dis not in dic:
                dic[dis]=[]
            dic[dis].append(palabra2)
        res={}
        #ordenar por distancia de menor a mayor
        for key in sorted(dic.keys()):
            res[key]=dic[key]
        return res
#-----------Buscador----------------------------------------------------
    def buscarPalabra(self, palabra):
        res=[]
        sinonimos=[]
        correccion=[]
        if palabra!="":
            palabra=palabra.lower()
            #Busqueda por sinonimos
            #Busqueda normal (si no existen sinonimos)
            if palabra in self.posList:
                dic_res=self.posList[palabra]
                for key in dic_res:
                    res_doc=self.doc[int(key)]
                    res.append((str(key), str(dic_res[key]), res_doc))
            elif palabra in self.dicSinonimos and len(self.dicSinonimos[palabra])>1:
                dic_res=self.sinoExpanDic[palabra]
                for sinonimo in self.dicSinonimos[palabra]:
                    if sinonimo in self.posList:
                        sinonimos.append(sinonimo)
                for key in dic_res:
                    res_doc=self.doc[int(key)-1]
                    res.append((str(int(key)-1), str(dic_res[key]), res_doc))
            #Correccion ortográfica por bigramas
            else:
                palabra_peso=self.convertirPalabra(palabra)
                list_bigramas=self.crearListaBigramas(palabra_peso)
                dic_list_bigramas=self.extraerDicBigramas(list_bigramas)
                set_palabras=sorted(self.extraerPalabras(dic_list_bigramas))
                listaLev=self.listLeven(palabra_peso,set_palabras)
                if listaLev:
                    min_clave=min(listaLev.keys())
                    for palabra1 in listaLev[min_clave]:
                        aux=palabra1.replace("$","")
                        correccion.append(aux)
                        dic_res=self.posList[aux]
                        for key in self.posList[aux]:
                            res_doc=self.doc[int(key)]
                            res.append((str(int(key)-1), str(dic_res[key]), res_doc))
        scores={}
        for tupla in res:
            if tupla[0] not in scores:
                scores[tupla[0]]=0
        numDoc=len(self.posList)
        if  palabra in self.posList:
            tfq=1
            dfp=self.frecPosList[palabra]['df']
            wq=tfq*math.log10(numDoc/dfp)
            for tupla in res:
                if tupla[0] in self.posList[palabra]:
                    tfd=len(self.posList[palabra][tupla[0]])
                    wd=tfd*math.log10(numDoc/dfp)
                    scores[tupla[0]]+=wd*wq
        scoresln=len(scores)
        for doc in scores:
            scores[doc]=scores[doc]/scoresln
        resOrdenada = sorted(res, key=lambda x: scores[x[0]], reverse=True)
        return resOrdenada, sinonimos, correccion
    def buscarFrase(self, ph):
        sinonimos=[]
        words=ph.split()
        keys=[]
        correccion=[]
        res=[]
        if ph[0]==ph[len(ph)-1]=='"':
            words=[word.replace('"',"") for word in words]
            for i in range(len(words)-1):
                keys.append(self.near_operator(self.posList[words[i]],self.posList[words[i+1]],1))
            set_keys=[set(lis) for lis in keys]
            if len(set_keys)>1:
                res_near=list(set_keys[0].intersection(*set_keys[1:]))
            else:
                res_near=keys[0]
            for key in res_near:
                res_doc=self.doc[int(key)]
                res.append((str(key),'', res_doc))
        else:
            for palabra in words:
                if palabra in self.posList:
                    dic_res=self.posList[palabra]
                    for key in dic_res:
                        res_doc=self.doc[int(key)]
                        res.append((str(key), str(dic_res[key]), res_doc))
        scores={}
        for tupla in res:
            if tupla[0] not in scores:
                scores[tupla[0]]=0
        numDoc=len(self.posList)
        for palabra in words:
            if  palabra in self.posList:
                tfq=words.count(palabra)
                dfp=self.frecPosList[palabra]['df']
                wq=tfq*math.log10(numDoc/dfp)
                if palabra in self.posList:
                    for tupla in res:
                            tfd=len(self.posList[palabra][tupla[0]])
                            wd=tfd*math.log10(numDoc/dfp)
                            scores[tupla[0]]+=wd*wq
        scoresln=len(scores)
        for doc in scores:
            scores[doc]=scores[doc]/scoresln
        resOrdenada = sorted(res, key=lambda x: scores[x[0]], reverse=True)

        return resOrdenada, sinonimos, correccion

    def identificar(self, entrada):
        aux=entrada.split()
        if len(aux)>1:
            return self.buscarFrase(entrada)
        else:
            return self.buscarPalabra(entrada)