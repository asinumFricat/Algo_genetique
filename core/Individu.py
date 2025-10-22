from Coordonnees import coordonnees

import math
import random


class Individual:
    def __init__(self, num_vars, bits_per_var=16, bounds=None):
        self.num_vars = num_vars
        self.bits_per_var = bits_per_var
        self.bounds = bounds or [(-5.0, 5.0)] * num_vars
        self.genotype = ""  # binary string
        self.phenotype = [0.0] * num_vars
        self.fitness = None

        # Mantisse-Exponent coding params
        self.sign_bits = 1
        self.exponent_bits = 5
        self.mantissa_bits = self.bits_per_var - self.sign_bits - self.exponent_bits
        self.exponent_bias = (2 ** (self.exponent_bits - 1)) - 1  # bias for exponent, e.g. 15

    def encode(self, phenotype):
        """Encode list of floats (phenotype) into Mantisse-Exponent binary string."""
        self.genotype = ""
        for i, val in enumerate(phenotype):
            low, high = self.bounds[i]
            val_clamped = max(min(val, high), low)
            bits = self.encode_value(val_clamped)
            self.genotype += bits
        self.decode()  # update phenotype from genotype to be consistent

    def encode_value(self, val):
        """Encode single float value to Mantisse-Exponent binary string (length bits_per_var)."""

        if val == 0:
            return "0" * self.bits_per_var

        sign_bit = "0"
        if val < 0:
            sign_bit = "1"
            val = -val

        exponent = int(math.floor(math.log2(val)))
        mantissa = val / (2 ** exponent)

        biased_exp = exponent + self.exponent_bias

        max_exp = 2 ** self.exponent_bits - 1
        if biased_exp < 0:
            biased_exp = 0
            mantissa = 0
        elif biased_exp > max_exp:
            biased_exp = max_exp
            mantissa = 1.999999

        exp_bits = format(biased_exp, f"0{self.exponent_bits}b")

        frac = mantissa - 1.0
        mant_bits_val = int(frac * (2 ** self.mantissa_bits))
        mant_bits = format(mant_bits_val, f"0{self.mantissa_bits}b")

        return sign_bit + exp_bits + mant_bits

    def decode(self):
        """Decode genotype binary string into phenotype list of floats."""
        self.phenotype = []
        for i in range(self.num_vars):
            start = i * self.bits_per_var
            end = start + self.bits_per_var
            bits = self.genotype[start:end]
            val = self.decode_value(bits)
            low, high = self.bounds[i]
            val_clamped = max(min(val, high), low)
            self.phenotype.append(val_clamped)

    def decode_value(self, bits):
        if len(bits) != self.bits_per_var:
            raise ValueError("Incorrect bits length")

        if bits == "0" * self.bits_per_var:
            return 0.0

        sign_bit = bits[0]
        exp_bits = bits[1 : 1 + self.exponent_bits]
        mant_bits = bits[1 + self.exponent_bits :]

        sign = -1 if sign_bit == "1" else 1
        biased_exp = int(exp_bits, 2)
        mantissa_val = int(mant_bits, 2)

        exponent = biased_exp - self.exponent_bias

        frac = mantissa_val / (2 ** self.mantissa_bits)
        mantissa = 1 + frac

        val = sign * mantissa * (2 ** exponent)
        return val

    def mutate(self, mutation_rate):
        bits = list(self.genotype)
        for i in range(len(bits)):
            if random.random() < mutation_rate:
                bits[i] = "1" if bits[i] == "0" else "0"
        self.genotype = "".join(bits)
        self.decode()

    def crossover(self, other, num_points=2):
        if len(self.genotype) != len(other.genotype):
            raise ValueError("Genotype lengths differ")

        points = sorted(random.sample(range(1, len(self.genotype)), num_points))
        child1_bits = []
        child2_bits = []
        last = 0
        toggle = False
        for point in points + [len(self.genotype)]:
            if not toggle:
                child1_bits.append(self.genotype[last:point])
                child2_bits.append(other.genotype[last:point])
            else:
                child1_bits.append(other.genotype[last:point])
                child2_bits.append(self.genotype[last:point])
            last = point
            toggle = not toggle

        child1 = Individual(self.num_vars, self.bits_per_var, self.bounds)
        child2 = Individual(self.num_vars, self.bits_per_var, self.bounds)
        child1.genotype = "".join(child1_bits)
        child2.genotype = "".join(child2_bits)
        child1.decode()
        child2.decode()
        return [child1, child2]

