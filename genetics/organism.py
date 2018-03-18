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

from genetics.chromosome import Chromosome
from genetics.util.decorators import comparable, memoize, synchronized, virtual


class Organism(object):
    '''
    This class defines an organism.  Organisms contain a genotype 
        genotype = {name: chromosome, ...}
    and a mapping from challenges to phenotype decoder functions 
        phenotypes = {challenge class: function, ...}
    based on those genotypes.
    
    Note that an organism should be immutable.  New organisms are created by 
    mutation and recombination.  This means that the phenotype for an organism
    should not change as long as the environment remains the same.
    '''    
    genotype   = {}
    phenotypes = {}

    # Keep track of the ID for each organism instance
    id = 0
    
    
    @synchronized
    def __next_id__(self):
        '''
        Increments the ID of the organism's class and returns it
        '''
        type(self).id += 1
        return type(self).id


    def __init__(self, genotype=None, *args, **kwargs):
        '''
        Creates a new organism, with a new instance of each chromosom in its 
        genotype.  An organism must define a class level genotype as a hash of
        classes that derive from Chromosome.  The keys will be set on the 
        Organism instance.
        
        Any class that inherits from Organism and overrides __init__ must call
        Organism.__init__ and must accept *args & **kwargs in its constructor:
            
            class MyOrganism(Organism):
                def __init__(self, bar='baz', *args, **kwargs):
                    self.baz = bar
                    super(MyOrganism, self).__init__(*args, **kwargs)
        
        @param genotype: a pre-built genotype for the organism
        '''
        if not genotype:
            genotype = {}
            
            # create a new genotype for the instance
            for name, chromosome_class in self.genotype.items():
                # make sure chromosome_class inherits from Chromosome
                # before instantiating it
                if not issubclass(chromosome_class, Chromosome):
                    raise TypeError('%s does not inherit from Chromosome' \
                        % chromosome_class)

                chromosome = chromosome_class()
                genotype[name] = chromosome

        for name, chromosome in genotype.items():
            # make sure it isn't already set
            if name in self.__dict__:
                raise ValueError('%s is already set on the organism' % name)
            
            # set the chromosome in the genotype dict and on the instance
            self.__dict__[name] = chromosome
        
        # set the id of this organism for its class.  organisms are 1-indexed
        self.id = self.__next_id__()

        # store the age of the organism
        self.age = 1


    @virtual
    def __cmp__(self, other): #@UnusedVariable
        '''
        Compares two organisms. Implement this for tournament selection.
        
        @param other: the organism to compare against
        '''
        pass
    

    def __repr__(self):
        '''
        Returns a string akin to Class: ID
        '''
        return '%s: %s' % (type(self), self.id)
        
    
    @memoize('_decoded_phenotypes')
    def decode(self, challenge, *args, **kwargs):
        '''
        Decodes the organisms genotype into a phenotype for a given problem.  
        Arguments should be passed in from the environment.  Since organisms 
        are immutable, there should be one phenotype per organism for a given 
        problem.
        
        Decoders for an organism can be specified by either Challenge instances 
        or classes, but are cached by instance.
        
        @param challenge: the challenge instance to decode against
        '''
        # see if the phenotype for this problem has already been decoded
        if challenge in self._decoded_phenotypes:
            return self._decoded_phenotypes[challenge]

        # do we have a method for decoding this phenotype?
        challenge_class, decoder = type(challenge), None
        
        if challenge in self.phenotypes:
            decoder = self.phenotypes[challenge]
        elif challenge_class in self.phenotypes:
            decoder = self.phenotypes[challenge_class]
        else:
            raise NotImplementedError('%s has no decoder for %s' % \
                (type(self), challenge))
        
        # cache the decoded phenotype
        phenotype = decoder(self, *args, **kwargs)
        self._decoded_phenotypes[challenge] = phenotype
        return phenotype
    

    def mutate(self):
        '''
        Returns a mutation of the current organism by calling mutate() on each 
        chromosome.  If a class that inherits from Organism changes the 
        signature of __init__, then it will also need to override mutate.
        '''
        new_genotype = {}
        for name in self.genotype:
            new_genotype[name] = self.__dict__[name].mutate()
            
        return type(self)(genotype=new_genotype)

    
    @comparable
    def crossover(self, other):
        '''
        Returns a tuple containing two children that are recombined from their
        parents.  These children are not the same as their parents and each 
        chromosome is subjected to a crossover.
        
        @param other: a second parent
        '''
        child1, child2 = {}, {}
        
        # for now child 1 will take the first chromosomes and 
        # child 2 will take the second
        for name in self.genotype:
            child1[name], child2[name] = self.__dict__[name].crossover(
               other.__dict__[name])

        return type(self)(genotype=child1), type(self)(genotype=child2)    