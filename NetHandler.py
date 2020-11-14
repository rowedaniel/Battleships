from random import normalvariate
import time

_range = range
_len = len
_sum = sum
_list = list
_map = map

class neural_net:
    time = 0
    def __init__(self,NoOfLayers,Nodenums):
        t1 = time.time()
        self.nodes = [
                      [0 for n in _range(Nodenums[l])] \
                     for l in _range(NoOfLayers)]
        self.biases = [
                      [0 for n in _range(Nodenums[l])] \
                     for l in _range(NoOfLayers)]
        self.weights = [
                        [[0 \
                         for w in _range(_len(self.nodes[l-1]))] \
                        for n in _range(_len(self.nodes[l]))] \
                       for l in _range(1,NoOfLayers)
                       ]
        self.NoOfLayers = NoOfLayers
        neural_net.time += time.time()-t1

    def getoutput(self,innodes):
        t1 = time.time()
        ns = self.nodes
        ws = self.weights
        bs = self.biases
        ns[0]=innodes
        llen = self.NoOfLayers
        for li in _range(1,llen):
            nlen = _len(ns[li-1])
            self.nodes[li] = _list(_map(self.responsefunction,
                            [_sum([ws[li-1][row][col]*ns[li-1][col] \
                                   for col in _range(nlen)])+\
                             bs[li][row] \
                                for row in _range(nlen)]))
        neural_net.time += time.time()-t1
        return self.nodes[-1]
            
    def responsefunction(self, value):
        if value > 1: return 1
        elif value < 0: return 0
        return value

def makeNewNet(shape):
    newnn = neural_net(_len(shape),shape)
    for l in _range(1,_len(shape)-1):
            for n in _range(_len(newnn.weights[l])):
                newnn.weights[l][n][n] = -100
    return newnn

def makeNetWithBase(n,NoOfLayers,shape):
    t1 = time.time()
    newn = neural_net(NoOfLayers,shape)
    newn.biases = [[n.biases[li][ni]+normalvariate(0.0,0.1) \
                    for ni in _range(shape[li])] \
                  for li in _range(NoOfLayers)]
    newn.weights = [
                    [
                     [n.weights[li-1][ni][wi]+normalvariate(0.0,0.1) \
                      for wi in _range(_len(n.nodes[li-1]))] \
                     for ni in _range(_len(n.nodes[li]))] \
                    for li in _range(1,NoOfLayers)]
    makeNetWithBase.time += time.time()-t1
    return newn

makeNetWithBase.time = 0
        
