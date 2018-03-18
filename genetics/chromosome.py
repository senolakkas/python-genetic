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


class Chromosome(object):
    '''
    This is an abstract base class for all Chromosomes.  Standard chromosomes 
    that extend this class are provided in genetics.chromosomes.*
    
    A Chromosome must implement:
        def __init__(self, *args, **kwargs): ...
        def __cmp__(self, other): ...
        def mutate(self): ...
        def crossover(self, other): ...
    '''
    @virtual
    def __init__(self, *args, **kwargs):
        '''
        Ensures that a new Chromosome can be created without arguments.
        '''
        pass
    
    
    @virtual
    def __cmp__(self, other): #@UnusedVariable
        '''
        Compares two Chromosome instances.
        
        @param other: chromosome to compare against
        '''
        pass


    @virtual
    def mutate(self):
        '''
        Returns a new Chromosome instance that is a mutation of this one.
        '''
        pass
        
    
    @virtual
    def crossover(self, other): #@UnusedVariable
        '''
        Returns a tuple of two children that are unlike their parents.
        
        @param other: chromosome to compare against
        '''
        pass