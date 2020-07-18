import json
import heapq

with open('participants.json') as f:
    participants = json.load(f)

data = {}
for fleet in participants:
    for p in participants[fleet]:
        data[p] = {
            'scores': [],
            'total': 0,
            'fleet': fleet
            }

#print(data)

def printOut(value, dataType):
    value = str(value)
    if dataType == 'name':
        width = 15
    elif dataType == 'score':
        width = 10
    elif dataType == 'standing':
        width = 5
    return value + ' ' * (width - len(value))

class Competitor:
    def __init__(self, name, fleet):
        self.name = name
        self.races = {}
        self.total = 0
        self.fleet = fleet
        self.throwoutIdxs = []
        
    def addScore(self, scoreObj):
        #print('addScore',scoreObj)
        self.races[len(self.races)+1] = scoreObj
        self.calcThrowouts()
        self.calcTotal()
        
    def calcThrowouts(self):
        #print('calcThrowouts')
        num = int(len(self.races) / 5)
        minq = []
        for race in self.races:
            if len(minq) < num:
                heapq.heappush(minq, self.races[race]['score'])
            else:
                heapq.heappushpop(minq, self.races[race]['score'])
        for race in self.races:
            if len(minq) == 0:
                break
            score = self.races[race]['score']
            if score in minq:
                self.races[race]['throwout'] = True
                minq.remove(score)
            else:
                self.races[race]['throwout'] = False

    def calcTotal(self):
        #print('calcTotal')
        #self.total = sum([self.races[i]['score'] for i in self.races])
        total = 0
        for race in self.races:
            if self.races[race]['throwout'] == False:
                total += self.races[race]['score']
        self.total = total

    def display(self):
        print(printOut(self.name,'name'),end='')
        for i in range(1,len(self.races)+1):
            score = self.displayScore(self.races[i])
            print(printOut(score,'score'),end='')
        print(printOut(self.total,'score'))
##        for race in self.races:
##            print(self.races[race])

    def displayScore(self,scoreObj):
        val = str(scoreObj['score'])
        if scoreObj['modifier'] != 'none':
            val = scoreObj['modifier'] + '-' + val
        if scoreObj['throwout']:
            val = '(' + val + ')'
        return val
    
    def setScore(self, raceNum, score):
        self.races[raceNum] = score
        self.calcThrowouts()
        self.calcTotal()

class Results:
    def __init__(self, fleets):
        self.competitors = {}
        for fleet in fleets:
            for name in fleets[fleet]:
                competitor = Competitor(name,fleet)
                self.competitors[name] = competitor
        self.raceNum = 0
    
    def get(self, fleet):
        pass

    def display(self, fleet):
        print(printOut('','standing') + printOut('Sailor','name'),end='')
        for i in range(1,self.raceNum+1):
            print(printOut('R'+str(i),'score'),end='')
        print('Total')
        place = 1
        cList = self.competitors.values()
        s = sorted(cList, key=lambda competitor: competitor.total)
        for c in s:
            if fleet != 'overall' and c.fleet != fleet:
                continue
            print(printOut(place,'standing'),end='')
            c.display()
            place += 1

    def addRace(self,d):
        self.raceNum += 1
        place = 1
        for name in d['finishes']:
            if name in d['OCS']:
                scoreObj = {
                    'score': len(self.competitors) + 1,
                    'modifier': 'OCS',
                    'throwout': False
                    }
            elif name in d['DSQ']:
                scoreObj = {
                    'score': len(self.competitors) + 1,
                    'modifier': 'DSQ',
                    'throwout': False
                    }
            else:
                scoreObj = {
                    'score': place,
                    'modifier': 'none',
                    'throwout': False
                    }
                place += 1
            self.competitors[name].addScore(scoreObj)

    def inputRace(self):
        i = 1
        arr = []
        raceObj = {
            'finishes': [],
            'OCS': [],
            'DSQ': []
            }
        while i <= len(self.competitors):
            name = input(str(i) + '. ')
            if name in self.competitors:
                raceObj['finishes'].append(name)
            else:
                print(name + ' not found, try again')
                continue
            i += 1
        asks = ['OCS','DSQ']
        for ask in asks:
            while True:
                name = input(ask + '. ')
                if name == 'done':
                    break
                if name in self.competitors:
                    raceObj['OCS'].append(name)
                else:
                    print(name + ' not found, try again')
        self.addRace(raceObj)

R = Results({'race': ['Kyle','Marco','Emi','Molly']})
R.inputRace()

##R.addRace({
##    'finishes': ['Kyle','Marco','Emi','Molly'],
##    'OCS': ['Emi'],
##    'DSQ': ['Molly']
##    })
##R.addRace({
##    'finishes': ['Marco','Molly','Kyle','Emi'],
##    'OCS': [],
##    'DSQ': []
##    })


##R = Results({'race': ['Kyle','Emi']})
##R.addRace({
##    'finishes': ['Kyle','Emi'],
##    'OCS': [],
##    'DSQ': []
##    })
R.display('race')
