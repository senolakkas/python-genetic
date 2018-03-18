# Python genetic programming & evolutionary computing modules
# Copyright (C) 2006  Ryan J. O'Neil <ryanjoneil ~ at ~ gmail.com>
# http://python-genetic.sourceforge.net/
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# $Revision: 1.4 $

from genetics.selectors.sampled.sampling import SamplingSelector
from genetics.util.decorators import virtual
import math


class RankingSelector(SamplingSelector):
    '''
    Rank-based Selector
    J.E. Baker.  "Reducing bias and inefficiency in selection algorithms."
    '''   
    def __init__(self, challenge, pressure=None):
        '''
        Constructs a ranked selector

        @param challenge: the challenge instance for fitness evaluation
        @param pressure: selection pressure constant
        '''
        self._cache = {} # scaling depends on pressure and size, so it can be cached
        super(RankingSelector, self).__init__(challenge, pressure)
    

    def select(self, n, population):
        '''
        TODO: Selects n organisms...  SUS...

        @param population: a Population instance or a list of organisms                
        '''
        population.sort(cmp=self.cmp_fitness)
        return super(RankingSelector, self).select(n, population)
    
    
    def scale(self, population=[]):
        '''
        Caches the probabilities for ranked selection since it does not
        change unless population size or pressure changes.

        @param population: a Population instance or a list of organisms                
        '''
        # get the probability for this pressure.  cache it by size & pressure
        size = len(population)
        if self.pressure not in self._cache:
            self._cache[self.pressure] = {}
        if size not in self._cache[self.pressure]:
            self._cache[self.pressure][size] = self.selection_probabilities(population)
        return self._cache[self.pressure][size]
    

    @virtual
    def selection_probabilities(self, population=[]): #@UnusedVariable
        '''
        Determines the selection probability for each
        organism. Returns a list of those probabilities.

        @param population: a Population instance or a list of organisms                
        '''
        pass
        
    
        
class LinearRankingSelector(RankingSelector):
    '''
    Linear Ranking Selector
    TODO: explain pressure.  Find good default value.
    '''
    def __init__(self, challenge, pressure=1.5):
        '''
        Constructs a linear ranked selector with a default pressure of 1.5

        @param challenge: the challenge instance for fitness evaluation
        @param pressure: selection pressure constant
        '''
        super(LinearRankingSelector, self).__init__(challenge, pressure)
    
    
    def selection_probabilities(self, population=[]):
        '''
        Finds the selection probability for each item by its rank:
            P(i) = [(2 - pressure) / n] + [2i(pressure - 1) / n(n - 1)]

        @param population: a Population instance or a list of organisms                
        '''
        # create a list for this pressure & population size
        size  = len(population)
        return [((2.0-self.pressure) / size) + ((2.0*i)*(self.pressure-1.0) / (size * (size-1.0)))
                for i in xrange(1, size + 1)]

    

class ExponentialRankingSelector(RankingSelector):
    '''
    Exponential Ranking Selector
    TODO: explain pressure.  Find good default value.
    '''
    def __init__(self, challenge, pressure=0.9):
        '''
        Constructs an exponentially ranked selector with a default pressure of 0.9

        @param challenge: the challenge instance for fitness evaluation
        @param pressure: selection pressure constant
        '''
        super(ExponentialRankingSelector, self).__init__(challenge, pressure)
    
    
    def selection_probabilities(self, population=[]):
        '''
        Finds the selection probability for each item by its rank:
            P(i) = (1 - e^-i) / pressure

        @param population: a Population instance or a list of organisms                
        '''        
        # create a list for this pressure & population size
        return [(1 - (math.e ** -i)) / self.pressure 
                 for i in xrange(1, len(population)+1)]