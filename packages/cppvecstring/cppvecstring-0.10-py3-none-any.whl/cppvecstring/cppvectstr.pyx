import cython
cimport cython
import numpy as np
cimport numpy as np
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from libcpp.unordered_set cimport unordered_set
from libcpp.string cimport string, npos
from libcpp.utility cimport pair
from libc.stdio cimport printf
from libcpp.algorithm cimport for_each
from cython.operator cimport dereference as deref, preincrement as inc
import ctypes
import regex as re
re.cache_all()
_func_cache=[]
ctypedef vector[string] stringvector
ctypedef pair[size_t,size_t] line_match_find

ctypedef void (*pure_c_function)(string val)
ctypedef void (*pure_c_pyfunction)(string val)
ctypedef void (*pure_c_function_nogil)(string val) noexcept nogil


cpdef size_t convert_to_c_function(object fu):
    CMPFUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef size_t convert_to_c_pyfunction(object fu):
    CMPFUNC = ctypes.PYFUNCTYPE(None, ctypes.c_char_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cdef _get_index_np(i):
    cdef:
        np.ndarray[int, ndim=1, mode="c", cast=False] dellist
    if isinstance(i,slice):
        dellist=np.arange(i.start or 0, i.stop, i.step or 1,dtype=int)
    else:
        if isinstance(i, int):
            i=[i]
        dellist=np.sort(np.array(i,dtype=int))
    return dellist


class NpDescriptor:
    def __init__(self):
        self.npdataype="S"

    def __get__(self, instance, owner):
        return np.array(instance.to_list(),dtype=self.npdataype)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = np.ndarray([],int)

cdef class CppVectorStr:
    cdef stringvector v
    nparray = NpDescriptor()

    def __init__(self,*args,**kwargs):
        cdef:
            Py_ssize_t indi
            Py_ssize_t len_args = 0
        if len(args)>0:
            len_args=len(args[0])
        for indi in range(len_args):
            self.v.push_back(<string>args[0][indi])

    def __len__(self):
        return (<size_t>self.v.size())

    def __delitem__(self, i):
        cdef:
            int[:] dellistview
            int indi
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
        dellistview=_get_index_np(i)
        with nogil:
            for indi in range(dellistview.shape[0]):
                if dellistview[indi]-indi >= self.v.size():
                    continue
                if begin + (dellistview[indi]-indi) < end:
                    self.v.erase(begin + (dellistview[indi]-indi))

    def print_array(self):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
        with nogil:
            while (begin!=end):
                printf("%d\t%s\n",linecounter,deref(begin).c_str())
                inc(begin)
                linecounter+=1


    def __str__(self):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
        with nogil:
            while (begin!=end):
                printf("%s\n",deref(begin).c_str())
                inc(begin)
                linecounter+=1
                if linecounter>50:
                    break
        return ""
    def __repr__(self) -> str:
        return self.__str__()

    def __setitem__(self, i, bytes v):
        cdef:
            int[:] setlistview
            int indi
            size_t vecsize=self.v.size()
            string vstring=v
        setlistview=_get_index_np(i)
        with nogil:
            for indi in range(setlistview.shape[0]):
                if setlistview[indi] < vecsize:
                    self.v[setlistview[indi]]= vstring
                else:
                    break

    def __getitem__(self,i):
        cdef:
            int[:] getlistview
            vector[string] results
            size_t vecsize = self.v.size()
            Py_ssize_t indi
        getlistview=_get_index_np(i)
        results.reserve(getlistview.shape[0])
        with nogil:
            for indi in range(getlistview.shape[0]):
                if getlistview[indi]>vecsize:
                    break
                results.push_back(self.v[getlistview[indi]])
        return self.__class__(results)

    cpdef int index(self, bytes i):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            int counter = -1
            string mystring = i
        with nogil:
            while (begin!=end):
                if deref(begin) == mystring:
                    return counter+1
                counter+=1
                inc(begin)

    cpdef vector[int] index_all(self, bytes i):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            vector[int] results
            int indexcounter=0
            string mystring = i
        with nogil:
            while (begin!=end):
                if deref(begin) == mystring:
                    results.push_back(indexcounter)
                indexcounter+=1
                inc(begin)
        return results

    def __contains__(self,bytes i):
        return self.index(i) > -1


    cpdef insert(self, i, bytes v):
        cdef:
            int[:] setlistview
            int indi
            int indicounter= 0
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            string vstring= v
        setlistview=_get_index_np(i)
        with nogil:
            for indi in range(setlistview.shape[0]):
                if begin+(setlistview[indi]+indicounter)<end:
                    self.v.insert(begin+(setlistview[indi]+indicounter), vstring)
                    end = self.v.end()
                    indicounter+=1

    cpdef to_list(self):
        return self.v

    cpdef pop(self, Py_ssize_t i):
        if self.v.size()<=i:
            raise IndexError()
        x = self.v[i]
        self.__delitem__(i)
        return x

    cpdef group_items(self):
        cdef:
            unordered_map[string,vector[int]] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            int counter=0
        with nogil:
            while (begin!=end):
                results[deref(begin)].push_back(counter)
                counter+=1
                inc(begin)
        return results

    cpdef split_at_index(self, i):
        cdef:
            int[:] splitlistview
            int indi
            int indi2
            int mylen = self.v.size()
            vector[vector[string]] result_vector = [[]]
        if isinstance(i, int):
            i=[i]
        i=[x for x in i if x<mylen]
        i.insert(0,0)
        i.append(mylen)
        splitlistview=_get_index_np(i)
        result_vector.resize(splitlistview.shape[0]-1)
        with nogil:
            for indi in range(splitlistview.shape[0]-1):
                result_vector[indi].reserve(splitlistview[indi+1]-splitlistview[indi])
                for indi2 in range(splitlistview[indi], splitlistview[indi+1]):
                    result_vector[indi].push_back(self.v[indi2])
        return result_vector
    cpdef split_at_value(self,bytes i):
        cdef:
            vector[int] results=self.index_all(i)
        return self.split_at_index(results)

    cpdef void extend(self, n):
        cdef:
            Py_ssize_t i
            Py_ssize_t len_iters = len(n)
        for i in range(len_iters):
            self.v.push_back(n[i])

    cpdef extend_save(self,n):
        cdef:
            Py_ssize_t i
            Py_ssize_t len_iters = len(n)
        for i in range(len_iters):
            try:
                self.v.push_back(n[i])
            except Exception:
                pass
    cpdef extend_save_with_conversion(self,n):
        cdef:
            Py_ssize_t i
            Py_ssize_t len_iters = len(n)
        for i in range(len_iters):
            try:
                self.v.push_back(n[i])
            except Exception:
                self.v.push_back(str(n[i]))
    cpdef void reserve(self, int n):
        self.v.reserve(n)

    cpdef void resize(self, int n):
        self.v.resize(n)

    cpdef void shrink_to_fit(self):
        self.v.shrink_to_fit()

    cpdef int count(self, bytes i):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            int counter = 0
            string mystring = i
        with nogil:
            while (begin!=end):
                if deref(begin) == mystring:
                    counter+=1
                inc(begin)
        return counter

    cpdef reverse(self):
        cdef:
            vector[string].reverse_iterator begin = self.v.rbegin()
            vector[string].reverse_iterator end = self.v.rend()
            vector[string] results
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                results.push_back(deref(begin))
                inc(begin)
        return self.__class__(results)

    cpdef copy(self):
        newclass=self.__class__()
        newclass.extend(self.nparray)
        return newclass
    cpdef void clear(self):
        self.v.clear()

    cpdef bint empty(self):
        return self.v.empty()

    cpdef tuple to_tuple(self):
        return tuple(self.nparray)
    cpdef to_set(self):
        cdef:
            unordered_set[string]  results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
        while (begin!=end):
            results.insert(deref(begin))
            inc(begin)
        return results        
    cpdef size_t _get_vector_address(self):
        return (<size_t>self.v.data())

    cpdef size_t _get_vector_size(self):
        return (<size_t>self.v.size())

    cpdef compare(self,bytes stri):
        cdef:
            vector[Py_ssize_t] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            Py_ssize_t linecounter=0
            string searchstring = stri
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                if (deref(begin).compare(searchstring) != 0):
                    results.push_back(linecounter)

                inc(begin)
                linecounter+=1
        return results

    cpdef find_first_not_of(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).find_first_not_of(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results
    cpdef find_first_of(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).find_first_of(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results
    cpdef find_last_not_of(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).find_last_not_of(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results
    cpdef find_last_of(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).find_last_of(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results
    cpdef find(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).find(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results

    cpdef rfind(self,bytes stri):
        cdef:
            vector[line_match_find] results
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t linecounter=0
            string searchstring = stri
            size_t checkstring
        results.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                checkstring=(deref(begin).rfind(searchstring))
                if checkstring !=npos:
                    results.push_back(line_match_find(linecounter,checkstring))
                inc(begin)
                linecounter+=1
        return results

    cpdef _refu(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
  bint partial=False, bint concurrent=True, object timeout=None, bint ignore_unused=True, str refunc='finditer', object kwargs=None,bint line_to_results=True):
        cdef:
            dict results = {}
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            Py_ssize_t linecounter=0
            list regresults
            object pat=re.compile(pattern=pattern, flags=flags, ignore_unused=ignore_unused,cache_pattern=None,**kwargs)
            object refunc_function = getattr(pat,refunc)
            int cat

        if refunc in ['finditer']:
            cat=0
        elif refunc in ['search','fullmatch','match']:
            cat=1
        else:
            cat=2
        while (begin!=end):
            if cat==0:
                regresults=[k for k in refunc_function(
                    string=deref(begin), pos=pos, endpos=endpos, overlapped=overlapped, concurrent=concurrent, partial=partial,
        timeout=timeout)]
            elif cat==1:
                regresultstmp=refunc_function(
                    string=deref(begin), pos=pos, endpos=endpos, concurrent=concurrent, partial=partial,
        timeout=timeout)
                if regresultstmp:
                    regresults=[regresultstmp]
                else:
                    regresults=[]
            else:
                regresults=refunc_function(
                    string=deref(begin), pos=pos, endpos=endpos, overlapped=overlapped, concurrent=concurrent,
        timeout=timeout)
            if regresults:
                if line_to_results:
                    results[linecounter]=[deref(begin),regresults]
                else:
                    results[linecounter]=regresults
            linecounter+=1
            inc(begin)
        return results

    cpdef re_finditer(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
  bint partial=False, bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None, bint line_to_results=True):
        if not kwargs:
            kwargs={}
        return self._refu(pattern=pattern, flags=flags, pos=pos, endpos=endpos, overlapped=overlapped,
  partial=partial,  concurrent=concurrent, timeout=timeout, ignore_unused=ignore_unused, refunc='finditer',kwargs=kwargs, line_to_results=line_to_results)


    cpdef re_findall(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
 bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None,bint line_to_results=True):
        if not kwargs:
            kwargs={}
        return self._refu(pattern=pattern, flags=flags, pos=pos, endpos=endpos, overlapped=overlapped,
  partial=False,  concurrent=concurrent, timeout=timeout, ignore_unused=ignore_unused, refunc='findall',kwargs=kwargs,line_to_results=line_to_results)


    cpdef re_match(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
  bint partial=False, bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None,bint line_to_results=True):
        if not kwargs:
            kwargs={}
        return self._refu(pattern=pattern, flags=flags, pos=pos, endpos=endpos, overlapped=overlapped,
  partial=partial,  concurrent=concurrent, timeout=timeout, ignore_unused=ignore_unused, refunc='match',kwargs=kwargs,line_to_results=line_to_results)

    cpdef re_fullmatch(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
  bint partial=False, bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None,bint line_to_results=True):
        if not kwargs:
            kwargs={}
        return self._refu(pattern=pattern, flags=flags, pos=pos, endpos=endpos, overlapped=overlapped,
  partial=partial,  concurrent=concurrent, timeout=timeout, ignore_unused=ignore_unused, refunc='fullmatch',kwargs=kwargs,line_to_results=line_to_results)

    cpdef re_search(self,bytes pattern, int flags=0, object pos=None, object endpos=None, bint overlapped=False,
  bint partial=False, bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None,bint line_to_results=True):
        if not kwargs:
            kwargs={}
        return self._refu(pattern=pattern, flags=flags, pos=pos, endpos=endpos, overlapped=overlapped,
  partial=partial,  concurrent=concurrent, timeout=timeout, ignore_unused=ignore_unused, refunc='search',kwargs=kwargs,line_to_results=line_to_results)

    cpdef re_split(self,bytes pattern, int maxsplit=0, int flags=0, bint concurrent=True, object timeout=None, bint ignore_unused=True, object kwargs=None,bint line_to_results=True):
        cdef:
            dict results = {}
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            Py_ssize_t linecounter=0
            list regresults
            dict kwargsn=kwargs or {}
            object pat=re.compile(pattern=pattern, flags=flags, ignore_unused=ignore_unused,cache_pattern=None,**kwargsn)
            object refunc_function = getattr(pat,'split')
        while (begin!=end):
            if line_to_results:
                results[linecounter]=[deref(begin),refunc_function(
                        string=deref(begin), maxsplit=maxsplit, concurrent=concurrent, timeout=timeout)]
            else:
                results[linecounter]=refunc_function(
                        string=deref(begin), maxsplit=maxsplit, concurrent=concurrent, timeout=timeout)
            linecounter+=1
            inc(begin)
        return results
    cpdef apply_function(self,fu):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            list results=[]
        while (begin!=end):
            results.append(fu(deref(begin)))
            inc(begin)
        return results

    cpdef apply_as_c_function(self,object function):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function*>fu)[0]
        for_each(begin,end,cfu)

    cpdef apply_as_c_function_nogil(self,object function):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function_nogil*>fu)[0]
        for_each(begin,end,cfu)

    cpdef apply_as_c_pyfunction(self,object function):
        cdef:
            vector[string].iterator begin = self.v.begin()
            vector[string].iterator end = self.v.end()
            size_t fu=convert_to_c_pyfunction(function)
            pure_c_pyfunction cfu = (<pure_c_pyfunction*>fu)[0]
        for_each(begin,end,cfu)