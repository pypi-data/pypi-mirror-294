# C++ unordered map for Python

### Tested against Windows 10 / Python 3.11 / Anaconda / C++ 20 - MSVC

### pip install cppumap

### Cython and a C++ compiler must be installed!

```PY
from cppumap.um_int__int import Um_int_int
import numpy as np

di = {k: k + 1 for k in range(100)}
di2 = {k: k - 100 for k in range(100, 200)}
stufftodeletelater = list(di2.items())
di.update(di2)
m = Um_int_int(di)
print(m)
stufftodelete = list(range(20))
del m[stufftodelete]
print(m)
values2delete = list(range(90, 100))
m.del_by_values(values2delete)
print(m)
m.del_by_values(79)
print(m)
m.del_by_key_and_value(stufftodeletelater)
print(m)
a = np.arange(100, dtype=np.int32)
b = np.arange(100, dtype=np.int32)
m.set_np(a, b)
print(m)
tuplelist = [(k, k + 1) for k in range(300, 400)]
m.set_tuple_list(tuplelist)
print(m)
print(m.getitems(a))
print(m.sorted())
for k, v in m.items():
    print(k, v)
for k in m:
    print(k)
print(m.keys())
print(m.values())
di3 = {k: k - 100 for k in range(1000, 1200)}
m.update(di3)
print(m)
cop = m.copy()
print(cop)
m.append(100000 - 1, 1)
print(m)

my_results_apply_as_c_function = []
my_results_apply_as_c_pyfunction = []
my_results_apply_as_c_function_nogil = []



def apply_as_c_function(a):
    my_results_apply_as_c_function.append(a)


def apply_as_c_pyfunction(a):
    my_results_apply_as_c_pyfunction.append(a)


def apply_function(a, b):
    return b, a


def apply_as_c_function_nogil(a):
    my_results_apply_as_c_function_nogil.append(a)  # might not release the gil


results1 = m.apply_function(apply_function)
print(results1)
m.apply_as_c_function(apply_as_c_function)
n2 = (
    np.array([q for q in my_results_apply_as_c_function if q is not None], dtype=np.uint64)
    .view(np.int32)
    .reshape((-1, 2))
)
m.apply_as_c_pyfunction(apply_as_c_pyfunction)

n1 = (
    np.array(
        [q for q in my_results_apply_as_c_pyfunction if q is not None], dtype=np.uint64
    )
    .view(np.int32)
    .reshape((-1, 2))
)

m.apply_as_c_function_nogil(apply_as_c_function_nogil)
n3 = (
    np.array(
        [q for q in my_results_apply_as_c_function_nogil if q is not None],
        dtype=np.uint64,
    )
    .view(np.int32)
    .reshape((-1, 2))
)
m.pop(9999)


```