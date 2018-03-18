# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.selectors.sampled.fitness import FitnessProportionalSelector
from genetics.selectors.sampled.ranking import (RankingSelector,
    LinearRankingSelector, ExponentialRankingSelector)
from genetics.selectors.sampled.sampling import SamplingSelector
from pyunit.base.organisms import AgeFitnessOrganism
from pyunit.base.populations import SmallPopulation
import random, unittest


class SamplingSelectorTest(unittest.TestCase):
    def setUp(self):
        self.population = SmallPopulation(AgeFitnessOrganism)
        self.challenge  = Challenge()

    def testVirtuals(self):
        selector = SamplingSelector(self.challenge)
        self.assertRaises(NotImplementedError, selector.select, 5, self.population)
        self.assertRaises(NotImplementedError, selector.scale, self.population)

        selector = RankingSelector(self.challenge)
        self.assertRaises(NotImplementedError, selector.select, 5, self.population)
        self.assertRaises(NotImplementedError, selector.scale, self.population)
        self.assertRaises(NotImplementedError, selector.selection_probabilities)

    def testFitnessNoVariance(self):
        selector = FitnessProportionalSelector(self.challenge)
        self.assertEqual([], selector.scale(self.population))
        self.assertEqual(len(selector.select(2, self.population)), 2)

    def testFitnessWithVariance(self):
        selector = FitnessProportionalSelector(self.challenge)
        # make one org more fit than the others
        r = random.randint(0, 9)
        org = self.population[r]
        org.age = 1000

        self.assertEqual(len(selector.scale(self.population)), self.population.size)
        self.assertEqual(len(selector.select(2, self.population)), 2)
        
    def testLinearRanking(self):
        selector = LinearRankingSelector(self.challenge)
        self.assertEqual(len(selector.scale(self.population)), self.population.size)
        self.assertEqual(len(selector.select(2, self.population)), 2)
        self.assertTrue(selector.pressure in selector._cache)
        self.assertTrue(self.population.size in selector._cache[selector.pressure])
        
    def testExponentialRanking(self):
        selector = ExponentialRankingSelector(self.challenge)
        self.assertEqual(len(selector.scale(self.population)), self.population.size)
        self.assertEqual(len(selector.select(2, self.population)), 2)
        self.assertTrue(selector.pressure in selector._cache)
        self.assertTrue(self.population.size in selector._cache[selector.pressure])
        

if __name__ == '__main__':
    unittest.main()