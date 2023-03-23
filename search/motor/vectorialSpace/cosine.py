import math
class vsm:
    def __init__(self):
        pass
    def cosineScore(self, query,posList, numDoc, k):
        scores={}
        palabras=query.split()
        for palabra in palabras:
            tfq=palabras.count(palabra)
            dfp=posList[palabra]['df']
            wq=tfq*math.log10(numDoc/dfp)
            if palabra in posList:
                for doc in posList[palabra]:
                    if doc!='df':
                        if doc not in scores:
                            scores[doc]=0
                for doc in posList[palabra]:
                    if doc != 'df':
                        tfd=len(doc)
                        wd=tfd*math.log10(numDoc/dfp)
                        scores[doc]+=wd*wq
        scoresln=len(scores)
        sortedScores=dict(sorted(scores.items(),  key=lambda item: item[1], reverse=True))
        for doc in scores:
            scores[doc]=scores[doc]/scoresln
        sortedScores=dict(sorted(scores.items(),  key=lambda item: item[1], reverse=True))
        return list(sortedScores.items())

    def main(self):
        numDoc=len(self.doc)
        query='habia una vez'
        res=self.cosineScore(query,self.posList, numDoc,500)
        for tupla in res:
            print(tupla[0], tupla[1])

run=vsm()
run.main()