from collections import OrderedDict
from typing import Iterable
from itertools import chain
import operator
import builtins
import ctypes
import re

global _last,_first
_last,_first = 0, -1

class PyObject(ctypes.Structure):
  pass

Py_ssize_t = hasattr(ctypes.pythonapi, 'Py_InitModule4_64') and ctypes.c_int64 or ctypes.c_int

PyObject._fields_ = [('ob_refcnt', Py_ssize_t), ('ob_type', ctypes.POINTER(PyObject)), ]

class SlotsPointer(PyObject):
  _fields_ = [('dict', ctypes.POINTER(PyObject))]

def proxy_builtin(klass):
  name = klass.__name__
  slots = getattr(klass, '__dict__', name)

  pointer = SlotsPointer.from_address(id(slots))
  namespace = {}

  ctypes.pythonapi.PyDict_SetItem(
    ctypes.py_object(namespace),
    ctypes.py_object(name),
    pointer.dict,)

  return namespace[name]

class forEach(list):
  def __init__(self, args, **kwargs):
    super().__init__(args)
    self.fname = kwargs.get('fname')

  def __getattr__(self, key):
    return forEach(self, fname = key)

  def __call__(self, *args, **kwargs):
    if not self.fname:
      raise TypeError()
    func = getattr(operator, self.fname, None) or\
           getattr(builtins, self.fname, None)
    if func:
      return forEach(( func(*((item,) + args), **kwargs) for item in self ))
    else:
      return forEach(getattr(item, self.fname)(*args, **kwargs) for item in self)

class _re(str):
  def __init__(self, _fname = None):
    super().__init__()
    self.fname = _fname

  def __getattr__(self, key):
    return _re(self, key)

  def __call__(self, *args, **kwargs):
    if not self.fname:
      raise TypeError()
    func = getattr(re, self.fname, None)

    if func:
      return _re(func(args[0], self, *args[1:], **kwargs))
    else:
      return _re(getattr(self, self.fname)(*args, **kwargs))

class dotDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

class OrderedDotDict(OrderedDict):
  __getattr__ = OrderedDict.__getitem__
  __setattr__ = OrderedDict.__setitem__
  __delattr__ = OrderedDict.__delitem__

def Nones(n=10):
  return [None]*n

def column(self, *names):
  if isinstance(names, str):
    names = [str(names),]
  if len(names) == 1:
    names= names[0]
    return [getattr(i, names) for i in self]
  else:
    return [[getattr(i, name) for name in names] for i in self]

def evens(self):
  return self[1::2]

def odds(self):
  return self[::2]

def last(self):
  return self[-1]

def first(self):
  return self[0]

def _reversed(self):
  return reversed(self)

def _len(self):
  return len(self)

def exclude(self, *what):
  for item in what:
    try:
      self.remove(item)
    except ValueError:
      pass
  return self

def where(self, what):
  if callable(what):
    return filter(what, self)
  elif isinstance(what, str):
    filter_code = '[item for item in self if item %s]'%what
    return eval(filter_code)
  else:
    raise TypeError()

def eduardinze():
  proxy_builtin( range )['forEach'] = property(forEach)
  proxy_builtin( str )['re'] = property(_re)
  # Extend lists
  proxy_builtin( list )['forEach'] = property(forEach)
  proxy_builtin( list )['len'] = property(_len)
  proxy_builtin( list )['exclude'] = exclude
  proxy_builtin( list )['column'] = column
  proxy_builtin( list )['evens'] = property(evens)
  proxy_builtin( list )['where'] = property(where)
  proxy_builtin( list )['odds'] = property(odds)
  proxy_builtin( list )['last'] = property(last)
  proxy_builtin( list )['first'] = property(first)
  proxy_builtin( list )['reversed'] = property(_reversed)
  # Extend ranges too
  proxy_builtin( range )['forEach'] = property(forEach)
  proxy_builtin( range )['len'] = property(_len)
  proxy_builtin( range )['exclude'] = exclude
  proxy_builtin( range )['column'] = column
  proxy_builtin( range )['evens'] = evens
  proxy_builtin( range )['where'] = where
  proxy_builtin( range )['odds'] = odds
  proxy_builtin( range )['last'] = last
  proxy_builtin( range )['first'] = first
  proxy_builtin( range )['reversed'] = _reversed

  # Extend ranges too
  proxy_builtin( range )['forEach'] = property(forEach)
  proxy_builtin( range )['len'] = property(_len)
  proxy_builtin( range )['exclude'] = exclude
  proxy_builtin( range )['column'] = column
  proxy_builtin( range )['evens'] = evens
  proxy_builtin( range )['where'] = where
  proxy_builtin( range )['odds'] = odds
  proxy_builtin( range )['last'] = last
  proxy_builtin( range )['first'] = first
  proxy_builtin( range )['reversed'] = _reversed

eduardinze()

def main():
  # Run some test and examples
  sample = list(range(0,10,3)) + ['a','b']
  print((list(range(0,10,3)) + ['a','b']).odds().str().upper())

  test = list(range(10)) + ['a','b']
  print(test.forEach.str().upper())
  print(range(66,88).forEach.chr().lower())
  pass

if __name__ == '__main__':
    main()

