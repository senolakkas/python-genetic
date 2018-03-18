# $Revision: 1.2 $

from genetics.challenge import Challenge
from genetics.organism import Organism
from genetics.util.decorators import comparable


class AgeFitnessOrganism(Organism):
    '''
    An organism with no genotype whose fitness is the same as its age
    '''    
    @comparable
    def __cmp__(self, other):
        return cmp(self.fitness(), other.fitness())
    
    def fitness(self):
        return self.age
    
    phenotypes = {Challenge: fitness}