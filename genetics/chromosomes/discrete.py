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
from sets import Set
import random


class DiscreteChromosome(Chromosome):
    '''
    This chromosome represents alleles from a finite set of discrete values
    
    Class/Instance Level Variables:
        -values: a Set of possible allele values
    
    Variation Invariants:
        - all chromosome values are in the values set

    Mutation Methods:
        - mutate_reset()
    '''
    values = Set()
    
    
    def __init__(self, allele, invariant=False, *args, **kwargs):
        '''
        Initializes a chromsome based on the value passed in.  Throws
        a type error if it cannot be converted to an integer.
        
        @param allele: discrete value for the chromosome
        '''
        self.allele = allele
        
        if not invariant and allele not in self.values:            
            raise ValueError('%s is not an accepted allele value' % allele)
    
    
    @comparable
    def __cmp__(self, other):
        '''
        Compares two discrete chromosomes
        
        @param other: other chromosome instance to compare against
        '''
        return cmp(self.allele, other.allele)
    
    
    def __repr__(self):
        '''
        String representation of a discrete chromosome
        '''
        return '%s: allele=%s' % (type(self), self.allele)
    
    
    def mutate_reset(self):
        '''
        Creates a new discrete chromosome randomly from the values set
        '''
        # TODO: performance test this
        return type(self)(allele=random.choice(tuple(self.values)))   