# $Revision: 1.1 $

from genetics.chromosomes.bitstring import BitStringChromosome
import unittest


class BitStringChromosomeTest(unittest.TestCase):
    def setUp(self):
        self.bit1 = BitStringChromosome((True, False))
        self.bit2 = BitStringChromosome((False, True))
        self.bit3 = BitStringChromosome((1, 0))
        
    def testCmp(self):
        self.assertEqual(self.bit1, self.bit3)
        self.assertNotEqual(self.bit1, self.bit2)
        
    def testMutateFlip(self):
        for item in self.bit1.mutate_flip().alleles:
            self.assertTrue(item in (True, False))
            
            
if __name__ == '__main__':
    unittest.main()