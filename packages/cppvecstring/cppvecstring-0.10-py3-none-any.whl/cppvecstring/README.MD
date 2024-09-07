# C++ string vector for Python

### Tested against Windows 10 / Python 3.11 / Anaconda / C++ 20 - MSVC

### pip install cppvecstring

### Cython and a C++ compiler must be installed!

```PY
from cppvecstring import CppVectorStr
import numpy as np

with open(r"C:\androidcsvdata.csv",mode='rb') as f:
    mystrings=f.read().splitlines()[:1500]
c=CppVectorStr(mystrings)
print(len(c))
print(c)
del c[0]
print(c)
del c[[0,1,2,3]]
print(c)
print(c.nparray)
resultre1=c.re_finditer(b'samsung')
resultre2=c.re_findall(b'samsung.{1,20}')
resultre3=c.re_match(b'samsung')
resultre4=c.re_fullmatch(b'samsung')
resultre5=c.re_search(b'samsung')
resultre6=c.re_split(b'samsung')
result2=c.find(b'samsung')
result3=c.find_first_not_of(b"abcdefghijklmnopqrstuvwxyz ")
result4=c.find_first_of(b"abcdefghijklmnopqrstuvwxyz ")
result3=c.find_last_not_of(b"abcdefghijklmnopqrstuvwxyz ")
result4=c.find_last_of(b"abcdefghijklmnopqrstuvwxyz ")
c[0]=b'xxxxxxxxxxxxxx'
c[90:98]=b'xxxxxxxxxxxxxx'
print(c[0])
print(b'xxxxxxxxxxxxxx' in c)
c.insert(2,b'yyyyy')
print(b'yyyyy' in c)
print(c.index(b'yyyyy'))
print(c)
print(c[5:10])
resultre1=c.re_finditer(b'samsung',line_to_results=False)
resultre2=c.re_findall(b'samsung.{1,20}',line_to_results=False)
resultre3=c.re_match(b'samsung',line_to_results=False)
resultre4=c.re_fullmatch(b'samsung',line_to_results=False)
resultre5=c.re_search(b'samsung',line_to_results=False)
resultre6=c.re_split(b'samsung',line_to_results=False)
print(c.index_all(b'xxxxxxxxxxxxxx'))
gi=c.group_items()
print(c.pop(1))
spli=c.split_at_index([2, 4, 6, 10])
spli=c.split_at_value(b'xxxxxxxxxxxxxx')
c.extend([b'aaaaaaaaaaa',b'bbbbbbbbbbbbbb'])
c.extend_save([b'aaaaaaaaaaa','aaaaaaaaaaa','aaaaaaaaaaa',b'bbbbbbbbbbbbbb','xxxxxxxxx','hhhhhhh',444.333])
c.extend_save_with_conversion([b'aaaaaaaaaaa','aaaaaaaaaaa','aaaaaaaaaaa',b'bbbbbbbbbbbbbb','xxxxxxxxx','hhhhhhh',444.333])

print(c.count(b'aaaaaaaaaaa'))
print(c.reverse())
cc=(c.copy())
print(cc)
cc.clear()
print(cc)
print(cc.empty())
print(c.to_list())
print(c.to_tuple())
print(c.to_set())

my_results_apply_as_c_function = []
my_results_apply_as_c_pyfunction = []
my_results_apply_as_c_function_nogil = []


def apply_as_c_function(a):
    my_results_apply_as_c_function.append(a.startswith(b'xxx'))


def apply_as_c_pyfunction(a):
    my_results_apply_as_c_pyfunction.append(a.startswith(b'xxx'))


def apply_function(a):
    return a.startswith(b'xxx')


def apply_as_c_function_nogil(a):
    my_results_apply_as_c_function_nogil.append(a.startswith(b'xxx'))  # might not release the gil

results1 = c.apply_function(apply_function)
print(results1)
c.apply_as_c_function(apply_as_c_function)
print(my_results_apply_as_c_function)
c.apply_as_c_pyfunction(apply_as_c_pyfunction)
print(my_results_apply_as_c_pyfunction)
c.apply_as_c_function_nogil(apply_as_c_function_nogil)
print(my_results_apply_as_c_function_nogil)


```