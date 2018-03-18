# $Revision: 1.5 $

from genetics.organism import Chromosome
from pyunit.base.chromosomes import EmptyChromosome
import unittest


class ChromosomeTest(unittest.TestCase):
    '''
    Tests errors thrown by abstract Chromosome class
    '''
    def setUp(self):
        self.chromosome1 = EmptyChromosome()
        self.chromosome2 = EmptyChromosome()
        
    def testInit(self):
        self.assertRaises(NotImplementedError, Chromosome)

    def testCmp(self):
        self.assertRaises(NotImplementedError, cmp, self.chromosome1, self)
        self.assertRaises(NotImplementedError, cmp, self.chromosome1, self.chromosome2)
        
    def testMutate(self):
        self.assertRaises(NotImplementedError, self.chromosome1.mutate)
        
    def testCrossover(self):
        self.assertRaises(NotImplementedError, self.chromosome1.crossover, self)
        self.assertRaises(NotImplementedError, self.chromosome1.crossover, self.chromosome1)
        

class OrganismTest(unittest.TestCase):
    '''
    TODO: Tests the Organism base class
    '''
    pass

            
if __name__ == '__main__':
    unittest.main()