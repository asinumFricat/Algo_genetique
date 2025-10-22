from Individu import Individual

import random
from typing import List
from collections import Counter
from ga.individual import Individual  # assuming Individual is in ga/individual.py


class Population:
    def __init__(
        self,
        size: int,
        individual_params: dict,
        mutation_rate: float,
        crossover_points: int,
        benchmark_function,
        optimization_goal: int = 1,  # +1=minimization, -1=maximization
    ):
        self.size = size
        self.individual_params = individual_params
        self.mutation_rate = mutation_rate
        self.crossover_points = crossover_points
        self.benchmark_function = benchmark_function
        self.optimization_goal = optimization_goal

        self.individuals: List[Individual] = []

    def generate_initial_population(self):
        """Generate initial population uniformly respecting bounds."""
        self.individuals = []
        num_vars = self.individual_params["num_vars"]
        bounds = self.individual_params.get("bounds", [(-5.0, 5.0)] * num_vars)

        for _ in range(self.size):
            phenotype = []
            for i in range(num_vars):
                low, high = bounds[i]
                # Uniform random float within bounds
                val = random.uniform(low, high)
                phenotype.append(val)
            indiv = Individual(
                num_vars=num_vars,
                bits_per_var=self.individual_params.get("bits_per_var", 16),
                bounds=bounds,
            )
            indiv.encode(phenotype)
            self.individuals.append(indiv)

        self.evaluate_fitness()

    def evaluate_fitness(self):
        """Evaluate fitness of all individuals using benchmark function and optimization goal."""
        for indiv in self.individuals:
            val = self.benchmark_function(indiv.phenotype)
            indiv.fitness = self.optimization_goal * val

    def select_parents(self) -> List[Individual]:
        """Select two parents randomly (can be replaced with tournament)."""
        return random.sample(self.individuals, 2)

    def survival_selection(self, candidates: List[Individual]) -> List[Individual]:
        """
        Select 2 survivors from 4 candidates (parents + children) probabilistically
        weighted by fitness (lower fitness better for minimization).
        To reduce determinism, we convert fitness to probabilities.
        """
        assert len(candidates) == 4

        # Convert fitness to positive scores for selection (lower fitness = higher score)
        # Add small epsilon to avoid zero division
        fitness_vals = [c.fitness for c in candidates]
        max_fit = max(fitness_vals)
        min_fit = min(fitness_vals)
        epsilon = 1e-8

        # For minimization, better fitness is lower; transform so higher score = better chance
        if self.optimization_goal == 1:
            scores = [max_fit - f + epsilon for f in fitness_vals]
        else:  # maximization
            scores = [f - min_fit + epsilon for f in fitness_vals]

        total = sum(scores)
        probabilities = [s / total for s in scores]

        selected = random.choices(candidates, weights=probabilities, k=2)
        # Avoid duplicates
        if selected[0] == selected[1]:
            selected = list(set(selected))
            while len(selected) < 2:
                candidate = random.choices(candidates, weights=probabilities, k=1)[0]
                if candidate not in selected:
                    selected.append(candidate)
        return selected

    def is_degenerate(self, threshold: float = 0.95) -> bool:
        """
        Check if population is degenerate based on genotype similarity.
        If too many individuals have identical genotypes, return True.
        """
        genotypes = [indiv.genotype for indiv in self.individuals]
        counts = Counter(genotypes)
        most_common_ratio = counts.most_common(1)[0][1] / self.size
        return most_common_ratio > threshold

    def refill_population(self, survivors: List[Individual]):
        """
        If population degenerate, keep best individual + some survivors
        and fill rest with new random individuals.
        """
        num_to_keep = max(1, int(self.size * 0.5))  # keep 50% survivors + best
        survivors = sorted(survivors, key=lambda ind: ind.fitness)  # best first (minimization)
        best = survivors[0]
        kept = survivors[:num_to_keep]

        num_to_generate = self.size - len(kept)
        new_inds = []
        num_vars = self.individual_params["num_vars"]
        bounds = self.individual_params.get("bounds", [(-5.0, 5.0)] * num_vars)

        for _ in range(num_to_generate):
            phenotype = []
            for i in range(num_vars):
                low, high = bounds[i]
                val = random.uniform(low, high)
                phenotype.append(val)
            indiv = Individual(
                num_vars=num_vars,
                bits_per_var=self.individual_params.get("bits_per_var", 16),
                bounds=bounds,
            )
            indiv.encode(phenotype)
            new_inds.append(indiv)
        self.individuals = kept + new_inds
        self.evaluate_fitness()

    def evolve_one_generation(self):
        """
        One generation step following:
        - select parents
        - crossover (fixed multi-point)
        - mutation
        - evaluate children
        - select 2 among father,mother,child1,child2 probabilistically
        - replace parents in population
        - check degeneracy and refill if needed
        """
        new_population = []

        # Shuffle population for pairing
        random.shuffle(self.individuals)
        pairs = [
            (self.individuals[i], self.individuals[i + 1])
            for i in range(0, self.size - 1, 2)
        ]

        for father, mother in pairs:
            # Crossover
            children = father.crossover(mother, num_points=self.crossover_points)

            # Mutation
            for child in children:
                child.mutate(self.mutation_rate)
                child.decode()
                child.fitness = self.optimization_goal * self.benchmark_function(
                    child.phenotype
                )

            # Select survivors among father,mother,child1,child2
            candidates = [father, mother] + children
            survivors = self.survival_selection(candidates)
            new_population.extend(survivors)

        # If odd population size, add random individual
        while len(new_population) < self.size:
            num_vars = self.individual_params["num_vars"]
            bounds = self.individual_params.get("bounds", [(-5.0, 5.0)] * num_vars)
            phenotype = [
                random.uniform(bounds[i][0], bounds[i][1]) for i in range(num_vars)
            ]
            indiv = Individual(
                num_vars=num_vars,
                bits_per_var=self.individual_params.get("bits_per_var", 16),
                bounds=bounds,
            )
            indiv.encode(phenotype)
            indiv.fitness = self.optimization_goal * self.benchmark_function(
                phenotype
            )
            new_population.append(indiv)

        self.individuals = new_population

        # Check degeneracy
        if self.is_degenerate():
            # Keep best and refill population
            self.refill_population(self.individuals)

        self.evaluate_fitness()
