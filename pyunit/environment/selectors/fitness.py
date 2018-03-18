# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.selectors.fitness import FitnessSelector
from pyunit.base.organisms import AgeFitnessOrganism
from pyunit.base.populations import SmallPopulation
import random, unittest


class FitnessSelectorTest(unittest.TestCase):
    def setUp(self):
        self.population = SmallPopulation(AgeFitnessOrganism)
        self.challenge  = Challenge()
        self.selector   = FitnessSelector(self.challenge)

    def testAgeSelector(self):
        # choose a random organism and adjust its age
        r = random.randint(0, 9)
        org = self.population[r]
        org.age = 10
        
        # select two youngest organisms from the population
        orgs = self.selector.select(2, self.population)
        self.assertTrue(org in orgs)
        self.assertEqual(len(orgs), 2)


if __name__ == '__main__':
    unittest.main()