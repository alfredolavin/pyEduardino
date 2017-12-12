import functools
import ctypes
import builtins
import operator


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


if __name__ == '__main__':
  pass
