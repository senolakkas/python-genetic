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


class Challenge(object):
    '''
    A challenge must implement:
        fitness(self, organism): decodes the phenotype for this challenge 
        into a (comparable) fitness rating
    '''
    def fitness(self, organism):
        '''
        Converts the phenotype for this challenge into a fitness rating, the
        higher the better.  By default this returns the decoded phenotype.
        
        @param organism: The organism to test the fitness of
        '''
        return organism.decode(self)
    
    
    def solved(self, organism): #@UnusedVariable
        '''
        Determines if an organism has found an optimal solution to the
        challenge.  By default this always returns false.
        
        @param organism: The organism that may have solved 
        '''
        return False
    
    
    def cmp(self, organism1, organism2):
        '''
        Calls fitness() on the organisms and compares them.  For use sorting in 
        descending order.
        
        @param organism1: an organism to compare
        @param organism2: an organism to compare
        '''
        return cmp(self.fitness(organism2), self.fitness(organism1))