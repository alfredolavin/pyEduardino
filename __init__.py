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

class dotSet(set):
  __getattr__ = OrderedDict.__getitem__
  __setattr__ = OrderedDict.__setitem__
  __delattr__ = OrderedDict.__delitem__

def Nones(self, n= 10):
  return forEach([None,]*(n or self.len))

def column(self, *names):
  if isinstance(names, str):
    names = [str(names),]
  if len(names) == 1:
    names= names[0]
    return forEach([getattr(i, names) for i in self])
  else:
    return forEach([[getattr(i, name) for name in names] for i in self])

def row(self, *names):
  if isinstance(names, str):
    names = [str(names),]
  if len(names) == 1:
    names= names[0]
    return forEach([getattr(i, names) for i in self])
  else:
    return forEach([[getattr(i, name) for name in names] for i in self])

def positionEvens(self):
  return forEach(self)[1::2]

def positionOdds(self):
  return forEach(self)[::2]

def evens(self):
  return forEach(filter(lambda x: x%2!=0,self))

def odds(self):
  return forEach(filter(lambda x: x%2==0,self))

def numbers(self):
  return forEach((self)[1::2])

def last(self):
  return forEach((self)[-1])

def middle(self):
  return forEach(self[self.len//2])

def first(self):
  return forEach(self[0])

def _reversed(self):
  return forEach(reversed(self))

def _len(self):
  return len(list(self))

def exclude(self, *what):
  tmp= forEach(self)
  for item in what:
    try:
      tmp.remove(item)
    except ValueError:
      pass
  return tmp

def _map(self, func):
  tmp= forEach(self)
  for i in range(tmp):
    tmp[i]= eval(func)
  return tmp

def enumerateme(self):
  return forEach(enumerate(self))

def where(self, what):
  if callable(what):
    return forEach(filter(what, self))
  elif isinstance(what, str):
    filter_code = '[item for item in self if item %s]'%what
    return forEach(eval(filter_code))
  else:
    raise TypeError()

def eduardinze():
  for _class in [list, tuple, range,]:
    proxy_builtin( _class )['Nones']= property(Nones)
    proxy_builtin( _class )['column']= property(column)
    proxy_builtin( _class )['row']= property(row)
    proxy_builtin( _class )['positionEvens']= property(positionEvens)
    proxy_builtin( _class )['positionOdds']= property(positionOdds)
    proxy_builtin( _class )['evens']= property(evens)
    proxy_builtin( _class )['odds']= property(odds)
    proxy_builtin( _class )['numbers']= property(numbers)
    proxy_builtin( _class )['last']= property(last)
    proxy_builtin( _class )['middle']= property(middle)
    proxy_builtin( _class )['first']= property(first)
    proxy_builtin( _class )['reversed']= property(_reversed)
    proxy_builtin( _class )['len']= property(_len)
    proxy_builtin( _class )['exclude']= property(exclude)
    proxy_builtin( _class )['map']= property(_map)
    proxy_builtin( _class )['enumerateme']= property(enumerateme)
    proxy_builtin( _class )['where']= property(where)
    proxy_builtin( _class )['forEach']= property(forEach)
    proxy_builtin( _class )['']= property()


eduardinze()

def main():
  # Run some test and examples
  sample = list(range(0,10,3))

  test = list(range(10)) + ['a','b']
  print(test.forEach.str().upper())
  print(range(66,88).forEach.chr().lower())
  pass

if __name__ == '__main__':
    main()

