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
# $Revision: 1.4 $

from genetics.selector import Selector
from genetics.selectors.randomized import RandomSelector


class TournamentSelector(Selector):
    '''
    Tournament Selector
    Pits organisms against each other for selection, 
    but does not evaluate fitness universally.
    
    Populations that use this selector must define provide a size
    and must define a __cmp__ method on their Organism class.
    '''
    def __init__(self, challenge, size):
        '''
        Constructs a tournament instance with the tournament size
        
        @param challenge: the challenge instance for fitness evaluation
        @param size: the number of organisms entered in the tournament
        '''
        self.size = size
        self.random_selector = RandomSelector(challenge)
        super(TournamentSelector, self).__init__(challenge)

    
    def select(self, n, population):
        '''
        Selects n organisms from the population by tournaments.
        For each organism selected, self.size organisms are
        pulled randomly from the population.  They are compared
        in pairs using Organism.__cmp__, and the winner of
        the tournament is put into the returned list.

        @param n: number of organisms to select
        @param population: a Population instance or a list of organisms
        '''
        return [self.compete(self.random_selector.select(self.size, population))
                for i in xrange(n)] #@UnusedVariable
    
    
    def compete(self, list=[]):
        '''
        Weeds out all but one organism from a list but comparing
        them in pairs, then only allowing the best of each pair
        to continue.  This only runs O(n) comparisons to find the
        winner of the tournament.
        
        @param list: organisms to compete in the tournament
        '''
        while True:
            # stop if we have a winner
            if len(list) <= 1:
                return list[0]
            
            new_list = []
            for i in xrange(0, len(list), 2):
                try :
                    # work on the list in pairs
                    j = i + 1
                    if list[i] > list[j]:
                        new_list.append(list[i])
                    else:
                        new_list.append(list[j])
        
                except IndexError:
                    # if there is only one organism remaining, go
                    # ahead and move it on to the next round
                    new_list.append(list[i])
    
            list = new_list