class operators:
    def __init__(self):
        pass
    def andOperator(self,dic1,dic2):
        doc1=[]
        doc2=[]
        for key in dic1:
            doc1.append(int(key))
        for key in dic2:
            doc2.append(int(key))
        result=[]
        i=j=0
        while i<len(doc1) and j<len(doc2):
            if doc1[i]==doc2[j]:
                result.append(doc1[i])
                i+=1
                j+=1
            elif doc1[i]<doc2[j]:
                i+=1
            else:
                j+=1
        result=set(result)
        print(result)
        return result

    def orOperator(self,dic1,dic2):
        doc1=[]
        doc2=[]
        for key in dic1:
            doc1.append(int(key))
        for key in dic2:
            doc2.append(int(key))
        result=[]
        i=j=0
        while i<len(doc1) and j<len(doc2):
            if doc1[i]==doc2[j]:
                result.append(doc1[i])
                i+=1
                j+=1
            elif doc1[i]<doc2[j]:
                result.append(doc1[i])
                i+=1
            else:
                result.append(doc2[j])
                j+=1
        result=set(result)
        print(result)
        return result

    def notOperator(self,dic1, n):
        doc1=[]
        for key in dic1:
            doc1.append(int(key))
        result=[]
        i=0
        j=1
        while(i<len(doc1)):
            if(doc1[i]==j):
                i+=1
                j+=1
            elif(j<doc1[i]):
                result.append(j)
                j+=1
        while(j<n):
            result.append(j)
            j+=1
        result=set(result)
        print(result)
        return result

    def nandOperator(self,doc1,doc2,n):
        r1=self.notOperator(doc1,n)
        r2=self.notOperator(doc2,n)
        result=self.andOperator(r1,r2)
        result=set(result)
        print(result)
        return result
