import random,time,pickle,math
from NetHandler import neural_net,makeNetWithBase,makeNewNet

_range = range
_any = any
_max = max
_min = min
_map = map
_list = list


def log(x):
    return 

def runOnesidedGame(n):
    t1 = time.time()
    boardx = 10
    boardy = 10
    boardsize = boardx*boardy
    H = 1
    V = boardx
    #boats = (2,)
    boats = (
             (51,61), # boat 1
            )
    
    guesses = [0.5 for i in _range(boardsize)]
    correct = [0,0,0,0,0,0,0,0,0,0,
               0,1,1,1,1,0,0,0,0,0,
               0,0,0,0,0,0,0,1,1,1,
               0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,1,0,0,
               0,1,0,0,1,0,0,1,0,0,
               0,1,0,0,1,0,0,1,0,0,
               0,0,0,0,1,0,0,0,0,0,
               0,0,0,0,1,0,0,0,0,0,
               0,0,0,0,1,0,0,0,0,0,]
##    for pos in boatpos:
##        correct[pos] = 1

    turns = score = 0
    won = True
    getoutput = n.getoutput
    while _any(correct):
        nouts = getoutput(guesses)
        nout = nouts.index(_max(nouts))
        if guesses[nout] != 0.5:
            won = False
            break
        if correct[nout] == 1:
            score += 10
        guesses[nout] = 0.25+0.75*correct[nout]
        correct[nout] = 0
        for b in boats:
            if nout not in b: continue
            if not (_any([correct[i] for i in b])):
                score += 50
                for i in b:
                    guesses[i] = 0.1
        turns += 1
        
    if won:
        score += 200
    score += _min((turns,21))
    runOnesidedGame.time += time.time()-t1
    return score
runOnesidedGame.time = 0
    

def startEvolution():
    t1 = time.time()
    random.seed(10)

    NoOfLayers = 6
    NoOfGens = 15
    NNetlen = 100
    shape = [100,100,100,100,100,100]
    NNets = [makeNewNet(shape) for i in _range(NNetlen)]
    
    scores = [0 for i in _range(NNetlen)]
    bestnets = [0 for i in _range(3)]
    
    for g in _range(NoOfGens):
        scores = _list(_map(runOnesidedGame, NNets))
        for i in _range(3):
            nindex = scores.index(_max(scores))
            bestnets[i] = NNets[nindex]
            thirdbest = scores.pop(nindex)
            #NNets.pop(nindex)
        NNets = bestnets+[makeNetWithBase(bestnets[i%3],NoOfLayers,shape) \
                           for i in _range(NNetlen-3)]
        print(g,thirdbest)
    pickle.dump((NNets,random.getstate()), open('NNetsavemain.txt','wb'))
    print(time.time()-t1)
    return NNets,scores

def continueEvolution(NoOfGens,PeriodicSave):
    t1 = time.time()
    NNets,rstate = pickle.load(open('NNetsavemain.txt','rb'))
    saveindex = 0
    
    NNetlen = 100
    shape = [100,100,100,100,100,100]
    NoOfLayers = 6
    scores = [0 for i in _range(NNetlen)]
    bestnets = [0 for i in _range(3)]
    
    for g in _range(NoOfGens):
        scores = _list(_map(runOnesidedGame, NNets))
        for i in _range(3):
            nindex = scores.index(_max(scores))
            bestnets[i] = NNets[nindex]
            thirdbest = scores.pop(nindex)
            #NNets.pop(nindex)
        NNets = bestnets+[makeNetWithBase(bestnets[i%3],NoOfLayers,shape) \
                           for i in _range(NNetlen-3)]
        print(g,thirdbest)
        if g % PeriodicSave == 0:
            pickle.dump((NNets,random.getstate()),
                        open('NNetsave%s.txt' % saveindex, 'wb'))
            saveindex += 1
    pickle.dump((NNets,random.getstate()), open('NNetsavemain.txt','wb'))
    print(time.time()-t1)
    return NNets,scores
    
            
        
