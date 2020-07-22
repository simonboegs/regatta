#-----
#GET LIST OF SAILORS AND INITIALIZE
#-----

f = open('sailorList.txt','r')
results = {}
sailors = {}
coaches = {}

for i in range(2):
    line = f.readline().strip()
    while line != '-':
        if line == 'RACE' or line == 'INTERMEDIATE':
            fleet = line
            line = f.readline().strip()
            continue
        name, sailNumber, coach = line.split(' ')
        results[sailNumber] = []
        sailors[sailNumber] = {
            'name': name,
            'fleet': fleet,
            'coach': coach
            }
        if coach in coaches:
            coaches[coach]['numOfSailors'] += 1
        else:
            coaches[coach] = {
                'total': 0,
                'numOfSailors': 1
                }
        line = f.readline().strip()
        
#-----
#GET RESULTS FROM EACH RACE FROM FILE
#-----
        
f = open('results.txt','r')
numOfRaces = int(f.readline().strip().split(' ')[1])

for raceNum in range(1,numOfRaces+1):
    raceHeader = f.readline().strip()
    line = f.readline().strip()
    place = 1
    scores = {}
    while line != '-':
        if line == 'OCS' or line == 'DSQ' or line == 'FINISHES':
            beingLogged = line
            line = f.readline().strip()
            continue
        sailNumber = line
        if beingLogged == 'FINISHES':
            if sailNumber in scores:
                line = f.readline().strip()
                continue
            scores[sailNumber] = place
            place += 1
        else:
            scores[sailNumber] = beingLogged
        line = f.readline().strip()
    for sailNumber in scores:
        results[sailNumber].append(scores[sailNumber])
    #check if any sail numbers weren't accounted for in that race
    for key in results:
        if len(results[key]) < raceNum:
            results[key].append('DSQ')

#-----
#CALCULATE RESULTS
#-----

official = {}
for sailNumber in results:
    official[sailNumber] = {
        'scores': [],
        'total': 0
        }
    #convert each score to an object with a modifier (OCS, DSQ) and throwout boolean
    for score in results[sailNumber]:
        if score == 'DSQ' or score == 'OCS':
            scoreObj = {
                'score': len(sailors) + 1,
                'modifier': score,
                'throwout':  False
                }
        else:
            scoreObj = {
                'score': score,
                'modifier': 'none',
                'throwout': False
                }
        official[sailNumber]['scores'].append(scoreObj)
        
    #calc throwouts
    numOfThrowouts = int(len(official[sailNumber]['scores']) / 5)
    for throwoutNum in range(numOfThrowouts):
        worstIdx = -1
        idx = 0
        for scoreObj in official[sailNumber]['scores']:
            if not scoreObj['throwout'] and (worstIdx == -1 or scoreObj['score'] > official[sailNumber]['scores'][worstIdx]['score']):
                worstIdx = idx
            idx += 1
        official[sailNumber]['scores'][worstIdx]['throwout'] = True
        
    #calc total
    for scoreObj in official[sailNumber]['scores']:
        if scoreObj['throwout'] == False:
            official[sailNumber]['total'] += scoreObj['score']
    coach = sailors[sailNumber]['coach']
    coaches[coach]['total'] += official[sailNumber]['total']

#-----
#DISPLAY RESULTS
#-----

#spacing display method        
def getDisplay(s,dataType):
    if dataType == 'name':
        width = 15
    elif dataType == 'score':
        width = 10
    elif dataType == 'place':
        width = 5
    return s + (' ' * (width - len(s)))

#tiebreaker methods
def tiebreak(sailNumber1,sailNumber2): #returns True if 1 beats 2, False if 2 beats 1
    scores1 = orderScores(sailNumber1)
    scores2 = orderScores(sailNumber2)
    for i in range(len(scores1)):
        if scores1[i] < scores2[i]:
            return True
        elif scores2[i] < scores1[i]:
            return False
    for i in range(len(scores1)-1,-1,-1):
        score1 = official[sailNumber1]['scores'][i]['score']
        score2 = official[sailNumber2]['scores'][i]['score']
        if score1 < score2:
            return True
        elif score2 < score1:
            return False

