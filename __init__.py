import operator
from alfredo import blackMagic
from collections import OrderedDict

class dotDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

class OrderedDotDict(OrderedDict):
  __getattr__ = OrderedDict.__getitem__
  __setattr__ = OrderedDict.__setitem__
  __delattr__ = OrderedDict.__delitem__

class forEach(list):
  def __init__(self, args, **kwargs):
    super().__init__(args)
    self.function = kwargs.get('function')
    
  def __getattr__(self, key):
    return forEach(self, function = key)
  
  def column(self):
    return forEach((getattr(i, name) for i in self))
  
  def __call__(self, *args, **kwargs):
    if getattr(operator, self.function, None):
      func = getattr(operator, self.function)
      return forEach(( func(*((item,) + args), **kwargs) for item in self ))
    else:
      return forEach(getattr(item, self.function)(*args, **kwargs) for item in self)

def addforEachMethodToLists(propertyName='forEach'):
  blackMagic.proxy_builtin(list)[propertyName] = property(forEach)

def addforEachMethodToTuples(propertyName='forEach'):
  blackMagic.proxy_builtin(tuple)[propertyName] = property(forEach)

def column(self, name):
  return [getattr(i, name) for i in self]

def addColumnPropertyToLists():
  blackMagic.proxy_builtin( list )['column'] = column

if __name__ == '__main__':
  pass
