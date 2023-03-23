import string
import json

class bigram:
    def __init__(self):
        pass
    def leer_vocabulario(self, path):
        vocabulario=set()
        with open(path,"r") as f:
            for linea in f:
                vocabulario.add(linea.strip())
        return vocabulario
    def txt_to_string(self, path):
        doc = []
        with open(path, 'r') as f:
            for linea in f:
                chiste = linea.split('|')[1].strip()
                translator = str.maketrans(string.punctuation + "¿¡", ' ' * (len(string.punctuation) + 2))
                chiste = chiste.translate(translator)
                palabras=chiste.split()
                palabras=["$"+palabra+"$" for palabra in palabras]
                chiste=" ".join(palabras)
                doc.append(chiste)
        return doc


    def posting_list(self, vocabulario, corpus):
        posting_lists={}
        for  i, linea in enumerate(corpus):
            palabras=linea.strip().split()
            for j, palabra in enumerate(palabras):
                if palabra in vocabulario:
                    if palabra not in posting_lists:
                        posting_lists[palabra]={}
                    if str(i) not in posting_lists[palabra]:
                        posting_lists[palabra][str(i)]=[]
                    posting_lists[palabra][str(i)].append(j)
        return posting_lists

    def main(self):
        vocabulario=self.leer_vocabulario("dollar_vocabulario.txt")
        corpus=self.txt_to_string("corpusChistes.txt")
        bi_post_index=self.posting_list(vocabulario,corpus)
        with open("posList.txt","w") as f:
            json.dump(bi_post_index,f,ensure_ascii=False)

run=bigram()
run.main()