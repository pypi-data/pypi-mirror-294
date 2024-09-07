from typing import *
from .dtypes.convert import handle_conversion
from .helpers.shapes import *
from .helpers.functional import *
from .helpers.ops import *
from copy import deepcopy
import math

int8 = "int8"
int16 = "int16"
int32 = "int32"
int64 = "int64"
long = "long"
float16 = "float16"
float32 = "float32"
float64 = "float64"
double = "double"

class array:
  int8 = int8
  int16 = int16
  int32 = int32
  int64 = int64 or long
  float16 = float16
  float32 = float32
  float64 = float64 or double

  def __init__(self, *data:Union[List["array"], list, int, float], dtype:Optional[Literal["int8", "int16", "int32", "int64", "float16", "float32", "float64"]]=None) -> None:
    self.data = data[0] if len(data) == 1 and isinstance(data[0], list) else list(data)
    self.shape = self.shape()
    self.dtype = array.int32 if dtype is None else dtype
    if dtype is not None:
      self.data = handle_conversion(self.data, dtype)

  def __repr__(self) -> str:
    return f"array([{self.data}])"

  def __str__(self) -> str:
    def format_element(element):
      if isinstance(element, list):
        return [format_element(sub_element) for sub_element in element]
      if self.dtype == int8 or self.dtype == int16 or self.dtype == int32 or self.dtype == int64 or self.dtype == long:
        return f"{element:.0f}."
      if self.dtype == float16:
        return f"{element:.2f}"
      if self.dtype == float32:
        return f"{element:.3f}"
      return f"{element:.4f}"

    formatted_data = format_element(self.data)

    def truncate_list(data, max_items=8):
      if len(data) > max_items:
        return data[:max_items // 2] + ['...'] + data[-max_items // 2:]
      return data

    def format_data(data, level=0):
      if isinstance(data[0], list):
        if len(data) > 8:
          data = truncate_list(data)  # Truncate rows if there are more than 8 arrays
        inner = ",\n".join(["  " * (level + 1) + format_data(sub_data, level + 1) for sub_data in data])
        return f"[\n{inner}\n" + "  " * level + "]"
      else:
        # Truncate individual row elements if they exceed 8
        data = truncate_list(data)
        return "[" + ", ".join(data) + "]"

    formatted_str = format_data(formatted_data, 0)
    formatted_str = formatted_str.replace("\t", " ")
    return f"array({formatted_str}, dtype={self.dtype})\n"

  def __getitem__(self, index:tuple):
    if isinstance(index, tuple):
      data = self.data
      for idx in index[:-1]:
        data = data[idx]
      return data[index[-1]]
    else:
      return self.data[index]
  
  def __setattr__(self, name: str, value: Any) -> None:
    super().__setattr__(name, value)
  
  def __setitem__(self, index: tuple, value: Any) -> None:
    if isinstance(index, tuple):
      data = self.data
      for idx in index[:-1]:
        data = data[idx]
      data[index[-1]] = value
    else:
      self.data[index] = value
  
  def __iter__(self) -> Iterator:
    for item in self.data:
      yield item
  
  def as_type(self, dtype:Literal["int8", "int16", "int32", "int64", "float16", "float32", "float64"]) -> List["array"]:
    out = handle_conversion(self.data, dtype)
    return array(out, dtype=dtype)
  
  def tolist(self) -> list:
    return self.data
  
  def copy(self) -> List["array"]:
    return array(deepcopy(self.data), dtype=self.dtype)
  
  def shape(self) -> list:
    return get_shape(self.data)
  
  def numel(self) -> int:
    out = 1
    for dim in self.shape:
      out *= dim
    return out
  
  def transpose(self) -> List["array"]:
    out = array(transpose(self.data), dtype=self.dtype)
    return out

  @property
  def F(self) -> List["array"]:
    return array(flatten(self.data), dtype=self.dtype)

  @property
  def T(self) -> List["array"]:
    return array(transpose(self.data), dtype=self.dtype)
  
  @property
  def size(self) -> tuple:
    return tuple(get_shape(self.data))
  
  @property
  def ndim(self) -> int:
    return len(get_shape(self.data))

  def flatten(self, start_dim:int=0, end_dim:int=-1) -> List["array"]:
    return array(flatten_recursive(self.data, start_dim, end_dim), dtype=self.dtype)

  def swap_axes(self, axis1:int, axis2:int) -> List["array"]:
    axis1 = self.ndim + axis1 if axis1 < 0 else axis1
    axis2 = self.ndim + axis2 if axis2 < 0 else axis2
    return array( swap_axes(self.data, axis1, axis2), dtype=self.dtype)

  def unsqueeze(self, dim:int=0):
    dim = dim if dim > 0 else self.ndim + dim
    return array(unsqueeze(self.data, dim), dtype=self.dtype)
  
  def squeeze(self, dim:int=0):
    if dim is not None and dim>=self.ndim:
      raise IndexError(f"Dimension out of range (expected to be in range of {self.ndim} dimensions)")
    dim = dim if dim > 0 else self.ndim + dim
    return array(squeeze(self.data, dim), dtype=self.dtype)
  
  def reshape(self, new_shape:tuple) -> List["array"]:
    out = reshape(self.data, new_shape)
    return array(out, dtype=self.dtype)

  def clip(self, min_value, max_value):
    def _clip(data, min_value, max_value):
      if isinstance(data, list):
        return [_clip(d, min_value, max_value) for d in data]
      return max(min(data, max_value), min_value)
    
    return array(_clip(self.data, min_value, max_value))
  
  # binary ops

  def __add__(self, other:List["array"]) -> List["array"]:
    other = other if isinstance(other, array) else array(other, dtype=self.dtype)
    def _add(a, b):
      if isinstance(a, list):
        return [_add(_a, _b) for _a, _b in zip(a, b)]
      else:
        return a + b

    target_shape, requires_broadcasting = broadcast_shape(self.shape, other.shape)
    
    if requires_broadcasting:
      self.data = handle_conversion(broadcast(self.data, target_shape), self.dtype)
      other.data = handle_conversion(broadcast(other.data, target_shape), other.dtype)
    
    if self.size == other.size:
      return array(_add(self.data, other.data), dtype=self.dtype)
    else:
      print(self.size, other.size)
      raise ValueError("shapes are incompatible for operation")

  def __mul__(self, other:List["array"]) -> List["array"]:
    other = other if isinstance(other, array) else array(other, dtype=self.dtype)
    def _mul(a, b):
      if isinstance(a, list):
        return [_mul(_a, _b) for _a, _b in zip(a, b)]
      else:
        return a * b
    
    target_shape, requires_broadcasting = broadcast_shape(self.shape, other.shape)

    if requires_broadcasting:
      self.data = handle_conversion(broadcast(self.data, target_shape), self.dtype)
      other.data = handle_conversion(broadcast(other.data, target_shape), other.dtype)

    if self.size == other.size:
      return array(_mul(self.data, other.data), dtype=self.dtype)
    else:
      raise ValueError("shapes are incompatible for operation")
  
  def __matmul__(self, other:List["array"]) -> List["array"]:
    out = matmul(self.data, other.data)
    return array(out, dtype=self.dtype)

  def __sub__(self, other:List["array"]) -> List["array"]:
    other = other if isinstance(other, array) else array(other, dtype=self.dtype)
    def _sub(a, b):
      if isinstance(a, list):
        return [_sub(_a, _b) for _a, _b in zip(a, b)]
      else:
        return a + b

    target_shape, requires_broadcasting = broadcast_shape(self.shape, other.shape)
    
    if requires_broadcasting:
      self.data = handle_conversion(broadcast(self.data, target_shape), self.dtype)
      other.data = handle_conversion(broadcast(other.data, target_shape), other.dtype)
    
    if self.size == other.size:
      return array(_sub(self.data, other.data), dtype=self.dtype)
    else:
      raise ValueError("shapes are incompatible for operation")

  def __rsub__(self, other:List["array"]) -> List["array"]:
    other = other if isinstance(other, array) else array(other, dtype=self.dtype)
    def _sub(a, b):
      if isinstance(a, list):
        return [_sub(_a, _b) for _a, _b in zip(a, b)]
      else:
        return a + b

    target_shape, requires_broadcasting = broadcast_shape(self.shape, other.shape)
    
    if requires_broadcasting:
      self.data = handle_conversion(broadcast(self.data, target_shape), self.dtype)
      other.data = handle_conversion(broadcast(other.data, target_shape), other.dtype)
    
    if self.size == other.size:
      return array(_sub(other.data, self.data), dtype=self.dtype)
    else:
      raise ValueError("shapes are incompatible for operation")
  
  def __rmul__(self, other:List["array"]) -> List["array"]:
    return other * self
  
  def __truediv__(self, other:List["array"]) -> List["array"]:
    return self * other ** -1
  
  def rtruediv(self, other:List["array"]) -> List["array"]:
    return other * self ** -1

  def __neg__(self) -> List["array"]:
    def _neg(a):
      if isinstance(a, list):
        return [_neg(_a) for _a in a]
      return -a
    return array(_neg(self.data), dtype=self.dtype)

  def __pow__(self, pow:Union[int, float], eps:float=1e6) -> List["array"]:
    assert isinstance(pow, (int, float)), "power exponent is of incompatible datatype"

    def _pow(data, pow):
      if isinstance(data, list):
        return [_pow(d, pow) for d in data]
      if data == 0:
        data = eps
      return math.pow(data, pow)

    return array(_pow(self.data, pow), dtype=array.float32)
  
  def exp(self) -> List["array"]:
    def _exp(data):
      if isinstance(data, list):
        return [_exp(d) for d in data]
      return math.exp(data)

    return array(_exp(self.data), dtype=array.float32)

  def relu(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return relu(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def relu_derivative(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return relu_derivative(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def tanh(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return tanh(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def tanh_derivative(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return tanh_derivative(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def sigmoid(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return sigmoid(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def sigmoid_derivative(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return sigmoid_derivative(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def gelu(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return gelu(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def gelu_derivative(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return gelu_derivative(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def silu(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return silu(data)
    return array(_apply(self.data), dtype=array.float32)
  
  def silu_derivative(self) -> List["array"]:
    def _apply(data):
      if isinstance(data, list):
        return [_apply(sub_data) for sub_data in data]
      else:
        return silu_derivative(data)
    return array(_apply(self.data), dtype=array.float32)

  def broadcast(self, other:List["array"]) -> List["array"]:
    other = other if isinstance(other, array) else array(other)
    new_shape, needs_broadcasting = broadcast_shape(self.shape, other.shape)
    if needs_broadcasting:
      return array(broadcast(other.data, new_shape), dtype=self.dtype)
    else:
      return None
  
  def dot(self, other:List["array"]) -> List["array"]:
    out = dot_product(self.data, other.data)
    return array(out, dtype=self.dtype)
  
  def det(self) -> List["array"]:
    out = determinant(self.data)
    return array(out, dtype=self.dtype)

  def mean(self, axis:Optional[int]=None, keepdims:bool=False) -> List["array"]:
    if axis is None:
      flat_array = flatten(self.data)
      mean_val = sum(flat_array) / len(flat_array)
      if keepdims:
        out = [[mean_val]]
      return mean_val
    if axis == 0:
      out = mean_axis0(self.data)
    else:
      out = mean_axis(self.data, axis, keepdims)
    return array(out, dtype=self.dtype)

  def var(self, axis:Optional[int]=None, ddof:int=0, keepdims:bool=False) -> List["array"]:
    if axis is None:
      flat_array = flatten(self.data)
      mean_value = sum(flat_array) / len(flat_array)
      variance = sum((x - mean_value) ** 2 for x in flat_array) / (len(flat_array) - ddof)
      if keepdims:
        out = [[variance]]
      return variance
    if axis == 0:
      out = var_axis0(self.data)
    else:
      mean_values = self.mean(axis=axis)
      out = var_axis(self.data, mean_values, axis, ddof, keepdims)
    return array(out, dtype=self.dtype)

  def std(self, axis:Optional[int]=None, ddof:int=0, keepdims:bool=False) -> List["array"]:
    variance = self.var(axis=axis, ddof=ddof, keepdims=keepdims).data
    def _std(var):
      if isinstance(var, list):
        return [_std(sub) for sub in var]
      return math.sqrt(var)
    if keepdims:
      out = [[math.sqrt(x)] for x in flatten(variance)]
    else:
      out = _std(variance)
    return array(out, dtype=self.dtype)
  
  def sum(self, axis:Optional[int]=None, keepdims:bool=False) -> List["array"]:
    if axis == None:
      if keepdims:
        out = [[sum(flatten(self.data))]]
      else:
        out = sum(flatten(self.data))
    elif axis == 0:
      out = sum_axis0(self.data)
    else:
      out = sum_axis(self.data, axis, keepdims)
    return array(out, dtype=self.dtype)
  
  def log(self) -> List["array"]:
    def _log_element(element):
      if isinstance(element, list):
        return [_log_element(sub_element) for sub_element in element]
      else:
        if element <= 0:
          raise ValueError(f"Logarithm undefined for non-positive values: {element}")
        return math.log(element)

    return array(_log_element(self.data), dtype=self.dtype)