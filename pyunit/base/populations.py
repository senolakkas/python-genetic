# $Revision: 1.1 $

from genetics.challenge import Challenge
from genetics.population import Population
from genetics.selectors.randomized import RandomSelector

class SmallPopulation(Population):
    '''
    A population of size 10
    '''
    size = 10
    
    # Mating pool selector
    mating_pool_selector = RandomSelector(Challenge)
    mating_pool_size     = 2
    
    # Survivor selector
    survivor_selector = RandomSelector(Challenge)
    
    # Mutation rate
    mutation = 0.5