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


class Queue(object):
    '''
    An unsynchronized queue object
    '''
    def __init__(self, items):
        '''
        Initializes a queue
        
        @param items: initial items on the queue
        '''
        self._items = list(items)
        
        
    def enqueue(self, item):
        '''
        Adds an item to the back of the queue
        
        @param item: item to enqueue
        '''
        self._items.append(item)
        
        
    def dequeue(self):
        '''
        Removes the first item from the queue and returns it
        '''
        item = self._items[0]
        del self._items[0]
        return item
    
    
    def empty(self):
        '''
        Determines if the queue is empty
        '''
        return len(self._items) <= 0