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
# $Revision: 1.11 $

from genetics.organism import Chromosome
from genetics.util.decorators import comparable, tuple_crossover
import random


class TupleChromosome(Chromosome):
    '''
    This chromosome represents a tuple with alleles of any types.  The tuple
    is of fixed length and all mutations and recombinations yield tuples
    chromosomes of the same length, and composed of the same alleles.
    
    Variation Invariant:
        - new tuples are the same size as their parents

    Mutation Methods:
        - mutate_swap()
        - mutate_insert()
        - mutate_scramble()
        - mutate_invert()
        
    Recombination Methods:
        - crossover_one_point(other)
        - crossover_uniform(other)
    '''
    def __init__(self, alleles, invariant=False, *args, **kwargs):
        '''
        Initializes the permutation based on a tuple passed in, or based on a
        size and a sequence of possible items to choose from.
        
        @param alleles: a sequence or a single allele
        @param invariant=False: variation invariant
        '''
        try:
            self.alleles = tuple(alleles)
        except TypeError:
            # received an atom instead of a sequence
            self.alleles = (alleles,)
            
        self.size = len(self.alleles)
            

    @comparable
    def __cmp__(self, other):
        '''
        Compares two tuples
            
        @param other: another TupleChromosome instance
        '''
        return cmp(self.alleles, other.alleles)
    
    
    def __repr__(self):
        '''
        String representation of a tuple chromosome
        '''
        return '%s: size=%s, alleles=%s' % (type(self), self.size, self.alleles)
    
    
    def mutate_swap(self):
        '''
        Creates a new tuple chromosome with two random alleles swapped
        
        Example:
            0 1 2 (3) 4 5 (6) 7 8 9  ->  0 1 2 (6) 4 5 (3) 7 8 9
        '''
        return type(self)(self._random_swap(), invariant=True)
    
    
    def mutate_insert(self):
        '''
        Creates a new tuple chromosome with two random alleles moved next to each other
        
        Example:
            0 1 2 (3) 4 5 (6) 7 8 9  ->  0 1 2 (3 6) 4 5 7 8 9  or
            0 1 2 (3) 4 5 (6) 7 8 9  ->  0 1 2 4 5 (3 6) 7 8 9
        '''
        return type(self)(self._random_insert(), invariant=True)
            
            
    def mutate_scramble(self):
        '''
        Creates a new tuple chromosome with a random section scrambled
        
        Example:
            0 1 2 (3 4 5 6) 7 8 9  ->  0 1 2 (5 3 6 4) 7 8 9    
        '''
        return type(self)(self._random_scramble(), invariant=True)
    
    
    def mutate_invert(self):
        '''
        Creates a new tuple chromosome with a random section reversed

        Example:
            0 1 2 (3 4 5 6) 7 8 9  ->  0 1 2 (6 5 4 3) 7 8 9    
        '''
        return type(self)(self._random_invert(), invariant=True)


    @tuple_crossover
    def crossover_one_point(self, other):
        '''
        One-Point Crossover
        J.H. Holland.  "Adaptation in Natural and Artificial Systems."
        
        Returns two child tuples from two sections randomly
        cut out of each parent (one-point crossover)
        
        Bias: positional
                
        Example:
            parents  => (0 1 2 3) [4 5 6 7 8 9], (9 8 7 6) {5 4 3 2 1 0}
            children => (0 1 2 3) {5 4 3 2 1 0}, (9 8 7 6) [4 5 6 7 8 9]
            
        @param other: another TupleChromosome instance
        '''
        # TODO: should we implement n-point?
        i = random.randrange(self.size)
        child1 = self.alleles [0:i] + other.alleles[i:]
        child2 = other.alleles[0:i] + self.alleles [i:]
        return type(self)(child1), type(self)(child2)
    
    
    @tuple_crossover
    def crossover_uniform(self, other):
        '''
        Uniform Crossover
        G. Syswerda.  "Uniform crossover in genetic algorithms."
        
        Recombines into two child tuples, each element randomly
        placed into the same position in one of the children.
        
        Bias: distributional
        
        Example:
            parents   =>  a1 a2 a3 a4,  b1 b2 b3 b4
            children  =>  a1 b2 b3 a4,  b1 a2 a3 b4
            
        @param other: another TupleChromosome instance
        '''
        child1, child2 = [], []
        
        for x, y in zip(self.alleles, other.alleles):
            if random.random() < 0.5:
                child1.append(x)
                child2.append(y)
            else:
                child1.append(y)
                child2.append(x)

        return type(self)(child1), type(self)(child2)

    
    def _random_indices(self, n=2, replacement=False):
        '''
        Internal method: returns a sorted tuple of n unique random indices from self.alleles
        
        @param n: number of indices to return
        @param replacement: with or without replacement
        '''
        indices = None
        if replacement:
            indices = [random.randrange(self.size) for i in xrange(n)] #@UnusedVariable
            
        else:
            indices = random.sample(xrange(self.size), n)

        indices.sort()
        return tuple(indices)
        
    
    def _random_swap(self):
        '''
        Internal method: returns a tuple with two alleles swapped
        '''
        new_alleles = list(self.alleles)
        
        if self.size > 1:
            # find two random elements to switch
            a, b = self._random_indices()            
            new_alleles[a], new_alleles[b] = new_alleles[b], new_alleles[a]
            return new_alleles

        return self.alleles
        
    
    def _random_insert(self):
        '''
        Internal method: returns a tuple with two random alleles adjacent
        '''
        if self.size > 2:
            first, second = self._random_indices()            
            
            insert  = (self.alleles[first], self.alleles[second])
            before  = self.alleles[0:first]
            between = self.alleles[first+1:second]
            after   = self.alleles[second+1:]
            
            if random.random() < 0.5:
                # sometimes we move the second one to the first
                return before + insert + between + after
            else:
                # and other times we move the first to the second
                return before + between + insert + after
            
        return self.alleles
        
        
    def _random_scramble(self):
        '''
        Internal method: returns a tuple with a random chunk scrambled
        '''
        if self.size > 1:
            first, second = self._random_indices()            
            
            before = self.alleles[0:first]
            middle = list(self.alleles[first:second+1])
            after  = self.alleles[second+1:]
            
            random.shuffle(middle)
            return before + tuple(middle) + after
        
        return self.alleles
    
    
    def _random_invert(self):
        '''
        Internal method: returns a tuple with a random chunk reversed
        '''
        if self.size > 1:
            first, second = self._random_indices()
            
            before = self.alleles[0:first]
            middle = list(self.alleles[first:second+1])
            after  = self.alleles[second+1:]
            
            middle.reverse()
            return before + tuple(middle) + after
        
        return self.alleles