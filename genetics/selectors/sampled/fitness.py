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
# $Revision: 1.2 $

from genetics.selectors.sampled.sampling import SamplingSelector
from genetics.util.stats import FitnessStatistics


class FitnessProportionalSelector(SamplingSelector):
    '''
    Fitness Proportional Selection using sigma scaling
    and stochastic universal sampling
    '''
    def __init__(self, challenge, pressure=2.0):
        '''
        Constructs a fitness proportioanal selector with a default pressure of 2.0
        
        @param challenge: the challenge instance for fitness evaluation
        @param pressure: selection pressure constant
        '''
        super(FitnessProportionalSelector, self).__init__(challenge, pressure)
        
        
    def scale(self, population=[]):
        '''
        Sigma scaling of fitness values
        D.E. Goldberg.  "Genetic Algorithms in Search, Optimization, and 
        Machine Learning."
        
        Returns a list of scaled fitness values:
            [max(fitness - (mean - constant * standard deviation) / sum, 0), ...]
        
        The sigma constant (self.pressure) is set to 2.0 by default.
        
        @param population: a Population instance or a list of organisms                
        '''
        stats  = FitnessStatistics(population, self.challenge)
        mean   = stats.mean()
        dev    = stats.stddev()
        scaled = [max(0.0, self.challenge.fitness(org) - (mean - self.pressure * dev)) \
                  for org in population]
        total  = sum(scaled)
        
        try:
            return [fitness / total for fitness in scaled]
        
        except ZeroDivisionError:
            return []