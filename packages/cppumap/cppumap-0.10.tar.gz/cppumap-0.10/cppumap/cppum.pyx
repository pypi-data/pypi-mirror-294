import cython
cimport cython
import numpy as np
cimport numpy as np
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from libcpp.string cimport string, npos
from libcpp.utility cimport pair
from libcpp.algorithm cimport for_each
from cython.operator cimport dereference as deref, preincrement as inc
import ctypes
_func_cache=[]

#datatypeinfos


#ctypedef int MY_DATA_TYPE_KEY
#ctypedef int MY_DATA_TYPE_VALUE
#MY_DATA_TYPE_C_TYPES_KEY=ctypes.c_int
#MY_DATA_TYPE_C_TYPES_VALUE=ctypes.c_int
#cdef bytes MY_DATA_TYPE_PRINTF_FORMAT = b"%d : %d\n"
#cdef int MY_DATA_TYPE_PRINTF_LF = 80
#MY_DATA_TYPE_PY_KEY=type(int)
#MY_DATA_TYPE_PY_VALUE=type(int)
#MY_DATA_TYPE_STR_KEY='l'
#MY_DATA_TYPE_STR_VALUE='l'

ctypedef unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] MY_UNORDERED_MAP
ctypedef unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator MY_UNORDERED_MAP_ITER
ctypedef pair[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] ipair

ctypedef void (*pure_c_function)(ipair)
ctypedef void (*pure_c_pyfunction)(ipair)
ctypedef void (*pure_c_function_nogil)(ipair) noexcept nogil

cpdef size_t getsizeofpair():
    cdef:
        ipair ipa=(1,1)
        size_t so=sizeof(ipa)
    return so

