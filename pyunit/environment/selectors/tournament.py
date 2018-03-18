# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.selectors.tournament import TournamentSelector
from pyunit.base.organisms import AgeFitnessOrganism
from pyunit.base.populations import SmallPopulation
import random, unittest


class TournamentSelectorTest(unittest.TestCase):
    def setUp(self):
        self.population = SmallPopulation(AgeFitnessOrganism)
        self.challenge  = Challenge()
        self.selector   = TournamentSelector(self.challenge, 10)

    def testAgeSelector(self):
        # make one organism more fit
        r = random.randint(0, 9)
        org = self.population[r]
        org.age = 10        
        
        # it should be selected each time since population size == tournament size
        orgs = self.selector.select(2, self.population)
        self.assertTrue(orgs[0] is orgs[1])
        self.assertEqual(len(orgs), 2)

    def testCompeteEven(self):
        list = range(0, 100)
        random.shuffle(list)
        self.assertEqual(self.selector.compete(list), 99)

    def testCompeteOdd(self):
        list = range(0, 101)
        random.shuffle(list)
        self.assertEqual(self.selector.compete(list), 100)


if __name__ == '__main__':
    unittest.main()