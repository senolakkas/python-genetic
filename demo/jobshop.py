# Demo program to solve the job shop scheduling problem
# See Chapter 3 of Eiben & Smith: "Introduction to Evolutionary Computing"
# $Revision: 1.3 $

from genetics.challenge import Challenge
from genetics.chromosomes.permutation import PermutationChromosome
from genetics.organism import Organism
from genetics.population import Population
from genetics.selectors.fitness import FitnessSelector
from genetics.selectors.randomized import RandomSelector
import random, time


NUM_MACHINES    =  10
NUM_OPERATIONS  =  25
MIN_OP_TIME     =   3
MAX_OP_TIME     =  15
NUM_JOBS        = 100
MIN_OPS_PER_JOB =   3
MAX_OPS_PER_JOB =  15


# Step 1: Create a list of machines
class Machine(object):
    def __init__(self):
        self.reset()
    
    def __cmp__(self, other):
        # this is for finding the next available machine
        return cmp(self.busy_until, other.busy_until)
    
    def schedule(self, operation):
        self.busy_until = self.busy_until + operation.time(self)
    
    def reset(self):
        self.busy_until = 0
        
machines = [Machine() for i in xrange(NUM_MACHINES)]


# Step 2: Create a list of operations.  An operation can be performed
#         on a random subset of the machines.
class Operation(object):
    def __init__(self):
        self.machines = random.sample(machines, random.randint(1, NUM_MACHINES))
        self.times = {}
        for machine in self.machines:
            self.times[machine] = random.randint(MIN_OP_TIME, MAX_OP_TIME)

    def time(self, machine):
        return self.times[machine]
    
operations = [Operation() for i in xrange(NUM_OPERATIONS)]


# Step 3: Create a list of jobs.  A job is an ordered sequence of operations.
class Job(object):
    def __init__(self):
        self.operations = random.sample(operations, random.randint(MIN_OPS_PER_JOB, MAX_OPS_PER_JOB))
        
jobs = [Job() for i in xrange(NUM_JOBS)]


# Step 4: Create a scheduling challenge
class ScheduleChallenge(Challenge):
    def fitness(self, organism):
        # fitness is time taken negated
        return -Challenge.fitness(self, organism)

challenge = ScheduleChallenge()


# Step 5: Represent a schedule of jobs
class ScheduleChromosome(PermutationChromosome):
    def __init__(self, schedule=None, *args, **kwargs):
        if not schedule:
            schedule = list(jobs)
            random.shuffle(schedule)
            
        super(ScheduleChromosome, self).__init__(schedule, *args, **kwargs)
        
    mutate    = PermutationChromosome.mutate_insert
    crossover = PermutationChromosome.crossover_order
    
    
# Step 6: Create organisms that can evaluate how much time a schedule takes
class Scheduler(Organism):
    def time(self):
        for m in machines:
            m.reset()
        
        end_time = 0
        
        for job in self.schedule.alleles:
            for operation in job.operations:
        
                # find the earliest available machine to run it on
                operation.machines.sort()
                machine = operation.machines[0]
                machine.schedule(operation)
                
                if machine.busy_until > end_time:
                    end_time = machine.busy_until
        
        return end_time
    
    genotype   = {'schedule': ScheduleChromosome}
    phenotypes = {ScheduleChallenge: time}
    
    
# Step 7: Population numbers
class JobShopPopulation(Population):
    size = 100
    
    # Mating pool selector
    mating_pool_selector = RandomSelector(challenge)
    mating_pool_size     = 4
    
    # Survivor selector
    survivor_selector = FitnessSelector(challenge)
    
    # Mutation rate
    mutation = 0.5
    
    
# Step 8: Create a population and approximate the problem
if __name__ == '__main__':
    start = time.time()
    
    p = JobShopPopulation(Scheduler)
    best = p.solve(challenge, iterations=50)
    print p.age, 'generations, job shop time:', best.decode(challenge)
    
    print 'time:', time.time() - start
