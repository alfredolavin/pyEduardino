from alfredo import blackMagic
import operator

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

if __name__ == '__main__':
  pass