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
# ===========================================
# begins main() python script for TSP ILS/VNS
# ===========================================

# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')
#pTSP.n  = 5
#pTSP.vx = [10, 20, 30, 40, 50]
#pTSP.vy = [10, 20, 30, 40, 50]
#pTSP.dist = ...

# initializes optframe engine
#pTSP.engine = optframe.Engine(optframe.APILevel.API1d)
print(pTSP)

# Register Basic Components
comp_list = pTSP.engine.setup(pTSP)
print(comp_list)

#ev_idx = pTSP.engine.minimize(pTSP, mycallback_fevaluate)
ev_idx = comp_list[0]
print("evaluator id:", ev_idx)

#c_idx = pTSP.engine.add_constructive(pTSP, mycallback_constructive)
c_idx = comp_list[2]
print("c_idx=", c_idx)

#is_idx = pTSP.engine.create_initial_search(ev_idx, c_idx)
is_idx = 0
print("is_idx=", is_idx)

# test each component

fev = pTSP.engine.get_evaluator(ev_idx)
pTSP.engine.print_component(fev)

fc = pTSP.engine.get_constructive(c_idx)
pTSP.engine.print_component(fc)

solxx = pTSP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z1 = pTSP.engine.fevaluator_evaluate(fev, True, solxx)
print("evaluation:", z1)

# NOT Possible for now... needs more "testing" API0 features...

#   // swap 0 with 1
#   MoveSwap move{ make_pair(0, 1), fApplySwap };
#   move.print();
#   // NSSwap nsswap;
#   // move for solution 'esol'
#   auto m1 = nsswap.randomMove(esol);
#   m1->print();
#   std::cout << std::endl;
#   std::cout << "begin listing NSSeqSwapFancy" << std::endl;
#   //
#   auto it1 = nsseq2->getIterator(esol);
#   for (it1->first(); !it1->isDone(); it1->next())
#      it1->current()->print();
#   std::cout << "end listing NSSeqSwapFancy" << std::endl;


# get index of new NS
#ns_idx = pTSP.engine.add_ns(pTSP,
#                           mycallback_ns_rand_swap,
#                           apply_swap,
#                           eq_swap,
#                           cba_swap)
ns_idx = pTSP.engine.add_ns_class(pTSP, NSSeqSwap)
print("ns_idx=", ns_idx)


# pack NS into a NS list
list_idx = pTSP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)


# get index of new NSSeq
#nsseq_idx = pTSP.engine.add_nsseq(pTSP,
#                                 mycallback_ns_rand_swap,
#                                 mycallback_nsseq_it_init_swap,
#                                 mycallback_nsseq_it_first_swap,
#                                 mycallback_nsseq_it_next_swap,
#                                 mycallback_nsseq_it_isdone_swap,
#                                 mycallback_nsseq_it_current_swap,
#                                 apply_swap,
#                                 eq_swap,
#                                 cba_swap)
nsseq_idx = pTSP.engine.add_nsseq_class(pTSP, NSSeqSwap)
print("nsseq_idx=", nsseq_idx)


print("Listing components:")
pTSP.engine.list_components("OptFrame:")
# list the required parameters for OptFrame ComponentBuilder
print("engine will list builders for OptFrame: ")
#print(pTSP.engine.list_builders("OptFrame:"))
print()

print("building 'BI' neighborhood exploration as local search", flush=True)

# make next local search component silent (loglevel 0)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")
#pTSP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "4")
#pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "4")

ls_idx = pTSP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:BI",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS:NSFind:NSSeq 0")
print("ls_idx=", ls_idx, flush=True)


print("creating local search list", flush=True)

list_vnd_idx = pTSP.engine.create_component_list(
    "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")
print("list_vnd_idx=", list_vnd_idx)


print("building 'VND' local search")

vnd_idx = pTSP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:VND",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:LocalSearch[] 0")
print("vnd_idx=", vnd_idx)


#####
pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_component) for ILSLevels...")
print("")

pert_idx = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")
print("pert_idx=", pert_idx)

pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_single_obj_search) for ILS...")
print("")

# make next global search component info (loglevel 3)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "3")

#sos_idx = pTSP.engine.build_single_obj_search(
#    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
#    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 1 OptFrame:ILS:LevelPert 0  10  5")
#print("sos_idx=", sos_idx)

print("will start ILS for 3 seconds")

#lout = pTSP.engine.run_sos_search(sos_idx, 3.0) # 3.0 seconds max
#print('lout=', lout)

# build ILS Levels with iterMax=10 maxPert=5
ilsl = ILSLevels(pTSP.engine, 0, 0, 1, 0, 10, 5)
lout = ilsl.search(3.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)


print("FINISHED")
