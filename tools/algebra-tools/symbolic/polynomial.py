
from fractions import Fraction
from typing import List


class Polynomial:
    """
    Polynomial Algebra Engine over the rational field Q.

    Coefficients are stored in ascending order:
    [a0, a1, a2] represents a0 + a1*x + a2*x^2
    """

    def __init__(self, coefficients):
        self.coeffs = [Fraction(c) for c in coefficients]
        self._normalize()

    def _normalize(self):
        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()

    @property
    def degree(self):
        return -1 if self.coeffs == [0] else len(self.coeffs) - 1

    # Addition
    def __add__(self, other):
        n = max(len(self.coeffs), len(other.coeffs))
        result = []

        for i in range(n):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            result.append(a + b)

        return Polynomial(result)

    # Subtraction
    def __sub__(self, other):
        return self + (-other)

    # Negation
    def __neg__(self):
        return Polynomial([-c for c in self.coeffs])

    # Multiplication
    def __mul__(self, other):
        result = [Fraction(0)] * (
            len(self.coeffs) + len(other.coeffs) - 1
        )

        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                result[i + j] += a * b

        return Polynomial(result)

    # Scalar multiplication
    def scale(self, scalar):
        return Polynomial([scalar * c for c in self.coeffs])

    # Horner's method
    def evaluate(self, x):
        result = Fraction(0)
        x = Fraction(x)

        for coefficient in reversed(self.coeffs):
            result = result * x + coefficient

        return result

    # Formal derivative
    def derivative(self):
        if self.degree <= 0:
            return Polynomial([0])

        return Polynomial([
            i * self.coeffs[i]
            for i in range(1, len(self.coeffs))
        ])

    # Indefinite integral (constant of integration = 0)
    def integrate(self):
        result = [Fraction(0)]

        for i, coefficient in enumerate(self.coeffs):
            result.append(coefficient / (i + 1))

        return Polynomial(result)

    # Polynomial long division
    def divmod(self, divisor):
        if divisor.degree < 0:
            raise ZeroDivisionError("Division by zero polynomial")

        remainder = Polynomial(self.coeffs)
        quotient = Polynomial([0])

        while remainder.degree >= divisor.degree:
            coefficient = (
                remainder.coeffs[-1] / divisor.coeffs[-1]
            )

            power = remainder.degree - divisor.degree

            term_coeffs = [0] * power + [coefficient]
            term = Polynomial(term_coeffs)

            quotient = quotient + term
            remainder = remainder - (term * divisor)

        return quotient, remainder

    # Euclidean algorithm
    def gcd(self, other):
        a, b = self, other

        while b.degree >= 0:
            _, remainder = a.divmod(b)
            a, b = b, remainder

        if a.degree >= 0:
            return a.scale(1 / a.coeffs[-1])

        return Polynomial([0])

    # Polynomial composition: P(Q(x))
    def compose(self, other):
        result = Polynomial([0])

        for coefficient in reversed(self.coeffs):
            result = result * other + Polynomial([coefficient])

        return result

    # String representation
    def __str__(self):
        if self.degree < 0:
            return "0"

        terms = []

        for power, coefficient in enumerate(self.coeffs):
            if coefficient == 0:
                continue

            if power == 0:
                term = str(coefficient)
            elif power == 1:
                term = f"{coefficient}x"
            else:
                term = f"{coefficient}x^{power}"

            terms.append(term)

        return " + ".join(reversed(terms)).replace("+ -", "- ")


# Lagrange interpolation
def lagrange_interpolation(points):
    """
    Construct a polynomial passing through given (x, y) points.
    """

    result = Polynomial([0])

    for i, (xi, yi) in enumerate(points):
        basis = Polynomial([1])
        denominator = Fraction(1)

        for j, (xj, _) in enumerate(points):
            if i == j:
                continue

            basis = basis * Polynomial([-xj, 1])
            denominator *= Fraction(xi) - Fraction(xj)

        if denominator == 0:
            raise ValueError("Interpolation x-values must be distinct")

        result += basis.scale(Fraction(yi) / denominator)

    return result


# Demonstration
if __name__ == "__main__":

    P = Polynomial([1, -2, 3])
    Q = Polynomial([2, 1])

    print("P(x):", P)
    print("Q(x):", Q)

    print("\nAddition:", P + Q)
    print("Subtraction:", P - Q)
    print("Multiplication:", P * Q)

    quotient, remainder = P.divmod(Q)

    print("\nQuotient:", quotient)
    print("Remainder:", remainder)

    print("\nDerivative:", P.derivative())
    print("Integral:", P.integrate())

    print("\nP(2):", P.evaluate(2))
    print("Composition:", P.compose(Q))
    print("GCD:", P.gcd(Q))

    points = [(0, 1), (1, 2), (2, 5)]

    interpolated = lagrange_interpolation(points)

    print("\nInterpolated polynomial:", interpolated)
