import cython
cimport cython
import numpy as np
cimport numpy as np
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from libcpp.unordered_set cimport unordered_set
from cpython cimport array
import array
from libc.stdio cimport printf
from libcpp.algorithm cimport sort, for_each
from cython.operator cimport dereference as deref, preincrement as inc
import ctypes
_func_cache=[]

#datatypeinfos

#ctypedef unsigned short MY_DATA_TYPE
#MY_DATA_TYPE_C_TYPES=ctypes.c_ushort
#cdef bytes MY_DATA_TYPE_PRINTF_FORMAT = b"%d, "
#cdef int MY_DATA_TYPE_PRINTF_LF = 20
#MY_DATA_TYPE_PY=type(int)
#MY_DATA_TYPE_STR='H'

#ctypedef int MY_DATA_TYPE
#MY_DATA_TYPE_C_TYPES=ctypes.c_int
#cdef bytes MY_DATA_TYPE_PRINTF_FORMAT = b"%d, "
#cdef int MY_DATA_TYPE_PRINTF_LF = 80
#MY_DATA_TYPE_PY=type(int)
#MY_DATA_TYPE_STR='l'

ctypedef vector[MY_DATA_TYPE] MY_DATA_TYPE_1D_VECTOR
ctypedef vector[MY_DATA_TYPE_1D_VECTOR] MY_DATA_TYPE_2D_VECTOR
ctypedef vector[MY_DATA_TYPE].iterator MY_DATA_TYPE_ITER
ctypedef unordered_set[MY_DATA_TYPE] MY_DATA_TYPE_UNORDERED_SET

ctypedef fused MY_DATA_TYPE_FUSED:
    list[MY_DATA_TYPE]
    vector[MY_DATA_TYPE]
    tuple[MY_DATA_TYPE]
    set[MY_DATA_TYPE]
    np.ndarray[MY_DATA_TYPE]
    array.array[MY_DATA_TYPE]

ctypedef void (*pure_c_function)(MY_DATA_TYPE val)
ctypedef void (*pure_c_pyfunction)(MY_DATA_TYPE val)
ctypedef void (*pure_c_function_nogil)(MY_DATA_TYPE val) noexcept nogil


cpdef size_t convert_to_c_function(object fu):
    CMPFUNC = ctypes.CFUNCTYPE(None, MY_DATA_TYPE_C_TYPES)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef size_t convert_to_c_pyfunction(object fu):
    CMPFUNC = ctypes.PYFUNCTYPE(None, MY_DATA_TYPE_C_TYPES)
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
    def __init__(self, dtype):
        self.dtype = dtype
        self.current_address = 0
        self.current_buffer = 0
        self.current_size = 0

    def __get__(self, instance, owner):
        cdef:
            size_t current_address_new=instance._get_vector_address()
            size_t current_size_new=len(instance)
            object haystack_buffer
        if current_address_new != self.current_address or current_size_new != self.current_size:
            haystack_buffer = (self.dtype * (current_size_new)).from_address(current_address_new)
            self.current_address=current_address_new
            self.current_buffer = np.frombuffer(haystack_buffer,dtype=self.dtype)
            self.current_size = current_size_new
        return self.current_buffer

    def __set__(self, instance, value):
        instance.__dict__[self.name] = np.array([],self.dtype)

