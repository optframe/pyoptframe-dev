# OptFrame Python Demo TSP - Traveling Salesman Problem

import os
from typing import List
import random
# DO NOT REORDER 'import sys ...'
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
#
from optframe import *

class SolutionTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n : int = 0
        # visited cities as a list
        self.cities : List[int] = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionTSP(n={self.n};cities={self.cities})"
    
class ProblemContextTSP(object):
    def __init__(self):
        # float engine for OptFrame
        self.engine = Engine(APILevel.API1d)
        # number of cities
        self.n = 0
        # x coordinates
        self.vx = []
        # y coordinates
        self.vy = []
        # distance matrix
        self.dist = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename: str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx.append(int(id_x_y[1]))
               self.vy.append(int(id_x_y[2]))
            #
            self.dist = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist[i][j] = round(self.euclidean(self.vx[i], self.vy[i], self.vx[j], self.vy[j]))

    def euclidean(self, x1, y1, x2, y2):
        import math
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextTSP(n={self.n};vx={self.vx};vy={self.vy};dist={self.dist})"
# continuation of ProblemContextTSP class...
    @staticmethod
    def minimize(pTSP: 'ProblemContextTSP', s: SolutionTSP) -> float:
        assert (s.n == pTSP.n)
        assert (len(s.cities) == s.n)
        # remember this is an API1d method
        f = 0.0
        for i in range(pTSP.n-1):
          f += pTSP.dist[s.cities[i]][s.cities[i + 1]];
        f += pTSP.dist[s.cities[int(pTSP.n) - 1]][s.cities[0]];
        return f
# continuation of ProblemContextTSP class...
    @staticmethod
    def generateSolution(problemCtx: 'ProblemContextTSP') -> SolutionTSP:
        sol = SolutionTSP()
        for i in range(problemCtx.n):
            sol.cities.append(i)
        random.shuffle(sol.cities)
        sol.n = problemCtx.n
        return sol

# optional tests...
assert isinstance(SolutionTSP, XSolution)            # composition tests 
assert isinstance(ProblemContextTSP,  XProblem)      # composition tests 
assert isinstance(ProblemContextTSP,  XConstructive) # composition tests    
assert isinstance(ProblemContextTSP,  XMinimize)     # composition tests


# move
class MoveSwap(object):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    @staticmethod
    def apply(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> 'MoveSwap':
        aux = sol.cities[m.j]
        sol.cities[m.j] = sol.cities[m.i]
        sol.cities[m.i] = aux
        # must create reverse move (j,i)
        return MoveSwap(m.j, m.i)
    @staticmethod
    def canBeApplied(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> bool:
        return True
    @staticmethod
    def eq(problemCtx: ProblemContextTSP, m1: 'MoveSwap', m2: 'MoveSwap') -> bool:
        return (m1.i == m2.i) and (m1.j == m2.j)

class NSSwap(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
        import random
        i = random.randint(0, pTSP.n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, pTSP.n - 1)
            j = random.randint(0, pTSP.n - 1)
        return MoveSwap(i, j)
# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current

class IteratorSwap(object):
    def __init__(self, _i: int, _j: int):
        self.i = _i
        self.j = _j
    @staticmethod
    def first(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        it.i = 0
        it.j = 1
    @staticmethod
    def next(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        if it.j < pTSP.n - 1:
            it.j = it.j+1
        else:
            it.i = it.i + 1
            it.j = it.i + 1
    @staticmethod
    def isDone(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        return it.i >= pTSP.n - 1

    @staticmethod
    def current(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        return MoveSwap(it.i, it.j)
    
class NSSeqSwap(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
        # there is no need to repeat from previous NSSwap, but this makes example more clear
        import random
        i = random.randint(0, pTSP.n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, pTSP.n - 1)
            j = random.randint(0, pTSP.n - 1)
        return MoveSwap(i, j)
    
    @staticmethod
    def getIterator(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
        return IteratorSwap(-1, -1)
# =========================================
# begins main() python script for TSP BRKGA
# =========================================

#
# random constructive: updates parameter ptr_array_double of type (LibArrayDouble*)
#
def mycallback_constructive_rk(problemCtx: ProblemContextTSP, ptr_array_double) -> int:
    rkeys = []
    for i in range(problemCtx.n):
        key = random.random() # [0,1] uniform
        rkeys.append(key)
    #
    ptr_array_double.contents.size = len(rkeys)
    ptr_array_double.contents.v = engine.callback_adapter_list_to_vecdouble(rkeys)
    return len(rkeys)


#
# decoder function: receives a problem instance and an array of random keys (as LibArrayDouble)
#
def mycallback_decoder_rk(problemCtx: ProblemContextTSP, array_double : engine.LibArrayDouble) -> SolutionTSP:
    #
    sol = SolutionTSP()
    #
    lpairs = []
    for i in range(array_double.size):
        p = [array_double.v[i], i]
        lpairs.append(p)
    #
    #print("lpairs: ", lpairs)
    sorted_list = sorted(lpairs)
    #print("sorted_list: ", sorted_list)
    #
    sol.n = problemCtx.n
    sol.cities = []
    for i in range(array_double.size):
        sol.cities.append(sorted_list[i][1]) # append index of city in order
    return sol


# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')
#pTSP.n  = 5
#pTSP.vx = [10, 20, 30, 40, 50]
#pTSP.vy = [10, 20, 30, 40, 50]
#pTSP.dist = ...

print("problem=",pTSP)
# initializes optframe engine
comp_list = pTSP.engine.setup(pTSP)
print(comp_list)
# pTSP.engine = optframe.Engine(optframe.APILevel.API1d)


# Register Basic Components

#ev_idx = pTSP.engine.minimize(pTSP, mycallback_fevaluate)
ev_idx = comp_list[0]
print("evaluator id:", ev_idx)

c_rk_idx = pTSP.engine.add_constructive_rk(pTSP, mycallback_constructive_rk)
print("c_rk_idx=", c_rk_idx)

pTSP.engine.list_components("OptFrame:")

initepop_rk_id = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicInitialEPopulationRKBuilder", 
    "OptFrame:Constructive:EA:RK:ConstructiveRK 0",
    "OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK")
print("initepop_rk_id=", initepop_rk_id)

print("")
print("WILL CREATE DECODER!!")
dec_rk_idx = pTSP.engine.add_decoder_rk(pTSP, mycallback_decoder_rk)
print("dec_rk_idx=", dec_rk_idx)

pTSP.engine.list_components("OptFrame:")

print("")
print("WILL BUILD COMPLETE DECODER WITH EVALUATOR!!")
drk_rk_id = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicDecoderRandomKeysBuilder", 
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:EA:RK:DecoderRandomKeysNoEvaluation 0",
    "OptFrame:EA:RK:DecoderRandomKeys")
print("drk_rk_id=", drk_rk_id)


# =======================

print("")
print("testing builder (build_global_search) for BRKGA...")
print("")

g_idx = pTSP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:EA:RK:BRKGA",
    "OptFrame:EA:RK:DecoderRandomKeys 0  OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK 0 "
    "30 1000 0.4 0.3 0.6")
print("g_idx=", g_idx)



pTSP.engine.list_components("OptFrame:")

print("")
print("testing execution of GlobalSearch (run_global_search) for BRKGA...")
print("")

lout = pTSP.engine.run_global_search(g_idx, 3.0)
print('solution:', lout)

print("FINISHED")
