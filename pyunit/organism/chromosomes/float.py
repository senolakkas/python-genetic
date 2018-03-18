# $Revision: 1.2 $

from genetics.chromosomes.float import FloatChromosome
import unittest


class FloatChromsomeTest(unittest.TestCase):
    def setUp(self):
        self.float1 = FloatChromosome(1.0)
        self.float2 = FloatChromosome('2.0')
        self.float3 = FloatChromosome(-1)
    
    def testCmp(self):
        self.assertTrue(self.float1 < self.float2)
        self.assertTrue(self.float1 > self.float3)
        self.assertTrue(self.float2 > self.float3)
    
    def testType(self):
        self.assertRaises(TypeError, FloatChromosome, [])
    
    def testMutateUniform(self):
        self.assertTrue(-100 < self.float1.mutate_uniform().allele < 100)
        self.float1.deviation = 0.1
        self.float1.mean = -100
        self.assertTrue(self.float1.mutate_uniform().allele < 0)
        
    def testMutateNonuniform(self):
        self.assertTrue(-1 <= self.float2.mutate_nonuniform().allele <= 1)
        self.float2.lower_bound = -5
        self.float2.upper_bound = -3
        self.assertTrue(-5 <= self.float2.mutate_nonuniform().allele <= -3)
    
    
if __name__ == '__main__':
    unittest.main()    