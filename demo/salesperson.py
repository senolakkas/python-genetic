# Demo program to solve TSP
# $Revision: 1.2 $

from genetics.selectors.randomized import RandomSelector
from Tkinter import Button, Canvas, Tk, mainloop
from genetics.chromosomes.permutation import PermutationChromosome
from genetics.challenge import Challenge
from genetics.population import Population
from genetics.organism import Organism
from genetics.selectors.sampled.ranking import ExponentialRankingSelector
from sets import Set
import math, random


SALES_FORCE = 50
PIXELS = 500
CITIES = Set()


# Step 1: define a challenge that minimizes route distance
class RouteChallenge(Challenge):
    def fitness(self, organism):
        # fitness is length of the route negated
        return -Challenge.fitness(self, organism)

challenge = RouteChallenge()


# Step 2: a route chromosome represents a series of cities to visit
class RouteChromosome(PermutationChromosome):
    def __init__(self, route=None, *args, **kwargs):
        if not route:
            route = list(CITIES)
            random.shuffle(route)
            
        super(RouteChromosome, self).__init__(route, *args, **kwargs)
        
    mutate = PermutationChromosome.mutate_insert
    # TODO: decide on a crossover or use a mutate-only recombination operator
    crossover = PermutationChromosome.crossover_edge
    #def crossover(self, other):
    #    return self, other
    

# Step 3: a salesperson has a route and can measure its travel distance
class Salesperson(Organism):
    def distance(self):
        d = 0
        for i in xrange(self.route.size):
            (x1,y1), (x2, y2) = self.route.alleles[i-1], self.route.alleles[i]
            d += math.sqrt(((x2-x1) ** 2) + ((y2-y1) ** 2))
    
        return d
    
    genotype   = {'route': RouteChromosome}
    phenotypes = {RouteChallenge: distance}
    

# Step 4: decide on selection operators for the population
class SalesForce(Population):
    size = SALES_FORCE
    
    # Mating pool selector
    mating_pool_selector = ExponentialRankingSelector(challenge)
    mating_pool_size     = SALES_FORCE / 2
    
    # Survivor selector
    survivor_selector = RandomSelector(challenge)
    
    # Mutation rate
    mutation = .9
    

# Step 5: create a GUI for the map
class Map(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, bg='gray', width=PIXELS, height=PIXELS)
        self.bind('<Button-1>', self.left_click )
        self.route = None
    
    def left_click (self, event): 
        CITIES.add((event.x, event.y))
        print len(CITIES), 'cities:', CITIES
  
    def update(self, cities):
        if self.route:
            self.delete(self.route)
        
        cities = list(cities)
        cities.append(cities[0])
        self.route = self.create_line(*cities)
        
  
class MapFrame(Tk):
    def __init__(self):
        Tk.__init__(self, className='TSP Solver')
        self.graph = Map(self)
        self.graph.pack()
        
        new    = Button(self, text='New Population', command=self.population)
        cycle  = Button(self, text='+100 Generations', command=self.solve)
        cities = Button(self, text='+10 Cities', command=self.expand)
        
        new.pack(side='left', expand=True, fill='x')
        cycle.pack(side='left', expand=True, fill='x')
        cities.pack(side='left', expand=True, fill='x')
        
    def solve(self):
        if len(CITIES) < 2: 
            print 'Click in the map to generate more cities'
        
        else:
            try:
                last_best = None
                for i in xrange(100): #@UnusedVariable
                    best = self.sales_force.best(challenge)
                    print '>>> population age:', self.sales_force.age, "\tbest id:", best.id, \
                          "\tdistance:", best.decode(challenge)
                    self.sales_force.cycle()
                
                    if best is not last_best:
                        self.graph.update(best.route.alleles)
                        last_best = best
        
            except AttributeError:
                print 'Generate a new population first!'
                
    def population(self):
        if len(CITIES) < 2: 
            print 'Click in the map to generate more cities'
        else:
            self.sales_force = SalesForce(Salesperson)
            self.graph.update(self.sales_force.best(challenge).route.alleles)
                    
    def expand(self):
        for i in range(10): #@UnusedVariable
            CITIES.add((random.randrange(PIXELS), random.randrange(PIXELS)))
        print len(CITIES), 'cities:', CITIES
  
      
if __name__ == '__main__':
    MapFrame()
    mainloop()