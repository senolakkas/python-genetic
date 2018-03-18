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

from genetics.chromosomes.tuple import TupleChromosome
import random


class BitStringChromosome(TupleChromosome):
    '''
    This chromosome represents a bit string as a tuple which 
    contains only boolean values
    
    Variation Invariants:
        - new bit strings are the same size as their parents
        - bit strings contain only boolean values
        
    Mutation Methods:
        - mutate_flip()
        - mutate_swap()
        - mutate_insert()
        - mutate_scramble()
        - mutate_invert()
        
    Recombination Methods:
        - crossover_one_point(other)
        - crossover_uniform(other)
    '''
    def __init__(self, alleles, *args, **kwargs):
        '''
        Initializes the bit string based on a tuple passed in.  Raises
        a ValueError if any alleles cannot be converted to boolean values.
        
        @param alleles: a sequence of boolean values
        '''
        super(BitStringChromosome, self).__init__(
            [bool(allele) for allele in alleles])

        
    def mutate_flip(self):
        '''
        Returns a new bit string with a random bit flipped
        
        Example:
            T F T (T) F  ->  T F T (F) F 
        '''
        new_alleles = list(self.alleles)
        
        index = random.randrange(self.size)
        new_alleles[index] = not new_alleles[index]
        return type(self)(new_alleles)