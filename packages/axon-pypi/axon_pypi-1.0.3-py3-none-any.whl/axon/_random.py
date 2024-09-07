import random
import math

class Random:
  def __init__(self, seed=None):
    self.seed(seed)

  def seed(self, seed=None):
    random.seed(seed)

  def randint(self, low, high=None, size=None):
    """
    Return random integers from `low` (inclusive) to `high` (exclusive).
    If high is None, then return integers from 0 to `low`.
    """
    if high is None:
      high = low
      low = 0
    return self._generate_random(lambda: random.randint(low, high - 1), size)

  def rand(self, *size):
    """
    Generate random float numbers between 0 and 1. Works like np.random.rand.
    """
    return self._generate_random(random.random, size)

  def uniform(self, low=0.0, high=1.0, size=None):
    """
    Return random floats in the half-open interval [low, high).
    """
    return self._generate_random(lambda: random.uniform(low, high), size)

  def randn(self, *size):
    """
    Generate random numbers from a standard normal distribution using Box-Muller transform.
    """
    def box_muller():
      u1 = random.random()
      u2 = random.random()
      z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
      return z0
    return self._generate_random(box_muller, size)

  def choice(self, a, size=None, replace=True):
    """
    Generate a random sample from a given 1D array `a`.
    If replace is False, it generates without replacement.
    """
    if not replace and size > len(a):
      raise ValueError("Cannot take a larger sample than population when 'replace=False'")
    
    if replace:
      return self._generate_random(lambda: random.choice(a), size)
    else:
      return random.sample(a, size)

  def _generate_random(self, func, size):
    """
    Utility function to generate random numbers with or without shape.
    If `size` is None, a single random value is returned.
    """
    if size is None:
      return func()
    if isinstance(size, int):
      return [func() for _ in range(size)]
    elif isinstance(size, tuple):
      return self._nested_list(func, size)
    else:
      raise ValueError(f"Invalid size: {size}")

  def _nested_list(self, func, shape):
    """
    Recursively create a nested list with the given shape.
    """
    if len(shape) == 1:
      return [func() for _ in range(shape[0])]
    else:
      return [self._nested_list(func, shape[1:]) for _ in range(shape[0])]