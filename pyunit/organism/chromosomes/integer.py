# $Revision: 1.2 $

from genetics.chromosomes.integer import IntegerChromosome
import unittest


class FloatChromsomeTest(unittest.TestCase):
    def setUp(self):
        self.int1 = IntegerChromosome(1.0)
        self.int2 = IntegerChromosome('2')
        self.int3 = IntegerChromosome(1)
    
    def testCmp(self):
        self.assertTrue(self.int1 <  self.int2)
        self.assertTrue(self.int2 >  self.int3)
        self.assertTrue(self.int1 == self.int3)
    
    def testType(self):
        self.assertRaises(TypeError, IntegerChromosome, [])
    
    def testMutateCreep(self):
        self.assertTrue(0 <= self.int1.mutate_creep().allele <= 2)
        self.int1.lower_bound = 100
        self.int1.upper_bound = 100
        self.assertEqual(self.int1.mutate_creep().allele, 101)
    
    
if __name__ == '__main__':
    unittest.main()    