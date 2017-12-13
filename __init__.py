from alfredo import blackMagic, forEach
from collections import OrderedDict

class dotDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

class OrderedDotDict(OrderedDict):
  __getattr__ = OrderedDict.__getitem__
  __setattr__ = OrderedDict.__setitem__
  __delattr__ = OrderedDict.__delitem__

def column(self, name):
  return [getattr(i, name) for i in self]

def addforEachMethodToLists(propertyName='forEach'):
  blackMagic.proxy_builtin(list)[propertyName] = property(forEach.forEach)

def addforEachMethodToTuples(propertyName='forEach'):
  blackMagic.proxy_builtin(tuple)[propertyName] = property(forEach.forEach)

def addColumnPropertyToLists():
  blackMagic.proxy_builtin( list )['column'] = column

if __name__ == '__main__':
  
  def cmd(*args):
    return ';'.join(args.forEach.str())
  
  addforEachMethodToTuples()
  print(cmd(2,3,4,5))
  
  pass

