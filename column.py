from alfredo import blackMagic

def column(self, name):
  return [getattr(i, name) for i in self]

def addColumnPropertyToLists():
  blackMagic.proxy_builtin( list )['column'] = column

if __name__ == '__main__':
  pass
