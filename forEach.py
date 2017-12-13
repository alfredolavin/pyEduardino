import operator
import builtins

class forEach(list):
  def __init__(self, args, **kwargs):
    super().__init__(args)
    self.fname = kwargs.get('fname')
    
  def __getattr__(self, key):
    return forEach(self, fname = key)
  
  def column(self):
    return forEach((getattr(i, name) for i in self))
  
  def __call__(self, *args, **kwargs):
    if not self.fname:
      raise TypeError()
    func = getattr(operator, self.fname, None) or\
           getattr(builtins, self.fname, None)
    if func:
      return forEach(( func(*((item,) + args), **kwargs) for item in self ))
    else:
      return forEach(getattr(item, self.fname)(*args, **kwargs) for item in self)
    
if __name__ == '__main__':
  pass
