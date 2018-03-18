# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.organism import Organism
import unittest


class ChallengeErrorsTest(unittest.TestCase):
    '''
    Tests NotImplementedErrors thrown by abstract Challenge class
    '''
    def setUp(self):
        self.challenge = Challenge()
        self.organism  = Organism()

    def testFitness(self):
        self.assertRaises(NotImplementedError, self.challenge.fitness, self.organism)
        
    def testSolved(self):
        self.assertTrue(not self.challenge.solved(self.organism))
        
    def testCmp(self):
        self.assertRaises(NotImplementedError, self.challenge.cmp, self.organism, self.organism)

        
if __name__ == '__main__':
    unittest.main()