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
# $Revision: 1.5 $

from genetics.selector import Selector
from genetics.selectors.randomized import RandomSelector
from genetics.util.decorators import virtual
import random


class SamplingSelector(Selector):
    '''
    Base selector class for selectors that use Stochastic
    Universal Sampling.

    TODO: explain pressure
    '''
    def __init__(self, challenge, pressure=None):
        '''
        Constructs a sampling selector with a given pressure
        
        @param challenge: the challenge instance for fitness evaluation
        @param pressure: selection pressure constant
        '''
        self.pressure = pressure
        self.random_selector = RandomSelector(challenge)
        super(SamplingSelector, self).__init__(challenge)
    
    
    def select(self, n, population):
        '''
        Stochastic Universal Sampling
        J.E. Baker.  "Reducing bias and inefficiency in selection algorithms."
        
        Selects n organisms by sigma-scaling their fitness values
        and then giving one turn of an equally-spaced n-armed
        roulette turn.  Note that this makes it possible to select
        a single organism multiple times.
        
        @param n: number of organisms to select
        @param population: a Population instance or a list of organisms
        '''
        if n < 1:
            return []
        
        selected = [] # the organisms we return
        current = 0.0 # the float for determining which org to copy
        i = 0         # the index for selecting
        increment = 1.0 / n
        r = random.random() * increment
        
        scaled = self.scale(population)
        if scaled:
            # we were able to scale the population. proceed to select from it.
            while n > 0:
                current += scaled[i]
                while r < current:
                    selected.append(population[i])
                    r += increment
                    n -= 1
                    
                    # stop if we have already filled our list
                    if n <= 0:
                        break
                
                i += 1
                
            return selected
        
        else:
            # no fitness variance in the population. resort to random selection.
            return self.random_selector.select(n, population)
        
    
    @virtual
    def scale(self, population): #@UnusedVariable
        '''
        Determines the selection probability for each
        organism. Returns a list of those probabilities.
        
        @param population: a Population instance or a list of organisms        
        '''
        pass   