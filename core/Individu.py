from Coordonnees import coordonnees

from typing import List
import random

class Individual:
    def __init__(self, num_vars: int, bits_per_var: int = 16, bounds: List[tuple] = None):
        """
        Args:
            num_vars: Number of variables (dimensions).
            bits_per_var: Number of bits encoding each variable.
            bounds: List of (min, max) tuples for each variable.
        """
        self.num_vars = num_vars
        self.bits_per_var = bits_per_var
        self.bounds = bounds if bounds else [(-5.0, 5.0)] * num_vars

        self.genotype = ""  # binary string of length num_vars * bits_per_var
        self.phenotype = [0.0] * num_vars  # decoded float values
        self.fitness = None  # To be set externally

    def encode(self, phenotype: List[float]) -> None:
        """Encode phenotype (floats) into binary genotype string."""
        genotype_bits = []
        for i, val in enumerate(phenotype):
            min_b, max_b = self.bounds[i]
            # Clamp value within bounds
            val_clamped = max(min_b, min(max_b, val))

            # Normalize val to [0, 2^bits_per_var - 1]
            max_int = 2 ** self.bits_per_var - 1
            normalized = int(round((val_clamped - min_b) / (max_b - min_b) * max_int))
            # Format as zero-padded binary string
            bin_str = format(normalized, f'0{self.bits_per_var}b')
            genotype_bits.append(bin_str)
        self.genotype = "".join(genotype_bits)
        self.phenotype = phenotype.copy()

    def decode(self) -> List[float]:
        """Decode genotype binary string into phenotype floats."""
        phenotype = []
        max_int = 2 ** self.bits_per_var - 1
        for i in range(self.num_vars):
            start = i * self.bits_per_var
            end = start + self.bits_per_var
            gene_bits = self.genotype[start:end]
            intval = int(gene_bits, 2)
            min_b, max_b = self.bounds[i]
            val = min_b + (intval / max_int) * (max_b - min_b)
            phenotype.append(val)
        self.phenotype = phenotype
        return phenotype

    def mutate(self, mutation_rate: float) -> None:
        """Bit-flip mutation on genotype string with given mutation_rate per bit."""
        new_bits = []
        for bit in self.genotype:
            if random.random() < mutation_rate:
                new_bits.append('1' if bit == '0' else '0')
            else:
                new_bits.append(bit)
        self.genotype = "".join(new_bits)
        self.decode()  # update phenotype after mutation

    def crossover(self, other: 'Individual', num_points: int = 2) -> List['Individual']:
        """Perform multi-point crossover with another individual.
        
        Args:
            other: Another Individual instance.
            num_points: Number of crossover points.
        
        Returns:
            Two offspring Individuals.
        """
        assert self.num_vars == other.num_vars
        assert self.bits_per_var == other.bits_per_var
        length = len(self.genotype)
        points = sorted(random.sample(range(1, length), num_points))
        
        # Build offspring genotypes by alternating segments
        offspring1_bits = []
        offspring2_bits = []
        last = 0
        toggle = False
        for point in points + [length]:
            if not toggle:
                offspring1_bits.append(self.genotype[last:point])
                offspring2_bits.append(other.genotype[last:point])
            else:
                offspring1_bits.append(other.genotype[last:point])
                offspring2_bits.append(self.genotype[last:point])
            last = point
            toggle = not toggle

        child1 = Individual(self.num_vars, self.bits_per_var, self.bounds)
        child1.genotype = "".join(offspring1_bits)
        child1.decode()

        child2 = Individual(self.num_vars, self.bits_per_var, self.bounds)
        child2.genotype = "".join(offspring2_bits)
        child2.decode()

        return [child1, child2]

    def __repr__(self):
        return (f"Individual(genotype='{self.genotype[:20]}...', "
                f"phenotype={self.phenotype}, fitness={self.fitness})")
