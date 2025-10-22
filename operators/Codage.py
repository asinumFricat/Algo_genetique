from abc import ABC, abstractmethod
from core.Coordonnees import coordonnees
import numpy as np

class Codage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def code(self, coord: coordonnees):
        pass


class codage_binaire(Codage):
    def __init__(self, taille_mantisse=10, taille_exposant=6):
        # Total size = mantisse + exposant = 16 bits (as requested)
        self.taille_mantisse = taille_mantisse
        self.taille_exposant = taille_exposant
        self.taille_total = taille_mantisse + taille_exposant

    def float_to_bin_mant_exp(self, val, low, high):
        """
        Encode a float val in [low, high] into a binary mantissa + exponent.
        Here simplified:
        - Normalize val to [low, high] range to a positive number
        - Convert integer part to exponent bits
        - Fractional part to mantissa bits
        This is a simplified example of mantisse-exposant binary encoding.
        """

        # Normalize value to positive
        normalized = (val - low) / (high - low)
        # Convert to float scientific notation: val = mantissa * 2^exponent
        if normalized == 0:
            mantissa = 0
            exponent = 0
        else:
            exponent = int(np.floor(np.log2(normalized)))
            mantissa_float = normalized / (2 ** exponent) - 1
            mantissa = int(mantissa_float * (2 ** self.taille_mantisse))
            exponent += 2 ** (self.taille_exposant - 1)  # bias for exponent

        # Clamp exponent and mantissa to bit size
        exponent = max(0, min(exponent, 2**self.taille_exposant - 1))
        mantissa = max(0, min(mantissa, 2**self.taille_mantisse - 1))

        # Convert to binary strings
        exp_bin = format(exponent, f'0{self.taille_exposant}b')
        mant_bin = format(mantissa, f'0{self.taille_mantisse}b')

        return exp_bin + mant_bin

    def codage(self, variables, bornes=None):
        """
        Encode each variable to a fixed-length binary string mantisse+exposant.
        Returns concatenated string of all variables.
        """
        if bornes is None:
            bornes = [(-10, 10)] * len(variables)
        encoded_vars = [
            self.float_to_bin_mant_exp(val, low, high)
            for val, (low, high) in zip(variables, bornes)
        ]
        # Single concatenated string for the individual
        return ''.join(encoded_vars)


class codage_reel(Codage):
    def codage(self, variables):
        variables = [float(variables[i]) for i in range(len(variables))]
        return variables


if __name__ == "__main__":
    x = [1, 2.5, 3, 4.7]
    codagebinaire = codage_binaire()
    print(codagebinaire.codage(x, [(-10, 10)]*len(x)))
