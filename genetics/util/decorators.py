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
# $Revision: 1.9 $

from threading import Lock


def virtual(method):
    '''
    Declares a method as virtual so that extending classes must implement it.
    This is done by raising a NotImplementedError and prepending 'Virtual
    Method' onto the doc string.
    
    @param method: method to mark as virtual
    '''
    def wrapper(self, *args, **kwargs): #@UnusedVariable
        raise NotImplementedError('%s not implemented for %s' % (method.__name__, type(self)))
    
        wrapper.__doc__ = 'Virtual Method: ' + method.__doc__
    return wrapper


def synchronized(method):
    '''
    Decorator to synchronize a method.  This is only here until python
    inevitably provides one.
    
        @synchronized
        def foo(self, bar):
            return bar.baz
    '''
    method.lock = Lock()
    
    def wrapper(self, *args, **kwargs):
        try:
            method.lock.acquire()
            return method(self, *args, **kwargs)
        finally:
            method.lock.release()

    wrapper.__doc__ = method.__doc__
    return wrapper
    
    
def comparable(method):
    '''
    Decorator for __cmp__ and crossover methods to throw a TypeError 
    if an instance of one type is compared to or recombined with an
    instance of some other type.
    
        @comparable
        def __cmp__(self, other):
            return cmp(self.foo, other.foo)
    '''
    def wrapper(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('%s is not of the same type as %s' % (other, self))
        return method(self, other)
        
    wrapper.__doc__ = method.__doc__
    return wrapper
    
    
def tuple_crossover(method):
    '''
    Decorator for tuple-based chromosomes that need to check that self
    and other are the same type and the same size.  It also handles returning
    empty chromosomes if there are no alleles in the tuple and chromosomes
    that are the same as the parents if the tuple size is one.
    
        @tuple_crossover
        def crossover_foo(self, other):
            ...
            return new children
    '''
    @comparable
    def wrapper(self, other):
        if self.size != other.size:
            raise ValueError('%s and %s are not of the same size' % (self, other))
        
        if self.size > 1:
            return method(self, other)
        else:
            return type(self)(self.alleles), type(self)(other.alleles)
    
    wrapper.__doc__ = method.__doc__
    return wrapper


def cached(name):
    '''
    Decorator for caching the return value of an instance level method in self.
    Assumes that there are no arguments passed to the method (not memoization).
    Pass in the name to use for storing the return value in self.__dict__.
    
        @cached('cached_name')
        def _get_something(self):
            ...
            return 'something'
        
    @param name: name to cache the return value in on self
    '''
    def decorator(method):
        def wrapper(self):
            try:
              return self.__dict__[name]
          
            except KeyError:
                self.__dict__[name] = method(self)
                return self.__dict__[name]
    
        # TODO: this doesn't work...
        wrapper.__doc__ = method.__doc__
        return wrapper
    
    return decorator


def memoize(name):
    '''
    Memoizes a function by the first argument passed in (referred to as the key).
    Remaining *args and **kwargs are passed in on the first call, but are not
    involved in the caching.  The cache is stored on self.name.
    
        @memoize('cached_name')
        def _get_something(self, key):
            ...
            return 'something'
        
    @param name: name to cache the return values in on self
    '''
    def decorator(method):
        def wrapper(self, key, *args, **kwargs):
            try:
                return self.__dict__[name][key]
            
            except KeyError:
                if name not in self.__dict__:
                    self.__dict__[name] = {}
                self.__dict__[name][key] = method(self, key, *args, **kwargs)
                return self.__dict__[name][key]
                
        # TODO: this doesn't work...
        wrapper.__doc__ = method.__doc__
        return wrapper

    return decorator