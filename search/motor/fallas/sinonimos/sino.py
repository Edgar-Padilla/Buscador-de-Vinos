import string
import unicodedata
import json
class exp_sin:
    def __init__(self):
        pass
    def sino_dic(self, path):
        dictionary = {}
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                key, values = line.strip().split(':')
                key=key.strip()
                values_list = [v.strip() for v in values.split(',')]
                values_list = [unicodedata.normalize('NFD', v).encode('ascii', 'ignore').decode('utf-8') for v in values_list]
                dictionary[key] = values_list
                line = file.readline()
        return dictionary
    def vocabulary(self,path):
        vocab = []
        with open(path, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                palabra = linea.split(':')[0]
                vocab.append(palabra)
        vocab=list(set(vocab))
        return vocab
    def txt_to_string(self, path):
        doc = []
        with open(path, 'r') as f:
            for linea in f:
                chiste = linea.split('|')[1].strip()
                translator = str.maketrans(string.punctuation + "¿¡", ' ' * (len(string.punctuation) + 2))
                chiste = chiste.translate(translator)
                palabras=chiste.split()
                chiste=" ".join(palabras)
                doc.append(chiste)
        return doc
    def inverted_index_posicional(self, documents,voc):
        inverted_index = {}
        for palabra in voc:
            inverted_index[palabra]={}
        for i in range(len(documents)):
            document = documents[i]
            for j in range(len(document.split())):
                term = document.split()[j]
                if term not in inverted_index:
                    inverted_index[term] = {}
                if str(i + 1) not in inverted_index[term]:
                    inverted_index[term][str(i + 1)] = []
                inverted_index[term][str(i + 1)].append(j)
        return inverted_index
    def expand_index(self,inverted_index, synonyms_dic):
        expanded_dict = {}
        for word in inverted_index.keys():
            if word in synonyms_dic:
                synonyms=synonyms_dic[word]
                aux1=inverted_index[word]
                merge={}
                for synonym in synonyms:
                    if synonym in inverted_index and synonym!=word:
                        aux2=inverted_index[synonym]
                        for key in aux1:
                            if key in aux2:
                                merge[key]=list(set(aux1[key]+aux2[key]))
                            else:
                                merge[key]=aux1[key]
                        for key in aux2:
                            if key not in merge:
                                merge[key]=aux2[key]
                for key in merge:
                    merge[key].sort()
                expanded_dict[word]=merge
        return expanded_dict



    def main(self):
        sinonimos=self.sino_dic("search/motor/files/sinonimos.txt")
        vocab=self.vocabulary("search/motor/files/drae1.txt")
        doc=self.txt_to_string("search/motor/files/corpusChistes.txt")
        pos=self.inverted_index_posicional(doc,vocab)
        expand=self.expand_index(pos,sinonimos)
        with open("search/motor/files/prueba.txt","w") as f:
            json.dump(expand,f,ensure_ascii=False)



run=exp_sin()
run.main()