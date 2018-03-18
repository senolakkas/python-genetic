# $Revision: 1.6 $

from genetics.chromosomes.discrete import DiscreteChromosome
from genetics.organism import Chromosome
from sets import Set


class EmptyChromosome(Chromosome):
    '''
    A chromosome that can be instantiated but does not implement anything else
    '''
    def __init__(self):
        pass


class OneToTenDiscreteChromosome(DiscreteChromosome):
    '''
    A chromosome that can have only values 1 to 10
    '''
    values = Set(range(1, 11))