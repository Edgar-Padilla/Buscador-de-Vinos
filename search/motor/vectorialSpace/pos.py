import json
class newPos:
    def __init__(self):
        with open("search/motor/files/posList.txt", "r") as f:
            self.posList=json.load(f)
    def agregarFrecuncia(self):
        self.newPosList=self.posList
        for key in self.posList:
            self.newPosList[key]['df']=len(self.posList[key])
        with open("search/motor/files/frecPosList.txt", "w") as f:
            json.dump(self.newPosList,f, ensure_ascii=False)
run=newPos()
run.agregarFrecuncia()