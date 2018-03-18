# Demo program to solve the 8 queens problem
# See Chapter 2 of Eiben & Smith: "Introduction to Evolutionary Computing"
# $Revision: 1.10 $

from genetics.challenge import Challenge
from genetics.chromosomes.permutation import PermutationChromosome
from genetics.organism import Organism
from genetics.population import Population
from genetics.selectors.age import AgeSelector
from genetics.selectors.sampled.ranking import ExponentialRankingSelector
import random, time


BOARD_SIZE = 8


# Step 1: Define a challenge to be solved
class QueensChallenge(Challenge):
    def fitness(self, organism):
        # fitness is # of conflicts negated
        return -Challenge.fitness(self, organism)

    def solved(self, organism):
        # a board is ok when there are 0 conflicts on it
        return organism.decode(self) == 0

challenge = QueensChallenge()


# Step 2: Define the the board as a chromosome
class BoardPermutation(PermutationChromosome):
    def __init__(self, alleles=None, size=BOARD_SIZE, *args, **kwargs):
        if not alleles:
            alleles = range(0, size)
            random.shuffle(alleles)
            
        super(BoardPermutation, self).__init__(alleles, *args, **kwargs)
        
    def __repr__(self):
        string = ''
        for q in self.alleles:
            string += ' -' * q + ' Q' + ' -' * (self.size - q - 1) + "\n"
        return string
    
    mutate    = PermutationChromosome.mutate_swap
    crossover = PermutationChromosome.crossover_cycle
    
    
# Step 3: Create organisms to solve the QueensChallenge
class BoardSolver(Organism):
    def conflicts(self):
        pairs = 0
        
        # determine if there are diagonal conflicts
        for i in range(len(self.board.alleles)):
            q = self.board.alleles[i]

            for j in range(i + 1, len(self.board.alleles)):
                diff = j - i
                if self.board.alleles[j] == (q - diff) or self.board.alleles[j] == (q + diff):
                    pairs += 1
   
        return pairs
    
    genotype   = {'board':   BoardPermutation}
    phenotypes = {challenge: conflicts}


# Step 4: Population numbers
class QueensPopulation(Population):
    size = 100
    
    # Mating pool selector
    mating_pool_selector = ExponentialRankingSelector(challenge)
    mating_pool_size     = 10
    
    # Survivor selector
    survivor_selector = AgeSelector(challenge)
    
    # Mutation rate
    mutation = 0.5
    
    
# Step 4: Create a population and solve the challenge
if __name__ == '__main__':
    start = time.time()

    p = QueensPopulation(BoardSolver)
    best = p.solve(challenge, iterations=10000)
    print p.age, 'generations, conflicts:', best.conflicts()
    print best
    print best.board
    
    print 'time:', time.time() - start