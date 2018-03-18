# Demo program to solve the knapsack problem
# See Chapter 2 of Eiben & Smith: "Introduction to Evolutionary Computing"
# Note that this version uses a permutation instead of a bit string
# $Revision: 1.6 $
from genetics.selectors.age import AgeSelector
from genetics.selectors.sampled.ranking import ExponentialRankingSelector

from genetics.challenge import Challenge
from genetics.chromosomes.permutation import PermutationChromosome
from genetics.organism import Organism
from genetics.population import Population
from sets import Set
import random, time


NUM_ITEMS = 100    # total items to choose from
MAX_COST  =  25    # max cost of an item
MAX_VALUE =  50    # max value of an item
KNAPSACK  =  75    # space in knapsack


# Step 1: Create items to choose from as (cost, value) tuples
items = Set()
for i in xrange(NUM_ITEMS):
    while True:
        cost, value = random.randint(1, MAX_COST), random.randint(1, MAX_VALUE)
        if (cost, value) not in items:
            items.add((cost, value))
            break


# Step 2: Define a knapsack challenge
challenge = Challenge()


# Step 3: Define a knapsack representation
# TODO: this could become more efficient by using a set chromosome
class Knapsack(PermutationChromosome):
    def __init__(self, knapsack=None, items=items, *args, **kwargs):
        if not knapsack:
            knapsack = list(items)
            random.shuffle(knapsack)
            
        super(Knapsack, self).__init__(knapsack, *args, **kwargs)
        
    mutate    = PermutationChromosome.mutate_swap
    crossover = PermutationChromosome.crossover_pmx
    
    
# Step 4: Create organisms that have a Knapsack
class KnapsackSolver(Organism):
    def __init__(self, max_cost=KNAPSACK, *args, **kwargs):
        self.max_cost = max_cost
        super(KnapsackSolver, self).__init__(*args, **kwargs)
        
    def value(self):
        # the value of all items from the start that will fit into the knapsack
        total_cost = total_value = 0
        
        for cost, value in self.knapsack.alleles:
            if total_cost + cost > self.max_cost:
                break
            
            total_cost += cost            
            total_value += value
        
        self.cost = total_cost
        return total_value

    genotype   = {'knapsack': Knapsack}
    phenotypes = {challenge:  value   }


# Step 5: Create a population
class TravelerPopulation(Population):
    size = 10
    
    # Mating pool selector
    mating_pool_selector = ExponentialRankingSelector(challenge)
    mating_pool_size     = 2
    
    # Survivor selector
    survivor_selector = AgeSelector(challenge)
    
    # Mutation rate
    mutation = 0.5
    
    
if __name__ == '__main__':
    start = time.time()
    
    p = TravelerPopulation(KnapsackSolver)
    best = p.solve(challenge, iterations=1000)
    print p.age, 'generations, knapsack value:', best.value()
    
    print 'time:', time.time() - start
