from typing import *
import random

def _zeros(shape:tuple) -> list:
  if len(shape) == 1:
    return [0] * shape[0]
  return [_zeros(shape[1:]) for _ in range(shape[0])]

def _ones(shape:tuple) -> list:
  if len(shape) == 1:
    return [1] * shape[0]
  return [_ones(shape[1:]) for _ in range(shape[0])]

def _randint(low:int, high:int, size:int=None) -> list:
  if size is None:
    return random.randint(low, high)
  else:
    return [random.randint(low, high) for _ in range(size)]

def _arange(start:int=0, end:int=10, step:int=1) -> list:
  return [start + i * step for i in range(int((end-start)/step))]

def _randn(domain:tuple=(1, -1), shape:tuple=None) -> list:
  if len(shape) == 1:
    return [random.uniform(domain[0], domain[1]) for _ in range(shape[0])]
  else:
    return [_randn(domain=domain, shape=shape[1:]) for _ in range(shape[0])]

def _zeros_like(arr:list) -> list:
  if isinstance(arr, list):
    return [_zeros_like(elem) for elem in arr]
  elif isinstance(arr, tuple):
    return tuple(_zeros_like(elem) for elem in arr)
  else:
    return [0]

def _ones_like(arr:list) -> list:
  if isinstance(arr, list):
    return [_ones_like(elem) for elem in arr]
  elif isinstance(arr, tuple):
    return tuple(_ones_like(elem) for elem in arr)
  else:
    return [1]