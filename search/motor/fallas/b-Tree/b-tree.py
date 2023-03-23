from BTrees.OOBTree import OOBTree
import json
class BTplus:
    def __init__(self):
        pass
    #Importar vocabulario
    def import_vocab(self, path):
        vocabulario=[]
        with open(path,"r") as f:
            for line in f:
                words=line.strip().split()
                for word in words:
                    vocabulario.append(word)
        return vocabulario
    #Invertir Vocabulario
    def reverse_vocab(self,vocab):
        inverse=[]
        for word in vocab:
            inverse.append(word[::-1])
        return inverse
    #Agregar palabra al árbol
    def agregar_palabra(self, palabra, arbol):
        nodo_actual = arbol
        for letra in palabra:
            if letra not in nodo_actual:
                nodo_actual[letra] = {}
            nodo_actual = nodo_actual[letra]
        nodo_actual[''] = palabra
    #Crear arbol
    def build_tree(self,arbol,vocab):
        for palabra in vocab:
            self.agregar_palabra(palabra, arbol)
    #Buscar  las palabras con el prefijo dado en el arbol
    def buscar_palabras_con_prefijo(self, prefijo, nodo_actual):
        # Iterar a través de cada letra del prefijo y seguir la rama correspondiente en el árbol
        for letra in prefijo:
            if letra in nodo_actual:
                nodo_actual = nodo_actual[letra]
            else:
                return []
        # Realizar una búsqueda en profundidad para encontrar todas las palabras que comienzan con el prefijo
        resultados = []
        def buscar_palabras(nodo):
            if '' in nodo:
                resultados.append(nodo[''])
            for letra in nodo:
                if letra != '':
                    buscar_palabras(nodo[letra])
        buscar_palabras(nodo_actual)
        return resultados
    #Imprimir arbol
    def imprimir_arbol(self,nodo_actual, nivel=0):
        for letra, hijo in nodo_actual.items():
            print(' ' * nivel, letra)
            if isinstance(hijo, str):
                print(' ' * (nivel + 1), hijo)
            else:
                self.imprimir_arbol(hijo, nivel=nivel+1)

    def main(self):
        #Cargar vocabulario
        vocabulario=self.import_vocab("search/motor/files/vocabulario.txt")
        #invertir vocabulario
        invVocabulario=self.reverse_vocab(vocabulario)
        #Crear arbol normal
        tree = OOBTree()
        self.build_tree(tree,vocabulario)
        #crear arbol con las palabras en orden inverso
        invTree=OOBTree()
        self.build_tree(invTree, invVocabulario)
        dicTree=dict(tree.items())
        invDicTree=dict(invTree.items())
        with open("search/motor/files/dicTree.txt","w") as f:
            json.dump(dicTree,f,ensure_ascii=False)
        with open("search/motor/files/invDicTree.txt","w") as f:
            json.dump(invDicTree,f,ensure_ascii=False)
        with open("search/motor/files/inVocabulario.txt","w") as f:
            for palabra in invVocabulario:
                f.write(palabra+"\n")
run=BTplus()
run.main()