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
# $Revision: 1.1 $

from genetics.util.decorators import virtual


class Selector(object):
    '''
    Abstract base class for selecting parents and survivors.
    '''
    def __init__(self, challenge):
        '''
        Creates a new selector
        
        @param challenge: the challenge instance for fitness evaluation
        '''
        self.challenge = challenge

    
    @virtual
    def select(self, n, population): #@UnusedVariable
        '''
        Selects n organisms from the population and returns them.
        
        @param n: number of organisms to select
        @param population: a Population instance or a list of organisms
        '''
        pass
         
    
    def cmp_fitness(self, x, y):
        '''
        Compares two organisms by descending fitness
        
        @param x: an organism
        @param y: an organism of the same type
        '''
        return cmp(self.challenge.fitness(y), self.challenge.fitness(x))