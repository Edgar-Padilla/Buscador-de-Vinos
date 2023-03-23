import json
import unicodedata
from BTrees.OOBTree import OOBTree


def diccionario_a_arbol_b(diccionario, arbol_b):
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            sub_arbol_b = OOBTree()
            diccionario_a_arbol_b(valor, sub_arbol_b)
            arbol_b[clave] = sub_arbol_b
        else:
            arbol_b[clave] = valor

# Cargar archivos
#Corpus
doc = []
with open('search/motor/files/corpusChistes.txt', 'r') as f:
    for linea in f:
        # Leer por linea
        chiste = linea.split('|')[1].strip()
        doc.append(chiste)
#Vocabulario
vocabulario = set()
with open('search/motor/files/vocabulario.txt', "r") as f:
    for linea in f:
        vocabulario.add(linea.strip())
#Vocabulario inverso
invVocabulario = set()
with open('search/motor/files/invVocabulario.txt', "r") as f:
    for linea in f:
        invVocabulario.add(linea.strip())
#Posting list
posList = {}
with open('search/motor/files/posList.txt', "r") as archivo:
    posList = json.load(archivo)
#Sinonimos
dicSinonimos = {}
with open('search/motor/files/sinonimos.txt', 'r') as file:
    line = file.readline()
    while line:
        key, values = line.strip().split(':')
        key=key.strip()
        values_list = [v.strip() for v in values.split(',')]
        values_list = [unicodedata.normalize('NFD', v).encode('ascii', 'ignore').decode('utf-8') for v in values_list]
        dicSinonimos[key] = values_list
        line = file.readline()
#Diccionario expandido por sinonimos
sinoExpanDic = {}
with open('search/motor/files/dicSino.txt', 'r') as archivo:
    sinoExpanDic = json.load(archivo)
#diccionario de bigramas
bigramDic = {}
with open('search/motor/files/bigramaDic.txt', 'r') as archivo:
    bigramDic = json.load(archivo)
#Diccionario arbol B
dicTree={}
with open('search/motor/files/dicTree.txt', 'r') as archivo:
    dicTree = json.load(archivo)
tree=OOBTree()
diccionario_a_arbol_b(dicTree, tree)
# Función recursiva para convertir un diccionario en un árbol B
#dicionario arbol B de palabras invertidas
invDicTree={}
with open('search/motor/files/invDicTree.txt', 'r') as archivo:
    invDicTree = json.load(archivo)
invTree=OOBTree()
diccionario_a_arbol_b(invDicTree, invTree)
#documentos del indice invertido posicional
totalDocuments=[]
with open('search/motor/files/documentos.txt', 'r') as f:
        totalDocuments = json.load(f)
totalDocuments = set(totalDocuments)
with open('search/motor/files/frecPosList.txt', 'r') as f:
        frecPosList = json.load(f)