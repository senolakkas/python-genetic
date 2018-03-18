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

from genetics.selectors.fitness import FitnessSelector
from genetics.util.decorators import synchronized
import random, sys


class Population(object):
    '''
    Defines a population of organisms.  A population must define, for example:
        
        # Population size
        size = 100
    
        # Mating pool selector
        mating_pool_selector = RandomSelector(challenge)
        mating_pool_size = 10
    
        # Survivor selector
        survivor_selector = FitnessSelector(challenge)
        
        # Only required for crossover with mutation variance (default)
        mutation = 0.5 # Mutation rate

    population.sort() sorts the organism list.  This is a link to the
    sort method, so it accepts the normal arguments.
    '''
    size     =   0 # population size (assumed constant)
    mutation = 0.0 # mutation rate

    mating_pool_selector = None # Selector instance for the mating pool
    mating_pool_size     =    0 # size of the mating pool
    survivor_selector    = None # Selector instance for the next generation
    
   
    def __init__(self, type, organisms=None):
        '''
        Initializes a random population:

        @param type: a class than inherits from Organism
        @param organisms: a pre-populated list of organisms to start with
        '''
        if self.size < 1:
            raise ValueError('population size must be greater than 0')

        if not self.mating_pool_selector:
            raise ValueError('a mating_pool_selector is required')
            
        if self.mating_pool_size < 1:
            raise ValueError('mating_pool_size must be greater than 0')
            
        if not self.survivor_selector:
            raise ValueError('a survivor_selector is required')
        
        # a population generates its first generation on instantiation
        if organisms:
            if len(organisms) != self.size:
                raise ValueError('initial list of organisms is the wrong size')
        else:
            organisms = [type() for i in xrange(self.size)] #@UnusedVariable
        
        self.organisms = organisms
        self.age       = 1
        
        # sorting a population means sorting its list or organisms
        self.sort = self.organisms.sort
        
        
    def __len__(self):
        '''
        Maps the length to self.size
        '''
        return self.size
    
    
    def __getitem__(self, key):
        '''
        Allows one to pull organisms directly from a population:
            population[5], population[2:10], etc.
        
        @param key: index
        '''
        return self.organisms[key]
        
        
    def __iter__(self):
        '''
        Allows one to iterate over the organisms in a population:
            for organism in population:
                ...
        '''
        return (organism for organism in self.organisms)
    
    
    _fitness_selectors = {}
    def best(self, challenge, n=1, organisms=None):
        '''
        Returns either the most fit item for a given challenge or a list of the 
        most fit n items (set by the variable n).  Internally this sorts the 
        list of organisms.  Raises an IndexError if there are not enough 
        organisms to select from.
        
        The challenge argument must be an instance of Challenge.
         
        If a list of organisms is provided, this will return the best of those,
        otherwise it will return the best of the population.
        
        @param challenge: the challenge to evaluate by
        @param n: number of organisms
        @param organisms: organisms or Population instance to pull from
        '''
        if not organisms:
            organisms = self.organisms
        
        if challenge not in self._fitness_selectors:
            self._fitness_selectors[challenge] = FitnessSelector(challenge)
        top = self._fitness_selectors[challenge].select(n, organisms)
        
        if n == 1:
            return top[0]
        else:
            return top
        
    
    def random(self, num=2, organisms=None):
        '''
        Returns a list of random organisms from the population, pulled without 
        replacement. Raises a ValueError if there are not enough organisms to 
        select from.
        
        @param num: number of organisms to select (default=2) 
        @param organisms: list of organisms to select from
        '''
        if not organisms:
            organisms = self.organisms

        return random.sample(organisms, num)
    
    
    @synchronized
    def cycle(self):
        '''
        Recombines random parents into a given number of children, adds those 
        children to the population, and removes the least fit members.  
        Population size is kept constant.
        '''
        # increment the age of each organism
        for org in self.organisms: #@UnusedVariable - TODO: file bug in PyDev
            org.age += 1            
        
        self.vary()
        
        # select the next generation
        self.organisms = self.survivor_selector.select(
           self.size, population=self.organisms)
        self.age += 1
        
        
    @synchronized
    def solve(self, challenge, iterations=sys.maxint):
        '''
        Cycles a population against a problem until its best representative either reaches
        a minimum level of fitness (decided by the challenge) or a maximum number of iterations
        have been reached.  By default that number is sys.maxint.
        
        Returns the best representative organism.
        
        @param challenge: the Challenge to solve
        @param iterations: maximum number of iterations to try
        '''
        best = None
        self.age = 1
        for i in xrange(iterations - 1): #@UnusedVariable
            best = self.best(challenge)
            
            #print '>>> population age:', self.age, "\tid:", best.id, \
            #    "\tdecoded:", best.decode(challenge)
            
            if challenge.solved(best):
                break
            
            self.cycle()
        
        return best


    def vary(self):
        '''
        Default variation operator: uses crossover on pairs of parents
        and then mutates the children based on the mutation rate.  If
        one desires to use mutate- or crossover-only variation, all
        that is necessary is to redefine population.vary (see vary_mutate
        and vary_crossover).
        
        Requires mutation rate to be set between 0.0 and 1.0
        '''
        if self.mutation < 0.00 or self.mutation > 1.00:
            raise ValueError('mutation rate must be between 0.00 and 1.00')
        
        # select the mating pool
        parents = self.mating_pool_selector.select(
           self.mating_pool_size, population=self.organisms)
        
        # randomly mate from the parents and add children to the population
        while parents:
            # get a first parent
            parent1_index = random.randrange(len(parents))
            
            parent1       = parents[parent1_index]
            del parents[parent1_index]
            
            if parents:
                # get a second parent
                parent2_index = random.randrange(len(parents))
                parent2       = parents[parent2_index]
                del parents[parent2_index]
                
                for child in parent1.crossover(parent2):
                    # figure out if we need to mutate the offspring
                    if random.random() < self.mutation:
                        self.organisms.append(child.mutate())
                    else:
                        self.organisms.append(child)    

    
    def vary_mutate(self):
        '''
        Mutate-only variation operator: selects the mating pool and
        then mutates each parent into a child organism.
        '''
        # select the mating pool
        parents = self.mating_pool_selector.select(
           self.mating_pool_size, population=self.organisms)
        
        self.organisms.extend([parent.mutate() for parent in parents])    

    
    def vary_crossover(self):
        '''
        Crossover-only variation operator: selects the mating pool
        and generates children from pairs of parents.
        '''
        # select the mating pool
        parents = self.mating_pool_selector.select(
           self.mating_pool_size, population=self.organisms)
        
        # randomly mate from the parents and add children to the population
        while parents:
            # get a first parent
            parent1_index = random.randrange(len(parents))
            
            parent1       = parents[parent1_index]
            del parents[parent1_index]
            
            if parents:
                # get a second parent
                parent2_index = random.randrange(len(parents))
                parent2       = parents[parent2_index]
                del parents[parent2_index]
                
                self.organisms.extend(parent1.crossover(parent2))