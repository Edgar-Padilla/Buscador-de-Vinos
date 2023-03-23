import re
from search.motor.logica.logic import operators

class busquedaAvanzada:
    def __init__(self,vocabulario, doc, posList, dicSinonimos, sinoExpanDic, bigramDic, tree, invTree, totalDocuments):
        self.vocabulario=vocabulario
        self.bigramDic=bigramDic
        self.doc=doc
        self.posList=posList
        self.dicSinonimos=dicSinonimos
        self.sinoExpanDic=sinoExpanDic
        self.tree=tree
        self.invTree=invTree
        self.totalDocuments=totalDocuments
#---------------------------Consulta comodin----------------------------------------------------------------------
    #Buscar  las palabras con el prefijo dado en el arbol
    def buscarPalabrasPrefijo(self, prefijo, nodo_actual):
        # Iterar a través de cada letra del prefijo y seguir la rama correspondiente en el árbol
        for letra in prefijo:
            if letra in nodo_actual:
                nodo_actual = nodo_actual[letra]
            else:
                return []
        # Realizar una búsqueda en profundidad para encontrar todas las palabras que comienzan con el prefijo
        resultados = []
        def buscarPalabras(nodo):
            if '' in nodo:
                resultados.append(nodo[''])
            for letra in nodo:
                if letra != '':
                    buscarPalabras(nodo[letra])
        buscarPalabras(nodo_actual)
        return resultados
    def reverseVocab(self,vocab):
        inverse=[]
        for word in vocab:
            inverse.append(word[::-1])
        return inverse
    def buscarPalabraComodin(self,entrada):
        ln=len(entrada)
        #Buscar que clase de comodin se ocupa y obtener resultados
        if entrada[ln-1]=="*":
            prefix=entrada.replace("*","")
            res=self.buscarPalabrasPrefijo(prefix,self.tree)
        elif entrada[0]=="*":
            sufix=entrada.replace("*","")
            sufix=sufix[::-1]
            res=self.reverse_vocab(self.buscarPalabrasPrefijo(sufix,self.invTree))
        else:
            query=entrada.split("*")
            if len(query)==2:
                prefix=query[0]
                sufix=query[1]
                sufix=sufix[::-1]
                res1=self.buscarPalabrasPrefijo(prefix,self.tree)
                res2=self.reverseVocab(self.buscarPalabrasPrefijo(sufix,self.invTree))
                res=list(set(res1).intersection(set(res2)))
        return res
    #consulta comodin
    def consultaComodin(self, entrada):
        res=[]
        sinonimos=[]
        correccion=[]
        palabras=self.buscarPalabraComodin(entrada)
        for palabra in palabras:
                correccion.append(palabra)
                dic_res=self.posList[palabra]
                for key in dic_res:
                    res_doc=self.doc[int(key)]
                    res.append((str(key), str(dic_res[key]), res_doc))
        return res, sinonimos, correccion
#-------------------------------Consulta logica-----------------------------------------------

    def consultaLogica(self, entrada):
        res=[]
        sinonimos=[]
        correccion=[]
        entrada=entrada.split()
        logic=operators()
        keys=set()
        if entrada[1]=="AND":
            if entrada[0] in self.posList and entrada[2] in self.posList:
                keys=logic.andOperator(self.posList[entrada[0]], self.posList[entrada[2]])
        elif entrada[1]=="OR":
            if entrada[0] in self.posList and entrada[2] in self.posList:
                keys=logic.orOperator(self.posList[entrada[0]], self.posList[entrada[2]])
        elif entrada[0]=="NOT":
            if entrada[1] in self.posList:
                keys=logic.notOperator(self.posList[entrada[1]], len(self.totalDocuments))
        elif entrada[1]=="NAND":
            if entrada[0] in self.posList and entrada[2] in self.posList:
                keys=logic.nandOperator(self.posList[entrada[0]], self.posList[entrada[2]],len(self.totalDocuments))
        if keys:
            for key in keys:
                res_doc=self.doc[int(key)]
                res.append((str(key),'', res_doc))

        return res, sinonimos, correccion

    def buscador(self, entrada):
        expresion_regular = r"[*]"
        if re.search(expresion_regular, entrada):
            print("busqueda comodin")
            return self.consultaComodin(entrada)
        else:
            print("busqueda logica")
            return self.consultaLogica(entrada)