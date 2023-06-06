
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
