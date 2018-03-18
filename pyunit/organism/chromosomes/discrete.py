# $Revision: 1.2 $

from genetics.chromosomes.discrete import DiscreteChromosome
from pyunit.base.chromosomes import OneToTenDiscreteChromosome
import unittest


class DiscreteChromsomeTest(unittest.TestCase):
    def setUp(self):
        self.discrete1 = OneToTenDiscreteChromosome(5)
        self.discrete2 = OneToTenDiscreteChromosome(5)
    
    def testCmp(self):
        self.assertEqual(self.discrete1, self.discrete2)
        
    def testEmptySet(self):
        self.assertRaises(ValueError, DiscreteChromosome, 5)
        
    def testMutateReset(self):
        self.assertTrue(self.discrete1.mutate_reset().allele in OneToTenDiscreteChromosome.values)
    
    def testInvariant(self):
        x = 'not in values'
        self.assertEqual(DiscreteChromosome(x, invariant=True).allele, x)
    
    
if __name__ == '__main__':
    unittest.main()    