import re
import json
class correcionGramatical:
    def __init__(self):
        self.doc=[]
        with open("search/motor/files/corpusChistes.txt", "r") as f:
            for line in f:
                self.doc.append(line)
    def preprocesamiento(self):
        self.docPreproces=[]
        for line in self.doc:
            #me quedo con la parte derecha del pip
            separar=line.split("|")
            new_line=separar[1].strip()
            #eliminar numeros
            new_line=re.sub(r'\d+',' ',new_line)
            new_line=new_line.split()
            new_line=' '.join(new_line)
            #eliminar signos de puntuacion
            new_line = re.sub(r'[^\w\s]', ' ',new_line)
            new_line=new_line.split()
            new_line=' '.join(new_line)
            self.docPreproces.append(new_line)
    def tokenizacion(self):
        self.tokens=set()
        for line in self.docPreproces:
            tokensLine=line.split()
            for token in tokensLine:
                self.tokens.add(token)
        self.tokens=list(self.tokens)
    def obtenerBigramas(self):
        self.bigramas=[]
        for line in self.docPreproces:
            tokensLine=line.split()
            for i in range(len(tokensLine)-1):
                bigrama=tokensLine[i]+" "+tokensLine[i+1]
                self.bigramas.append(bigrama)
    def modeloMarkov(self):
        # Calcular la matriz de transición
        self.matrizTransicion = {}
        for bigrama in self.bigramas:
            bg=bigrama.split()
            if bg[0] in self.matrizTransicion:
                self.matrizTransicion[bg[0]][bg[1]] = self.matrizTransicion[bg[0]].get(bg[1], 0) + 1
            else:
                self.matrizTransicion[bg[0]] = {bg[1]: 1}
        # Convertir el recuento en probabilidades
        for word, next_words in self.matrizTransicion.items():
            total = sum(next_words.values())
            for w in next_words:
                next_words[w] /= total
    def main(self):
        self.preprocesamiento()
        self.tokenizacion()
        self.obtenerBigramas()
        self.modeloMarkov()
        with open('search/motor/files/matrizTransicion.txt', 'w') as archivo:
            json.dump(self.matrizTransicion, archivo, ensure_ascii=False)
        with open('search/motor/files/bigramas.txt', 'w') as archivo:
            json.dump(self.bigramas, archivo, ensure_ascii=False)

run=correcionGramatical()
run.main()