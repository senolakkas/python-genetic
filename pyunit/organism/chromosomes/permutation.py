# $Revision: 1.9 $

from genetics.chromosomes.permutation import PermutationChromosome
import unittest


class EmptyPermutationTest(unittest.TestCase):
    '''
    Tests empty permutation chromosomes
    '''
    def setUp(self):
        self.permutation1 = PermutationChromosome(alleles=())
        self.permutation2 = PermutationChromosome(alleles=())
        
    def testMutateOperators(self):
        self.assertEqual(self.permutation1.mutate_insert(),   self.permutation2)
        self.assertEqual(self.permutation1.mutate_invert(),   self.permutation2)
        self.assertEqual(self.permutation1.mutate_scramble(), self.permutation2)
        self.assertEqual(self.permutation1.mutate_swap(),     self.permutation2)
    
    def testCrossover(self):
        self.assertEqual(self.permutation1.crossover_one_point, None)
        self.assertEqual(self.permutation1.crossover_uniform, None)
        self.assertRaises(TypeError, self.permutation1.crossover_order, self)
        self.assertTrue(self.permutation1 in self.permutation1.crossover_order(self.permutation2))

        
class SinglePermutationTest(unittest.TestCase):
    '''
    Tests permutation chromosomes with one item in them
    '''
    def setUp(self):
        self.permutation1 = PermutationChromosome(alleles=(True))
        self.permutation2 = PermutationChromosome(alleles=(False))
        self.permutation3 = PermutationChromosome(alleles=True)

    def testCrossoverOrder(self):
        self.assertTrue(self.permutation1 in self.permutation1.crossover_order(self.permutation3))
        self.assertTrue(self.permutation2 not in self.permutation1.crossover_order(self.permutation3))            


class MultiplePermutationTest(unittest.TestCase):
    '''
    Tests permutations with multiple items
    '''
    single_edges = {4: [6, 5], 5: [4, 6], 6: [4, 5]}
    
    def setUp(self):
        self.permutation2a = PermutationChromosome(alleles=(0, 1))
        self.permutation2b = PermutationChromosome(alleles=(2, 3))
        self.permutation2c = PermutationChromosome(alleles=(0, 1))
        self.permutation3a = PermutationChromosome(alleles=(4, 5, 6))
        self.permutation3b = PermutationChromosome(alleles=(0, 1, 2))
        
    def testUniqueness(self):
        self.assertRaises(ValueError, PermutationChromosome, (0, 0))    
        
    def testInvariant(self):
        self.assertEqual(PermutationChromosome((0, 1, 0), invariant=True).alleles, (0, 1, 0))
        
    def testCrossoverDifferentLengths(self):
        self.assertRaises(ValueError, self.permutation2a.crossover_order, self.permutation3a)
        self.assertRaises(ValueError, self.permutation3b.crossover_order, self.permutation2b)
        
        self.assertRaises(ValueError, self.permutation2a.crossover_edge, self.permutation3a)
        self.assertRaises(ValueError, self.permutation3b.crossover_edge, self.permutation2b)

        self.assertRaises(ValueError, self.permutation2a.crossover_pmx, self.permutation3a)
        self.assertRaises(ValueError, self.permutation3b.crossover_pmx, self.permutation2b)

        self.assertRaises(ValueError, self.permutation2a.crossover_cycle, self.permutation3a)
        self.assertRaises(ValueError, self.permutation3b.crossover_cycle, self.permutation2b)

    def testCrossoverOrder(self):
        p1, p2 = self.permutation2a.crossover_order(self.permutation2b)
        self.assertNotEqual(p1, p2)
        self.assertEqual(p1.size, self.permutation2a.size)
        
    def testBuildOrderedPermutation(self):
        p1, p2 = self.permutation3a, self.permutation3b
        self.assertEqual(p1._build_ordered_permutation(p1, p2, 0, 0), [4,1,2])
        self.assertEqual(p1._build_ordered_permutation(p1, p2, 0, 1), [4,5,2])
        self.assertEqual(p1._build_ordered_permutation(p1, p2, 1, 2), [0,5,6])

        self.assertEqual(p1._build_ordered_permutation(p2, p1, 0, 0), [0,5,6])
        self.assertEqual(p1._build_ordered_permutation(p2, p1, 0, 1), [0,1,6])
        self.assertEqual(p1._build_ordered_permutation(p2, p1, 1, 2), [4,1,2])

    def testSingleEdge(self):
        self.assertEqual(self.single_edges, self.permutation3a._edge_table())

    def testDoubleEdges(self):
        p3a = self.permutation3a
        self.assertEqual(self.single_edges, p3a._double_edge_table(p3a))
        self.assertEqual({}, p3a._double_edge_table(self.permutation2a))
        
    def testCycleCrossover(self):
        p1, p2 = self.permutation3a.crossover_cycle(self.permutation3b)
        self.assertEqual(p1.alleles, (4,1,6))
        self.assertEqual(p2.alleles, (0,5,2))
        
    def testPMX(self):
        p1, p2 = self.permutation2a.crossover_order(self.permutation2b)
        self.assertEqual(p1.size, self.permutation2a.size)

    def testBuildPMXPermutation(self):
        p1, p2 = self.permutation3a, self.permutation3b
        self.assertEqual(p1._build_pmx_permutation(p1, p2, 0, 0), [4,1,2])
        self.assertEqual(p1._build_pmx_permutation(p1, p2, 0, 1), [4,5,2])
        self.assertEqual(p1._build_pmx_permutation(p1, p2, 1, 2), [0,5,6])
        
        
if __name__ == '__main__':
    unittest.main()