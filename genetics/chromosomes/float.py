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
# $Revision: 1.8 $

from genetics.organism import Chromosome
from genetics.util.decorators import comparable
import random


class FloatChromosome(Chromosome):
    '''
    This chromosome represents a single real-valued allele
    using the standard float type.  Mutation operators return
    new chromosomes based on uniform or nonuniform variance.
    
    Class/Instance Level Variables:
        - mean:      the mean value for uniform variance     (default = 0.0)
        - deviation: standard deviation for uniform variance (default = 1.0)

        - upper_bound: upper bound for nonuniform variance (default =  1.0)
        - lower_bound: lower bound for nonuniform variance (default = -1.0)       
    
    Variation Invariants:
        - uniform: yields floats based on mean and deviation of the parent
        - nonuniform: floats between lower and upper bounds of the parent
    
    Mutation Methods:
        - mutate_uniform()
        - mutate_nonuniform()
    '''
    mean        =  0.0
    deviation   =  1.0
    upper_bound =  1.0
    lower_bound = -1.0
    
    
    def __init__(self, allele, *args, **kwargs):
        '''
        Initializes a chromosome based on the value passed in.  Throws
        a type error if it cannot be converted to a float.
        
        @param allele: float value for the chromosome
        '''
        self.allele = float(allele)
        if self.lower_bound > self.upper_bound:
            raise ValueError('lower_bound (%s) > upper_bound (%s)' % (self.lower_bound, self.upper_bound))
        self._nonuniform_size = self.upper_bound - self.lower_bound
        
    
    @comparable
    def __cmp__(self, other):
        '''
        Compares two floats
        
        @param other: other chromosome instance to compare to
        '''
        return cmp(self.allele, other.allele)
    
    
    def __repr__(self):
        '''
        String representation of a float chromosome
        '''
        return '%s: allele=%f' % (type(self), self.allele)
    
    
    def mutate_uniform(self):
        '''
        Creates a new float chromosome normally distributed around the mean
        '''
        return type(self)(allele=random.gauss(self.mean, self.deviation))


    def mutate_nonuniform(self):
        '''
        Creates a new float chromosome randomly distributed between
        the lower_bound and upper_bound class variables:  (L, U)
        '''
        return type(self)(allele=(random.random() * 
            self._nonuniform_size + self.lower_bound))    