cpdef size_t convert_to_c_function(object fu):
    CMPFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef size_t convert_to_c_pyfunction(object fu):
    CMPFUNC = ctypes.PYFUNCTYPE(None, ctypes.c_void_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef vector[MY_DATA_TYPE_KEY]  _getiter_key(i):
    cdef:
        vector[MY_DATA_TYPE_KEY] keyvec
        Py_ssize_t iterloop
    if not isinstance(i,(str,bytes)):
        try:
            for iterloop in range(len(i)):
                keyvec.push_back(i[iterloop])
        except Exception:
            keyvec.push_back(i)
    else:
        keyvec.push_back(i)
    return keyvec

cpdef vector[MY_DATA_TYPE_VALUE]  _getiter_val(i):
    cdef:
        vector[MY_DATA_TYPE_VALUE] keyvec
        Py_ssize_t iterloop
    if not isinstance(i,(str,bytes)):
        try:
            for iterloop in range(len(i)):
                keyvec.push_back(i[iterloop])
        except Exception:
            keyvec.push_back(i)
    else:
        keyvec.push_back(i)
    return keyvec


cdef class CppUMap:
    cdef MY_UNORDERED_MAP v

    def __init__(self,*args,**kwargs):
        if len(args)>0:
            self.v.reserve(len(args[0]))
            for k,v in args[0].items():
                self.v[k]=v
    
    cpdef print_data(self,Py_ssize_t limit=150):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            Py_ssize_t counter = 0
        with open("CONOUT$",mode='w',) as f:
            while (begin!=end):
                f.write(str(deref(begin).first))
                f.write('\t:\t')
                f.write(str(deref(begin).second))
                f.write('\n')
                inc(begin)
                counter+=1
                if counter>limit:
                    break

    def __str__(self):
        self.print_data()
        return ""


    def __len__(self):
        return self.v.size()

    def __getitem__(self, MY_DATA_TYPE_KEY key):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  it = self.v.find(key)
        if it == self.v.end():
            raise KeyError(f'{key} not found')
        return deref(it).second

    cpdef getitems(self,i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] resultmap = {}
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec = _getiter_key(i)
            vector[MY_DATA_TYPE_KEY].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_KEY].iterator vec_end=keyvec.end()
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):

                    if deref(begin).first == deref(vec_begin):
                        resultmap[deref(begin).first]=deref(begin).second
                        break
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)
        return resultmap

    def __setitem__(self, MY_DATA_TYPE_KEY key, MY_DATA_TYPE_VALUE value):
        self.v[key] = value

    cpdef void set_np(self, np.ndarray keys, np.ndarray values):
        cdef:
            Py_ssize_t key_array_len=keys.shape[0]
            Py_ssize_t indi
        for indi in range(key_array_len):
            self.v[keys[indi]]=values[indi]

    cpdef void set_tuple_list(self,list[tuple] keys_values):
        cdef:
            Py_ssize_t key_array_len=len(keys_values)
            Py_ssize_t indi
        for indi in range(key_array_len):
            self.v[keys_values[indi][0]]=keys_values[indi][1]

    cpdef get(self, MY_DATA_TYPE_KEY key, default=None):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  it = self.v.find(key)
        if it == self.v.end():
            return default
        return deref(it).second


    def __repr__(self):
        return self.__str__()


    def __delitem__(self, i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec = _getiter_key(i)
            vector[MY_DATA_TYPE_KEY].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_KEY].iterator vec_end=keyvec.end()
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):

                    if deref(begin).first == deref(vec_begin):
                        begin=self.v.erase(begin)
                        break
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)
    cpdef del_by_values(self, i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_VALUE] keyvec = _getiter_val(i)
            vector[MY_DATA_TYPE_VALUE].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_VALUE].iterator vec_end=keyvec.end()
            Py_ssize_t iterloop
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):
                    if deref(begin).second == deref(vec_begin):
                        begin=self.v.erase(begin)
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)

    cpdef del_by_key_and_value(self, list[tuple] i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec
            vector[MY_DATA_TYPE_KEY].iterator key_vec_begin
            vector[MY_DATA_TYPE_KEY].iterator key_vec_end
            vector[MY_DATA_TYPE_VALUE] valvec
            vector[MY_DATA_TYPE_VALUE].iterator val_vec_begin
            vector[MY_DATA_TYPE_VALUE].iterator val_vec_end
            Py_ssize_t iterloop
        for iterloop in range(len(i)):
            keyvec.push_back(i[iterloop][0])
            valvec.push_back(i[iterloop][1])
        key_vec_begin=keyvec.begin()
        key_vec_end=keyvec.end()
        val_vec_begin=valvec.begin()
        val_vec_end=valvec.end()
        with nogil:
            while (key_vec_begin!=key_vec_end) and (val_vec_begin!=val_vec_end):
                while (begin!=end):
                    if (deref(begin).first == deref(key_vec_begin)) and (deref(begin).second == deref(val_vec_begin)):
                        begin=self.v.erase(begin)
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(key_vec_begin)
                inc(val_vec_begin)

    cpdef dict sorted(self,key=None,reverse=False):
        return {k1:v1 for k1,v1 in sorted(dict(self.v).items(),key=key,reverse=reverse)}

    def __iter__(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
        while (begin!=end):
            yield deref(begin).first
            inc(begin)
    cpdef keys(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(deref(begin).first)
                inc(begin)
        return resultvector
    cpdef values(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_VALUE] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(deref(begin).second)
                inc(begin)
        return resultvector
    cpdef items(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[ipair] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(ipair(deref(begin).first, deref(begin).second))
                inc(begin)
        return resultvector

    cpdef dict to_dict(self):
        return self.v

    cpdef pop(self, MY_DATA_TYPE_KEY i):
        x = self.__getitem__(i)
        self.__delitem__(i)
        return x

    cpdef void update(self,object other):
        for k,v in other.items():
            self.v[k] = v

    cpdef copy(self):
        newclass=self.__class__()
        newclass.update(self.v)
        return newclass

    cpdef void append(self, MY_DATA_TYPE_KEY key, MY_DATA_TYPE_VALUE value):
        self.v.insert(ipair(key,value))

    cpdef list apply_function(self,object fu):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            list results=[]
        while (begin!=end):
            results.append(fu(deref(begin).first,deref(begin).second))
            inc(begin)
        return results

    cpdef void apply_as_c_function(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function*>fu)[0]
        for_each(begin,end,cfu)

    cpdef void apply_as_c_function_nogil(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function_nogil*>fu)[0]
        for_each(begin,end,cfu)

    cpdef void apply_as_c_pyfunction(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_pyfunction(function)
            pure_c_pyfunction cfu = (<pure_c_pyfunction*>fu)[0]
        for_each(begin,end,cfu)

