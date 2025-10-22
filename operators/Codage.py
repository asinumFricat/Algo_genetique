from abc import ABC, abstractmethod
from core.Coordonnees import coordonnees
import math
import numpy as np


# === Abstract Base Class ===

class Codage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def code(self, coord: coordonnees):
        """
        Fonction qui prends les coordonnées réelles et les encode
        pour pouvoir faire les autres opérations de l'algo génétique
        """


# === Concrete Codage: Mantisse-Exposant (Task 1) ===

class CodageMantisseExposant(Codage):
    """
    Codage en binaire type Mantisse-Exposant pour chaque coordonnée.
    """

    def __init__(self, bits_per_var=16, exponent_bits=5):
        super().__init__()
        self.bits_per_var = bits_per_var
        self.exponent_bits = exponent_bits
        self.sign_bits = 1
        self.mantissa_bits = bits_per_var - exponent_bits - self.sign_bits
        self.bias = (2 ** (exponent_bits - 1)) - 1

    def code(self, coord: coordonnees):
        """
        Encode les coordonnées réelles en binaire avec codage Mantisse/Exposant
        """
        encoded = []
        for val in coord.coordonnees:
            encoded.extend(self.encode_value(val))
        coord.coordonnees_codees = np.array(encoded)

    def encode_value(self, val):
        if val == 0.0:
            return [0] * self.bits_per_var

        sign = 0 if val >= 0 else 1
        val = abs(val)

        exponent = int(math.floor(math.log2(val)))
        mantissa = val / (2 ** exponent)

        biased_exp = exponent + self.bias
        biased_exp = max(0, min(biased_exp, 2 ** self.exponent_bits - 1))
        exp_bits = [int(x) for x in format(biased_exp, f'0{self.exponent_bits}b')]

        frac = mantissa - 1.0
        mant_bits_val = int(frac * (2 ** self.mantissa_bits))
        mant_bits = [int(x) for x in format(mant_bits_val, f'0{self.mantissa_bits}b')]

        return [sign] + exp_bits + mant_bits

    def decode(self, coord: coordonnees):
        if coord.coordonnees_codees is None:
            raise ValueError("Les coordonnées codées sont vides.")

        bits = coord.coordonnees_codees.tolist()
        decoded = []

        for i in range(0, len(bits), self.bits_per_var):
            sub_bits = bits[i:i + self.bits_per_var]
            decoded.append(self.decode_value(sub_bits))

        coord.coordonnees = np.array(decoded)

    def decode_value(self, bits):
        if len(bits) != self.bits_per_var:
            raise ValueError("Longueur de bits incorrecte")

        sign = -1 if bits[0] == 1 else 1
        exp = int("".join(str(b) for b in bits[1:1 + self.exponent_bits]), 2)
        exponent = exp - self.bias

        mantissa_bits = bits[1 + self.exponent_bits:]
        mantissa_val = int("".join(str(b) for b in mantissa_bits), 2)
        mantissa = 1 + mantissa_val / (2 ** self.mantissa_bits)

        return sign * mantissa * (2 ** exponent)


# === Other Codage Stubs (existing) ===

class codage_binaire:
    def codage(self, variables):
        # codage binaire pour chaque élément
        # A IMPLEMENTER
        pass


class codage_reel:
    def codage(self, variables):
        """ "
        Transforme chaque élément de la liste en float
        """
        variables = [float(variables[i]) for i in range(len(variables))]
        return variables


# === Test Block ===

if __name__ == "__main__":
    x = [1, 2.5, 3, 4.7]
    codagereel = codage_reel()
    codagebinaire = codage_binaire()
    print("Codage réel :", codagereel.codage(x))
    print("Codage binaire :", codagebinaire.codage(x))

    # Test MantisseExposant codage
    from core.Coordonnees import coordonnees
    c = coordonnees(np.array([3.14, -2.7, 0.5]))
    coder = CodageMantisseExposant(bits_per_var=16, exponent_bits=5)
    coder.code(c)
    print("Encoded (MantisseExposant):", c.coordonnees_codees)
    coder.decode(c)
    print("Decoded (MantisseExposant):", c.coordonnees)
