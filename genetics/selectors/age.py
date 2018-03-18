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


class AgeSelector(Selector):
    '''
    Selector for choosing organisms by age.
    '''
    def select(self, n, population):
        '''
        Selects the n youngest organisms from self.population.
        
        @param n: number of organisms to select
        @param population: a Population instance or a list of organisms
        '''
        def cmp_age(x, y):
            return cmp(x.age, y.age)
        
        population.sort(cmp=cmp_age)
        return population[:n]