def orderScores(sailNumber):
    scores = []
    for scoreObj in official[sailNumber]['scores']:
        if len(scores) == 0:
            scores.append(scoreObj['score'])
            continue
        spotFound = False
        for j in range(len(scores)-1,-1,-1):
            if scoreObj['score'] >= scores[j]:
                spotFound = True
                if j+1 == len(scores):
                    scores.append(scoreObj['score'])
                else:
                    scores.insert(j+1,scoreObj['score'])
                break
        if not spotFound:
            scores.insert(0,scoreObj['score'])
    return scores

#display each person's results
def displayResults(targetFleet):
    #sort scores into list of sail numbers
    sailNumberList = []
    for sailNumber in official:
        if len(sailNumberList) == 0:
            sailNumberList.append(sailNumber)
            continue
        spotFound = False
        for j in range(len(sailNumberList)-1,-1,-1):
            if official[sailNumber]['total'] >= official[sailNumberList[j]]['total']:
                if official[sailNumber]['total'] == official[sailNumberList[j]]['total']:
                    tieBreakBool = tiebreak(sailNumber,sailNumberList[j])
                    if tieBreakBool:
                        continue
                spotFound = True
                if j+1 == len(sailNumberList):
                    sailNumberList.append(sailNumber)
                else:
                    sailNumberList.insert(j+1,sailNumber)
                break
            
                
        if not spotFound:
            sailNumberList.insert(0,sailNumber)
    #display column headers
    print(getDisplay('','place') + getDisplay('NAME','name') + getDisplay('FLEET','name') + getDisplay('SAIL NUMBER','name'), end='')
    for raceNum in range(1,len(official[sailNumberList[0]]['scores']) + 1):
        print(getDisplay('R' + str(raceNum),'score'),end='')
    print(getDisplay('TOTAL','score'))
    #display sailor scores
    place = 1
    for sailNumber in sailNumberList:
        name = sailors[sailNumber]['name']
        fleet = sailors[sailNumber]['fleet']
        if targetFleet != 'OVERALL' and fleet != targetFleet:
            continue
        print(getDisplay(str(place),'place') + getDisplay(name,'name') + getDisplay(fleet, 'name') + getDisplay(sailNumber, 'name'), end='')
        for scoreObj in official[sailNumber]['scores']:
            score = str(scoreObj['score'])
            if scoreObj['modifier'] != 'none':
                score = scoreObj['modifier'] + '-' + score
            if scoreObj['throwout']:
                score = '(' + score + ')'
            print(getDisplay(score,'score'),end='')
        print(getDisplay(str(official[sailNumber]['total']),'score'))
        place += 1

#display total by coach
def displayCoachResults():
    #calculate coach score averages
    #sort coaches
    coachList = []
    for coach in coaches:
        coaches[coach]['avg'] = coaches[coach]['total'] / coaches[coach]['numOfSailors']
        if len(coachList) == 0:
            coachList.append(coach)
            continue
        spotFound = False
        for j in range(len(coachList)-1,-1,-1):
            if coaches[coach]['avg'] >= coaches[coachList[j]]['avg']:
                spotFound = True
                if j+1 == len(coachList):
                    coachList.append(coach)
                else:
                    coachList.insert(j+1,coach)
                break
        if not spotFound:
            coachList.insert(0,coach)
    #display column headers
    print(getDisplay('','place') + getDisplay('COACH','name') + getDisplay('# SAILORS','score') + getDisplay('TOTAL','score') + getDisplay('AVERAGE','score'))
    #display coach totals
    place = 1
    for coach in coachList:
        print(getDisplay(str(place),'place'),end='')
        print(getDisplay(coach,'name'),end='')
        print(getDisplay(str(coaches[coach]['numOfSailors']),'score'),end='')
        print(getDisplay(str(coaches[coach]['total']),'score'),end='')
        print(getDisplay(str(round(coaches[coach]['avg'],1)),'score'))
        place += 1

import sys
arg = sys.argv[1].upper()
fleets = ['OVERALL','INTERMEDIATE','RACE']

if arg in fleets:
    displayResults(arg)
else:
    if arg == 'COACHES' or arg == 'COACH':
        displayCoachResults()
    else:
        print(arg,'is not a valid argument')
