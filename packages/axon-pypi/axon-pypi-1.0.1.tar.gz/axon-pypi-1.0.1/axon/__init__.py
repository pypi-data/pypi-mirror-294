from .base import array, int8, int16, int32, int64, float16, float32, float64, double, long
from ._ops import *
from ._utils import *
from ._random import Random

random = Random(seed=200)