"""
This module contains utilities for Monte Carlo simulation.
"""

import numpy as np


def antithetic_normal(rng, n, scale, out):
    """Generate antithetic normal random numbers into a preallocated array.

    Args:
        rng: a random number generator.
        n: the number of random numbers to generate.
        scale: scaling factor to apply.
        out: the destination array of size 2n.

    Example:
        >>> rng = np.random.default_rng()
        >>> n = 5
        >>> out = np.empty(2 * n, dtype=np.float64)
        >>> antithetic_normal(rng, n, 10.0, out)
        >>> print(out)
        [-26.92756586   9.72017449 -11.28828596  -7.71927495  -3.78729135
        26.92756586  -9.72017449  11.28828596   7.71927495   3.78729135]

    """
    rng.standard_normal(n, out=out[0:n])
    np.multiply(scale, out[0:n], out=out[0:n])
    np.negative(out[0:n], out=out[n:])


if __name__ == "__main__":
    rng = np.random.default_rng()
    n = 5
    out = np.empty(2 * n, dtype=np.float64)
    antithetic_normal(rng, n, 10.0, out)
    print(out)
