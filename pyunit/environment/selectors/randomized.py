# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.selectors.randomized import RandomSelector
from pyunit.base.organisms import AgeFitnessOrganism
from pyunit.base.populations import SmallPopulation
import unittest


class RandomSelectorTest(unittest.TestCase):
    def setUp(self):
        self.population = SmallPopulation(AgeFitnessOrganism)
        self.challenge  = Challenge()
        self.selector   = RandomSelector(self.challenge)

    def testAgeSelector(self):
        orgs = self.selector.select(2, self.population)
        self.assertTrue(orgs[0] is not orgs[1])
        self.assertEqual(len(orgs), 2)


if __name__ == '__main__':
    unittest.main()