# C++ vectors with Python indexing

### Tested against Windows 10 / Python 3.11 / Anaconda / C++ 20 - MSVC

### pip install cppvec

### Cython and a C++ compiler must be installed!

```PY
from cppvec import (
    CppVectorChar,
    CppVectorDouble,
    CppVectorFloat,
    CppVectorInt,
    CppVectorLong,
    CppVectorLongLong,
    CppVectorUnsignedInt,
    CppVectorUnsignedLong,
    CppVectorUnsignedLongLong,
    CppVectorUnsignedChar,
    CppVectorShort,
    CppVectorUnsignedShort,
    CppVectorByte,
    CppVectorUnsignedByte,
    CppVectorLongDouble,
    CppVectorSize_t,
)
import numpy as np
import ctypes

array_char = np.arange(100).astype(ctypes.c_byte)
array_int = np.arange(100).astype(ctypes.c_int)
array_long = np.arange(100).astype(ctypes.c_long)
array_long_long = np.arange(100).astype(ctypes.c_longlong)
array_float = np.arange(100).astype(ctypes.c_float)
array_double = np.arange(100).astype(ctypes.c_double)
array_uchar = np.arange(100).astype(ctypes.c_ubyte)
array_uint = np.arange(100).astype(ctypes.c_uint)
array_ulong = np.arange(100).astype(ctypes.c_ulong)
array_ulong_long = np.arange(100).astype(ctypes.c_ulonglong)
array_short = np.arange(100).astype(ctypes.c_short)
array_ushort = np.arange(100).astype(ctypes.c_ushort)
array_byte = np.arange(100).astype(ctypes.c_byte)
array_ubyte = np.arange(100).astype(ctypes.c_ubyte)
array_long_double = np.arange(100).astype(ctypes.c_longdouble)
array_size_t = np.arange(100).astype(ctypes.c_size_t)


vec_char = CppVectorChar(array_char)
vec_int = CppVectorInt(array_int)
vec_long = CppVectorLong(array_long)
vec_long_long = CppVectorLongLong(array_long_long)
vec_float = CppVectorFloat(array_float)
vec_double = CppVectorDouble(array_double)
vec_uchar = CppVectorUnsignedChar(array_uchar)
vec_uint = CppVectorUnsignedInt(array_uint)
vec_ulong = CppVectorUnsignedLong(array_ulong)
vec_ulong_long = CppVectorUnsignedLongLong(array_ulong_long)
vec_short = CppVectorShort(array_short)
vec_ushort = CppVectorUnsignedShort(array_ushort)
vec_byte = CppVectorByte(array_byte)
vec_ubyte = CppVectorUnsignedByte(array_ubyte)
vec_long_double = CppVectorLongDouble(array_long_double)
vec_size_t = CppVectorSize_t(array_size_t)

my_vectors = {
    "vec_char": vec_char,
    "vec_int": vec_int,
    "vec_long": vec_long,
    "vec_long_long": vec_long_long,
    "vec_float": vec_float,
    "vec_double": vec_double,
    "vec_uchar": vec_uchar,
    "vec_uint": vec_uint,
    "vec_ulong": vec_ulong,
    "vec_ulong_long": vec_ulong_long,
    "vec_short": vec_short,
    "vec_ushort": vec_ushort,
    "vec_byte": vec_byte,
    "vec_ubyte": vec_ubyte,
    "vec_long_double": vec_long_double,
    "vec_size_t": vec_size_t,
}

my_results_apply_as_c_function = []
my_results_apply_as_c_pyfunction = []
my_results_apply_as_c_function_nogil = []


def apply_as_c_function(a):
    my_results_apply_as_c_function.append(a + 5)


def apply_as_c_pyfunction(a):
    my_results_apply_as_c_pyfunction.append(a + 5)


def apply_function(a):
    return a + 5


def apply_as_c_function_nogil(a):
    my_results_apply_as_c_function_nogil.append(a + 5)  # might not release the gil


for k, c in my_vectors.items():
    print(f"before: {k=}")
    print(f"{c}")
    c.append(5)
    print(f"{c=}")
    print("-----------------------------------------")
    added = c + [1, 23, 3, 3]
    print(f"{added=}")
    print("-----------------------------------------")
    del c[5]
    print(c)
    print("-----------------------------------------")
    del c[:30]
    print(c)
    print("-----------------------------------------")
    del c[:10:2]
    print(c)
    print("-----------------------------------------")
    c[[1, 2, 11]] = 126
    print(c)
    print("-----------------------------------------")

    c[0] = 125
    print(c)
    print("-----------------------------------------")

    c[12:17:2] = 124
    print(c)
    print("-----------------------------------------")

    c.insert(4, 101)
    print(c)
    print("-----------------------------------------")
    c.insert([1, 3, 4, 6], 113)
    print(c)
    print("-----------------------------------------")
    print(c.index_all(113))
    print("-----------------------------------------")
    print(c.index(113))
    print("-----------------------------------------")
    print(113 in c)
    print("-----------------------------------------")
    print(103 in c)
    print("-----------------------------------------")
    c.remove(113)
    print(c)
    print("-----------------------------------------")
    popped = c.pop(3)
    print(popped)
    print(c)
    print("-----------------------------------------")
    c.remove_all(113)
    print(c)
    print("-----------------------------------------")
    print(c.group_items())
    print(c.split_at_index([2, 4, 6, 10]))
    print(c.split_at_index(3))
    print(c.split_at_value(124))
    c.extend([77, 1, 2, 3, 4, 5, 99])
    print(c)
    c.extend_save([7777, 1, 2, 3, 4, 5, 9999, 11.232, "stax", 9999])
    print(c)
    nparray = np.array([77, 1, 2, 3, 4, 5, 99], dtype=c.nparray.dtype)
    c.extend_np(nparray)
    print(c)
    c.reserve(1000)
    c.resize(300)
    print(c)
    print(c.count(0))
    c.remove_all(0)
    print(c)
    print(c.count(0))
    crev = c.reverse()
    print(crev)
    ccopy = c.copy()
    print(ccopy)
    ccopy.clear()
    print(ccopy)
    print(ccopy.empty())
    print(c.to_tuple())
    print(c.to_list())
    print(c.to_set())
    try:
        print(np.max(c.nparray))
        print(np.min(c.nparray))
        print(np.where(c.nparray > 10))
    except Exception:
        print(f"wrong datatype: {c.nparray.dtype}")
    c.sort()
    print(c)
    results1 = c.apply_function(apply_function)
    print(results1)
    c.apply_as_c_function(apply_as_c_function)
    print(my_results_apply_as_c_function)
    c.apply_as_c_pyfunction(apply_as_c_pyfunction)
    print(my_results_apply_as_c_pyfunction)
    c.apply_as_c_function_nogil(apply_as_c_function_nogil)
    print(my_results_apply_as_c_function_nogil)
    my_results_apply_as_c_pyfunction.clear()
    my_results_apply_as_c_function.clear()
    my_results_apply_as_c_function_nogil.clear()

```