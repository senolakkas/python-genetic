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
# $Revision: 1.3 $

from genetics.util.decorators import cached
import math


class FitnessStatistics(object):
    '''
    Generates mean and standard deviation for the fitness of a population
    '''
    def __init__(self, population, challenge):
        '''
        Constructs a stats instance.  Sets population and challenge on self.
        
        @param population: population to generate stats for
        @param challenge: challenge for generating fitness
        '''
        self.population = population
        self.challenge  = challenge
        
    
    @cached('__mean')
    def mean(self):
        '''
        Generates the mean for the fitness of a given population
        '''
        num = len(self.population)
        if num < 1:
            return 0.0
        
        total = sum([self.challenge.fitness(x) for x in self.population])
        return total / float(num)
        
    
    @cached('__stddev')
    def stddev(self):
        '''
        Generates the standard deviation for a given population
        '''
        num = float(len(self.population))
        if num <= 1:
            return 0.0
    
        mean = self.mean()
        variance = sum([(self.challenge.fitness(x) - mean) ** 2 for x in self.population])
        return math.sqrt((1/num) * variance)