# $Revision: 1.4 $

from genetics.chromosomes.tuple import TupleChromosome
import unittest


class EmptyTupleTest(unittest.TestCase):
    '''
    Tests empty tuple chromosomes
    '''
    def setUp(self):
        self.tuple1 = TupleChromosome(alleles=())
        self.tuple2 = TupleChromosome(alleles=())

    def testNotImplemented(self):
        self.assertRaises(NotImplementedError, self.tuple1.mutate)
        self.assertRaises(NotImplementedError, self.tuple1.crossover, self.tuple2)

    def testCmp(self):
        self.assertRaises(TypeError, cmp, self.tuple1, self)
        self.assertEqual(self.tuple1, self.tuple2)
        
    def testMutateInsert(self):
        self.assertEqual(self.tuple1.mutate_insert(), self.tuple2)
        
    def testMutateInvert(self):
        self.assertEqual(self.tuple1.mutate_invert(), self.tuple2)

    def testMutateScramble(self):
        self.assertEqual(self.tuple1.mutate_scramble(), self.tuple2)

    def testMutateSwap(self):
        self.assertEqual(self.tuple1.mutate_swap(), self.tuple2)

    def testCrossoverCut(self):
        self.assertRaises(TypeError, self.tuple1.crossover_one_point, self)
        self.assertTrue(self.tuple1 in self.tuple1.crossover_one_point(self.tuple2))
        
    def testCrossoverUniform(self):
        self.assertRaises(TypeError, self.tuple1.crossover_uniform, self)
        self.assertTrue(self.tuple1 in self.tuple1.crossover_uniform(self.tuple2))


class SingleTupleTest(unittest.TestCase):
    '''
    Tests tuple chromosomes with one item in them
    '''
    def setUp(self):
        self.tuple1 = TupleChromosome(alleles=(True))
        self.tuple2 = TupleChromosome(alleles=(False))
        self.tuple3 = TupleChromosome(alleles=True)

    def testCmp(self):
       self.assertNotEqual(self.tuple1, self.tuple2)
       self.assertEqual(self.tuple1, self.tuple3)
        
    def testMutateInsert(self):
        self.assertEqual(self.tuple1.mutate_insert(), self.tuple3)
        self.assertNotEqual(self.tuple2.mutate_insert(), self.tuple3)
        
    def testMutateInvert(self):
        self.assertEqual(self.tuple1.mutate_invert(), self.tuple3)
        self.assertNotEqual(self.tuple2.mutate_invert(), self.tuple3)
        
    def testMutateScramble(self):
        self.assertEqual(self.tuple1.mutate_scramble(), self.tuple3)
        self.assertNotEqual(self.tuple2.mutate_scramble(), self.tuple3)
        
    def testMutateSwap(self):
        self.assertEqual(self.tuple1.mutate_swap(), self.tuple3)
        self.assertNotEqual(self.tuple2.mutate_swap(), self.tuple3)
        
    def testCrossoverCut(self):
        self.assertTrue(self.tuple1 in self.tuple1.crossover_one_point(self.tuple3))
        self.assertTrue(self.tuple2 not in self.tuple1.crossover_one_point(self.tuple3))

        p1, p2 = self.tuple1.crossover_one_point(self.tuple2)
        self.assertEqual(self.tuple1, p1)
        self.assertEqual(self.tuple2, p2)

    def testCrossoverUniform(self):
        self.assertTrue(self.tuple1 in self.tuple1.crossover_uniform(self.tuple3))
        self.assertTrue(self.tuple2 not in self.tuple1.crossover_uniform(self.tuple3))

        p1, p2 = self.tuple2.crossover_one_point(self.tuple1)
        self.assertTrue(p1.alleles[0] in (True, False))
        self.assertTrue(p2.alleles[0] in (True, False))
        self.assertNotEqual(p1.alleles, p2.alleles)
        

class MultipleTupleTest(unittest.TestCase):
    '''
    Tests tuples with multiple items
    '''
    def setUp(self):
        self.tuple2a = TupleChromosome(alleles=(0, 1))
        self.tuple2b = TupleChromosome(alleles=(2, 3))
        self.tuple2c = TupleChromosome(alleles=(0, 1))
        self.tuple3a = TupleChromosome(alleles=(4, 5, 6))
        self.tuple3b = TupleChromosome(alleles=(0, 1, 2))
        
    def testCmp(self):
        self.assertNotEqual(self.tuple2a, self.tuple2b)
        self.assertTrue(self.tuple3b > self.tuple2a)

    def testMutateInsert2Items(self):
        self.assertTrue(self.tuple2a.mutate_insert().alleles in ((0,1), (1,0)))
                
    def testMutateInsert3Items(self):
        p = self.tuple3a.mutate_insert().alleles
        self.assertEqual(len(p), 3)
        self.assertTrue(4 in p and 5 in p and 6 in p)
        
    def testMutateInvert2Items(self):
        self.assertTrue(self.tuple2a.mutate_invert().alleles in ((0,1), (1,0)))
                
    def testMutateInvert3Items(self):
        p = self.tuple3a.mutate_invert().alleles
        self.assertEqual(len(p), 3)
        self.assertTrue(4 in p and 5 in p and 6 in p)
        
    def testMutateScramble2Items(self):
        self.assertTrue(self.tuple2a.mutate_scramble().alleles in ((0,1), (1,0)))
                
    def testMutateScramble3Items(self):
        p = self.tuple3a.mutate_scramble().alleles
        self.assertEqual(len(p), 3)
        self.assertTrue(4 in p and 5 in p and 6 in p)
        
    def testMutateSwap2Items(self):
        self.assertTrue(self.tuple2a.mutate_swap().alleles in ((0,1), (1,0)))
                
    def testMutateSwap3Items(self):
        p = self.tuple3a.mutate_swap().alleles
        self.assertEqual(len(p), 3)
        self.assertTrue(4 in p and 5 in p and 6 in p)
        
    def testCrossOverCut(self):
        p1, p2 = self.tuple2a.crossover_one_point(self.tuple2b)
        self.assertEqual(len(p1.alleles), p1.size, 2)
        self.assertEqual(len(p2.alleles), p2.size, 2)
        self.assertNotEqual(p1.alleles[0], p1.alleles[1])
        self.assertNotEqual(p2.alleles[0], p2.alleles[1])
            
    def testCrossOverCutDifferentLengths(self):
        self.assertRaises(ValueError, self.tuple2a.crossover_one_point, self.tuple3a)
        self.assertRaises(ValueError, self.tuple3b.crossover_one_point, self.tuple2b)
    
    def testCrossOverUniform(self):
        p1, p2 = self.tuple2a.crossover_uniform(self.tuple2b)
        self.assertEqual(len(p1.alleles), p1.size, 2)
        self.assertEqual(len(p2.alleles), p2.size, 2)
        self.assertNotEqual(p1.alleles[0], p1.alleles[1])
        self.assertNotEqual(p2.alleles[0], p2.alleles[1])
            
    def testCrossOverUniformDifferentLengths(self):
        self.assertRaises(ValueError, self.tuple2a.crossover_uniform, self.tuple3a)
        self.assertRaises(ValueError, self.tuple3b.crossover_uniform, self.tuple2b)


if __name__ == '__main__':
    unittest.main()