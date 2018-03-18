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

from genetics.organism import Chromosome
from genetics.util.decorators import comparable
import random


class IntegerChromosome(Chromosome):
    '''
    This chromosome represents a single integer-valued allele.
    
    Class/Instance Level Variables:
        - upper_bound: upper bound for creep variance (default =  1.0)
        - lower_bound: lower bound for creep variance (default = -1.0)       
    
    Variation Invariants:
        - creep: yields integers from the current value plus the
          a random integer between the lower and upper bounds
    
    Mutation Methods:
        - mutate_creep()
    '''
    upper_bound =  1
    lower_bound = -1
    
    
    def __init__(self, allele, *args, **kwargs):
        '''
        Initializes a chromsome based on the value passed in.  Throws
        a type error if it cannot be converted to an integer.
        
        @param allele: integer value for the chromosome
        '''
        self.allele = int(allele)
        if self.lower_bound > self.upper_bound:
            raise ValueError('lower_bound (%s) > upper_bound (%s)' % \
                (self.lower_bound, self.upper_bound))
        
    
    @comparable
    def __cmp__(self, other):
        '''
        Compares two integers
        
        @param other: other chromosome instance to compare to
        '''
        return cmp(self.allele, other.allele)
    
    
    def __repr__(self):
        '''
        String representation of an integer chromosome
        '''
        return '%s: allele=%i' % (type(self), self.allele)
    
    
    def mutate_creep(self):
        '''
        Creates a new integer chromosome out of this chromosomes value
        plus a creep value randomly chosen from the lower and upper bounds
        '''
        return type(self)(allele=(self.allele + 
            random.randint(self.lower_bound, self.upper_bound)))
    