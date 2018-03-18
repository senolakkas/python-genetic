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
# $Revision: 1.16 $

from genetics.chromosomes.tuple import TupleChromosome
from genetics.util.decorators import tuple_crossover, cached
from genetics.util.structures import Queue
from sets import Set
import random


class PermutationChromosome(TupleChromosome):
    '''
    This chromosome represents a permutation of any type of items as a tuple.
    It enforces the rule that each allele is unique.  All mutation and 
    crossover mechanisms are inherited from TupleChromosome.
    
    Variation Invariants:
        - new permutations are the same size as their parents
        - new permutations contain only unique alleles
        
    Mutation Methods:
        - mutate_swap()
        - mutate_insert()
        - mutate_scramble()
        - mutate_invert()
        
    Recombination Methods:
        - crossover_pmx(other) - partially mapped crossover
        - crossover_edge(other) - edge 3
        - crossover_order(other)
        - crossover_cycle(other)
        
    Not Inherited from TupleChromosome:
        - crossover_one_point(other)
        - crossover_uniform(other)
    '''
    def __init__(self, alleles, invariant=False, *args, **kwargs):
        '''
        Initializes the permutation based on a tuple passed in.  Raises
        an error if an allele occurs more than once.
        
        @param alleles: a sequence of *unique* alleles
            
        @param invariant=False: used to indicate that the variation
              invarants for this chromosome have not been broken by 
              the permutation mutation and crossover operators.  This
              is important for internal use since these operators can
              guarantee that new chromosomes contain unique alleles.
              Not intended for use by external code!
        
              Classes that inherit from PermutationChromosome must
              accept *args and **kwargs in their __init__.
        '''
        super(PermutationChromosome, self).__init__(alleles)
        
        # this parameter is meant for internal use only
        # allows us to skip uniqueness verification for performance reasons
        if not invariant:
            # make sure the permutation only contains unique items
            seen = Set()
            for x in self.alleles:
                if x in seen:
                    raise ValueError('Alleles in a permutation must be unique: ' 
                        + str(alleles))
                seen.add(x)
    

    # Delete crossover_one_point, crossover_n_point, and crossover_uniform
    # instead of inheriting them from TupleChromosome since they do not 
    # satisfy PermutationChromosome's variation invariants.
    crossover_one_point = None
    crossover_n_point   = None
    crossover_uniform   = None


    @tuple_crossover
    def crossover_pmx(self, other):
        '''
        Partially Mapped Crossover (PMX)
        D.E. Goldberg, R. Lingle.  "Alleles, loci, and the travelling salesman problem."
        D. Whitley.  "Permutations."
        
        Copies contiguous section from a parent into a child, places elements from
        the same section in the other parent into related locations in the child,
        then puts in the remaining elements from the second parent.
        
        Bias: adjacency
        
        Example:
            parents  => 0 1 2 3 4 5 6 7 8 9,  2 8 7 1 5 3 6 9 4 0
            children => 7 1 2 3 4 8 6 9 5 0,  0 8 7 1 5 4 6 2 3 9
            
        @param other: another PermutationChromosome instance
        '''
        first, second = self._random_indices()
        child1 = self._build_pmx_permutation(self, other, first, second)
        child2 = self._build_pmx_permutation(other, self, first, second)
        return type(self)(child1, invariant=True), type(self)(child2, invariant=True)        
         

    @tuple_crossover
    def crossover_edge(self, other):
        '''
        Edge-3 Crossover
        D. Whitley.  "Permutations."
        
        Builds children out of edges found in the parents.  Edges that
        appear in both parents take precedence over those in one.
        
        Bias: adjacency
        
        Example:
            parents  => 0 1 2 3 4 5 6 7 8 9,  9 8 7 6 5 4 3 2 1 0
            children => 3 2 1 6 5 4 9 8 7 0,  7 8 9 5 4 3 2 1 6 0
            
        @param other: another PermutationChromosome instance
        '''         
        child1, child2 = [], []
        my_edges  = self._edge_table()
        his_edges = other._edge_table()
        our_edges = self._double_edge_table(other)
        
        for child, unseen in (child1, Set(self.alleles)), (child2, Set(other.alleles)):
            
            current = None
            for i in xrange(self.size): #@UnusedVariable
                
                # if there is no current item, choose one randomly
                if not current:
                    current = random.choice(tuple(unseen))
                    
                # add the current element to the child and mark it as seen
                child.append(current)
                unseen.remove(current)                
                
                # choose next element:
                double = [x for x in our_edges.get(current, []) if x in unseen]
                if double:
                    # first try edges found in both permutations...
                    current = random.choice(double)
                    
                else:
                    # ...then try edges found only once...
                    single = [x for x in my_edges.get(current, [])  if x in unseen] + \
                             [x for x in his_edges.get(current, []) if x in unseen]
                    if single:
                        current = random.choice(single)
                    else:
                        current = None
                        
        return type(self)(child1, invariant=True), type(self)(child2, invariant=True)
        
        
    @tuple_crossover
    def crossover_order(self, other):
        '''
        Order Crossover
        L. Davis, Ed.  "Handbook of Genetic Algorithms."  Van Nostrand Reinhold, 1991.
        
        Randomly copies a segment each parent into a child, then copies
        the remaining elements from the other parent in the same order.
        Intended to transmit relative order of alleles.
        
        Bias: order
        
        Example:
            parents  => 0 1 2 3 4 5 6 7 8 9,  9 8 7 6 5 4 3 2 1 0
            children => 7 6 2 3 4 5 1 0 9 8,  2 3 7 6 5 4 8 9 0 1
            
        @param other: another PermutationChromosome instance
        '''
        # figure out what middle section to copy
        first, second = self._random_indices(replacement=True)
        child1 = self._build_ordered_permutation(self, other, first, second)
        child2 = self._build_ordered_permutation(other, self, first, second)
        return type(self)(child1, invariant=True), type(self)(child2, invariant=True)


    @tuple_crossover
    def crossover_cycle(self, other):
        '''
        Cycle Crossover
        I.M. Oliver, D.J. Smith, J. Holland.  "A study of permutation crossover
        operators on the travelling salesman problem."
        
        Preserves as much information as possible regarding absolute positions
        of alleles in the parents.  Chops parent tuples into cycles and switches
        between them in creating children.
        
        Bias: positional    
        
        Example:
            parents  => 0 1 2 3 4 5 6 7 8 9,  2 8 7 1 5 3 6 9 4 0
            children => 0 8 2 1 5 3 6 7 4 9,  2 1 7 3 4 5 6 9 8 0
            
        @param other: another PermutationChromosome instance
        '''
        self_hash = self._index_by_value()
        
        # find all the cycles
        cycles, seen = [], Set()
        for i in xrange(self.size):
            cycle = []
            while i not in seen:
                cycle.append(i)
                seen.add(i)
                
                # move to the index of other.alleles[i] in self.alleles
                if other.alleles[i] not in self_hash:
                    break
                i = self_hash[other.alleles[i]]
                
            # save this cycle
            if cycle:
                cycles.append(cycle)
        
        # build the child permutations
        switch = False
        child1, child2 = list(self.alleles), list(other.alleles)
        for cycle in cycles:
            if switch:
                for i in cycle:
                    child1[i], child2[i] = child2[i], child1[i]
                switch = False
            
            else:
                # do nothing. unswitched cycles are already present!
                switch = True
        
        return type(self)(child1, invariant=True), type(self)(child2, invariant=True)
    
    
    @cached('__index_by_value')
    def _index_by_value(self):
        '''
        Internal method: returns a cached table of allele => index
        '''
        index_by_value = {}
        for i in xrange(self.size):
            index_by_value[self.alleles[i]] = i
        return index_by_value
        

    @cached('__edge_table_')
    def _edge_table(self):
        '''
        Internal method: constructs an edge table from two permutations
        Structure:
            allele -> (Set(edges in one permutation), Set(edges in both))
        '''
        edges = {} 
        for i in xrange(self.size):
            first, second = self.alleles[i], self.alleles[i-1]
            
            if first not in edges:
                edges[first]  = []
            if second not in edges:
                edges[second] = []
            
            edges[first].append(second)
            edges[second].append(first)
         
        return edges
    
    
    def _double_edge_table(self, other):
        '''
        Internal method: returns a hash of edges that are found in both permutations
            
        @param other: another PermutationChromosome instance
        '''
        edges = {}
        other_edges = other._edge_table()
        
        for allele, adjacents in self._edge_table().items():
            for adjacent in adjacents:
                
                if allele in other_edges and adjacent in other_edges[allele]:
                    if allele not in edges:
                        edges[allele] = []
                    edges[allele].append(adjacent)
                    
        return edges
    
    
    def _build_pmx_permutation(self, perm1, perm2, first, second):
        '''
        Internal method: builds tuples for crossover_pmx based on indices
        
        @param perm1: the first permutation
        @param perm2: the second permutation
        @param first: random indices from the first permutation
        @param second: random indices from the second permutation
        '''
        # start the child off with the section from tuple 1 and all else from 
        # tuple2 this eleminates the last step: copying remaining alleles 
        # from tuple2
        tuple1, tuple2 = perm1.alleles, perm2.alleles
        perm2_hash = perm2._index_by_value()
        
        section  = list(tuple1[first:second+1]) # copy this section into the child
        child    = list(tuple2[:first]) + section + list(tuple2[second+1:])
        copied   = Set(section)
        occupied = Set(xrange(first, second+1))

        # for each element in the corresponding segment of other,
        # find any elements that have not been copied
        for i in xrange(first, second+1):
            
            allele = tuple2[i]
            if allele not in copied:
                # start off at the index of self.alleles[i] in other
                j = i
                
                while tuple1[j] in perm2_hash:
                    # and get the element copied in its place from self
                    j = perm2_hash[tuple1[j]]
                    
                    if j not in occupied:
                        # put i into the position of j in other...
                        child[j] = allele
                        occupied.add(j)
                        break
                    
                copied.add(allele)
        
        return child
        

    def _build_ordered_permutation(self, perm1, perm2, first, second):
        '''
        Internal method: builds tuples for crossover_order based on indices

        @param perm1: the first permutation
        @param perm2: the second permutation
        @param first: random indices from the first permutation
        @param second: random indices from the second permutation
        '''
        # middle is the block from tuple1 we put in the same position
        # of the child.  queue has the items from tuple2 in the order
        # we can use them: [items after second + items through second]
        middle = list(perm1.alleles[first:second+1])
        queue  = Queue(perm2.alleles[second+1:] + perm2.alleles[:second+1])
        
        # this fills out the end of the new list w/ items from the queue
        for i in xrange(self.size - second - 1): #@UnusedVariable
            while not queue.empty():
                end_item = queue.dequeue()
                if end_item not in middle:
                    middle.append(end_item)
                    break
        
        # and this puts items from the queue into the beginning
        start = []
        for i in xrange(first): #@UnusedVariable
            while not queue.empty():
                start_item = queue.dequeue()
                if start_item not in middle:
                    start.append(start_item)
                    break

        return start + middle