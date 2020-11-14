import pygame,random,time,math,pickle

_range = range
_any = any
_max = max
_min = min
_map = map
_list = list


def runOnesidedGameVisual(n):
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

    turns = 0
    score = 0
    won = True
    getoutput = n.getoutput
    for n in range(0,100,10):
        print(correct[n:n+10])
    while _any(correct):
        nouts = getoutput(guesses)
        print(nouts.index(_max(nouts)))
        nout = nouts.index(_max(nouts))
        if guesses[nout] != 0.5:
            won = False
            print('sigh')
            break
        if correct[nout] == 1:
            score += 10
            print('hit!')
        guesses[nout] = 0.25+0.75*correct[nout]
        correct[nout] = 0
        for b in boats:
            if nout not in b: continue
            if not (_any([correct[i] for i in b])):
                print('you sunk my battleship')
                score += 50
                for i in b:
                    guesses[i] = 0.1
        turns += 1
        
    if won:
        score += 200
    score += _min((turns,21))
    runOnesidedGameVisual.time += time.time()-t1
    return score
runOnesidedGameVisual.time = 0
