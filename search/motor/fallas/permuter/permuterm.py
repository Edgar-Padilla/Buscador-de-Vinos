
import json
class Permuterm:
    def __init__(self):
        self.tree={}
        self.vocabulario=set()
        with open("search/motor/files/vocabulario.txt","r") as f:
            for linea in f:
                self.vocabulario.add(linea.strip())
    def build_permuterm(self):
        for term in self.vocabulario:
            if term not in self.tree:
                self.tree[term]={}
            newTerm=term+'$'
            permutaciones=[]
            for i in range(len(newTerm)):
                permutaciones.append(newTerm[i:]+newTerm[:i])
            for permutacion in permutaciones:
                if permutacion not in self.tree[term]:
                    self.tree[term][permutacion]={}
                self.tree[term][permutacion]=""

    def main(self):
        self.build_permuterm()
        with open("search/motor/files/prueba.txt","w") as f:
            json.dump(self.tree,f,ensure_ascii=False)
run=Permuterm()
run.main()