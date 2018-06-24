from random import random
from math import log

from .make_random_tree_service import MakeRandomTreeService
from .mutate_service import MutateService
from .crossover_service import CrossoverService


class EvolveService:
    def __init__(self, pc, population_size, rank_function, max_generations=500,
                 mutation_rate=0.1, breeding_rate=0.4, prob_exp=0.7, prob_new=0.05):
        self.pc = pc
        self.population_size = population_size
        self.rank_function = rank_function
        self.max_generations = max_generations
        self.prob_new = prob_new
        self.prob_exp = prob_exp
        self.mutation_rate = mutation_rate
        self.breeding_rate = breeding_rate

    def select_index(self):
        """
        Returns a random number, tending towards lower numbers. The lower pexp is, more lower numbers you will get
        """
        return int(log(random()) / log(self.prob_exp))

    def call(self):
        # Create a random initial population
        population = [MakeRandomTreeService(self.pc).call() for _ in range(self.population_size)]

        for i in range(self.max_generations):
            scores = self.rank_function(population)
            print(scores[0][0])
            if scores[0][0] == 0:
                break

            # The two best always make it
            new_population = [scores[0][1], scores[1][1]]

            # Build the next generation
            while len(new_population) < self.population_size:
                if random() > self.prob_new:
                    new_elem = CrossoverService(scores[self.select_index()][1], scores[self.select_index()][1],
                                                probswap=self.breeding_rate).call()
                    new_elem = MutateService(new_elem, self.pc, probchange=self.mutation_rate).call()
                else:
                    # Add a random node to mix things up
                    new_elem = MakeRandomTreeService(self.pc).call()

                new_population.append(new_elem)

            population = new_population
        scores[0][1].display()
        return scores[0][1]