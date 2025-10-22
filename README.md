# Algo_genetique
Implementation code Algo génétique en Python


Explanation:

The genotype is a single binary string (length = num_vars * bits_per_var).

Encoding normalizes each phenotype float to an integer in [0, 2^bits_per_var - 1].

Decoding does the reverse to recover floats.

mutate() flips bits randomly based on mutation_rate.

crossover() performs multi-point crossover and returns two new Individuals.

fitness is stored but computed externally.