cdef class CppVector:
    cdef MY_DATA_TYPE_1D_VECTOR v
    nparray=NpDescriptor(MY_DATA_TYPE_C_TYPES)

    def __init__(self,*args,**kwargs):
        cdef:
            Py_ssize_t indi
            Py_ssize_t len_args = 0
        if len(args)>0:
            len_args=len(args[0])
        for indi in range(len_args):
            self.v.push_back(args[0][indi])


    def print_array(self):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            int linebreak_counter = 1
            const char * vec_int_format_c = MY_DATA_TYPE_PRINTF_FORMAT

        with nogil:
            printf('[')
            while (begin!=end):
                printf(vec_int_format_c, deref(begin))
                if linebreak_counter % MY_DATA_TYPE_PRINTF_LF == 0:
                    printf('\n')
                linebreak_counter+=1
                inc(begin)
            printf(']')
        return ""
    
    def __str__(self):
        return(str(self.nparray))

    def __repr__(self):
        return self.__str__()


    def __add__(self, object i):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            Py_ssize_t indi
            Py_ssize_t len_iters
            vector[MY_DATA_TYPE] results

        try:
            len_iters=len(i)
        except Exception:
            i=[i]
            len_iters=len(i)

        results.reserve(self.v.size()+len_iters)
        while (begin!=end):
            results.push_back(deref(begin))
            inc(begin)
        for indi in range(len_iters):
            results.push_back(i[indi])
        return self.__class__(results)

    def __len__(self):
        return (<size_t>self.v.size())

    def __delitem__(self, i):
        cdef:
            int[:] dellistview
            int indi
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
        dellistview=_get_index_np(i)
        with nogil:
            for indi in range(dellistview.shape[0]):
                if dellistview[indi]-indi >= self.v.size():
                    continue
                if begin + (dellistview[indi]-indi) < end:
                    self.v.erase(begin + (dellistview[indi]-indi))

    def __setitem__(self, i, MY_DATA_TYPE v):
        cdef:
            int[:] setlistview
            int indi
            size_t vecsize=self.v.size()
        setlistview=_get_index_np(i)
        with nogil:
            for indi in range(setlistview.shape[0]):
                if setlistview[indi] < vecsize:
                    self.v[setlistview[indi]]= v

    def __getitem__(self,i):
        return self.nparray[i]

    def __contains__(self,MY_DATA_TYPE i):
        return self.index(i) > -1

    cpdef insert(self, i, MY_DATA_TYPE v):
        cdef:
            int[:] setlistview
            int indi
            int indicounter= 0
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
        setlistview=_get_index_np(i)
        with nogil:
            for indi in range(setlistview.shape[0]):
                if begin+(setlistview[indi]+indicounter)<end:
                    self.v.insert(begin+(setlistview[indi]+indicounter), v)
                    end = self.v.end()
                    indicounter+=1


    cpdef void append(self, MY_DATA_TYPE i):
        self.v.push_back(i)

    cpdef size_t _get_vector_address(self):
        return (<size_t>self.v.data())

    cpdef void remove(self,MY_DATA_TYPE i):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
        with nogil:
            while (begin!=end):
                if deref(begin) == i:
                    self.v.erase(begin)
                    break
                inc(begin)



    cpdef void remove_all(self,MY_DATA_TYPE i):
        cdef:
            vector[int] results=self.index_all(i)
        self.__delitem__(results)

    cpdef int index(self, MY_DATA_TYPE i):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            int counter = -1
        with nogil:
            while (begin!=end):
                if deref(begin) == i:
                    return counter+1
                counter+=1
                inc(begin)

    cpdef vector[int] index_all(self, MY_DATA_TYPE i):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            vector[int] results
            int indexcounter=0

        with nogil:
            while (begin!=end):
                if deref(begin) == i:
                    results.push_back(indexcounter)
                indexcounter+=1
                inc(begin)
        return results

    cpdef pop(self, Py_ssize_t i):
        if self.v.size()<=i:
            raise IndexError()
        x = self.v[i]
        self.__delitem__(i)
        return x

    cpdef group_items(self):
        cdef:
            unordered_map[MY_DATA_TYPE,vector[int]] results
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
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
            MY_DATA_TYPE_2D_VECTOR result_vector = [[]]
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

    cpdef split_at_value(self,i):
        cdef:
            vector[int] results=self.index_all(i)
        return self.split_at_index(results)

    cpdef void extend(self, MY_DATA_TYPE_FUSED n):
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

    cpdef extend_np(self, MY_DATA_TYPE[:] n):
        cdef:
            Py_ssize_t i
            Py_ssize_t len_iters = n.shape[0]
        with nogil:
            for i in range(len_iters):
                self.v.push_back(n[i])

    cpdef void reserve(self, int n):
        self.v.reserve(n)

    cpdef void resize(self, int n):
        self.v.resize(n)

    cpdef void shrink_to_fit(self):
        self.v.shrink_to_fit()

    cpdef int count(self, MY_DATA_TYPE i):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            int counter = 0
        with nogil:
            while (begin!=end):
                if deref(begin) == i:
                    counter+=1
                inc(begin)
        return counter

    cpdef reverse(self):
        cdef:
            vector[MY_DATA_TYPE].reverse_iterator begin = self.v.rbegin()
            vector[MY_DATA_TYPE].reverse_iterator end = self.v.rend()
            vector[MY_DATA_TYPE] results
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

    cpdef list to_list(self):
        return self.nparray.tolist()

    cpdef tuple to_tuple(self):
        return tuple(self.nparray)

    cpdef to_set(self):
        cdef:
            MY_DATA_TYPE_UNORDERED_SET results
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
        while (begin!=end):
            results.insert(deref(begin))
            inc(begin)
        return results

    cpdef apply_function(self,fu):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            list results=[]
        while (begin!=end):
            results.append(fu(deref(begin)))
            inc(begin)
        return results

    cpdef apply_as_c_function(self,object function):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function*>fu)[0]
        for_each(begin,end,cfu)

    cpdef apply_as_c_function_nogil(self,object function):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function_nogil*>fu)[0]
        for_each(begin,end,cfu)

    cpdef apply_as_c_pyfunction(self,object function):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
            size_t fu=convert_to_c_pyfunction(function)
            pure_c_pyfunction cfu = (<pure_c_pyfunction*>fu)[0]
        for_each(begin,end,cfu)


    cpdef sort(self):
        cdef:
            vector[MY_DATA_TYPE].iterator begin = self.v.begin()
            vector[MY_DATA_TYPE].iterator end = self.v.end()
        with nogil:
            sort(begin, end)