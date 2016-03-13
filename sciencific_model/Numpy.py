# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20:54:01 2016

@author: T800GHB

This file will demostrate how use basic function offered by numpy model.

Numpy is designed to stroe multi-dimensional array, it's called ndarray.
Array in numpy is so different from array in native python.
In numpy, dimensions named axes, number of axes called rank.
For example, 3D coordiante [1,2,3] is a array of rank 1 and length 3.
[[1,2,3],
[4,5,6]]    
is a array of rank 2. Length of first rank is 2, and second rank is 3.

There some introduction about attribute of numpy's array:
ndarray.ndim
    rank of ndarray
ndarray.shape
    dimensions of array. It's a tuple indicate length of array in each dimension.
ndarray.size
    total elements of array. It equal to product of element in shape.
ndarray.dtype
    type of element in array.
ndarray.itemsize
    size of element in array.
ndarray.data
    buffer that store the real element of array. We will not use it directly.
    but get reference.
    
Function introduction

Array creation:
arange, array, copy, empty, empty_like, eye, fromfile, fromfunction, identity, linspace, logspace, mgrid, ogrid, ones, ones_like, r , zeros, zeros_like 

Convertion:
astype, atleast 1d, atleast 2d, atleast 3d, mat 

Formation operation:
array split, column stack, concatenate, diagonal, dsplit, dstack, hsplit, hstack, item, newaxis, ravel, repeat, reshape, resize, squeeze, swapaxes, take, transpose, vsplit, vstack 

Inquiry:
all, any, nonzero, where 

Sort:
argmax, argmin, argsort, max, min, ptp, searchsorted, sort 

Calculation:
choose, compress, cumprod, cumsum, inner, fill, imag, prod, put, putmask, real, sum 

Statistics:
cov, mean, std, var 

Linear algebra:
cross, dot, outer, svd, vdot    
"""

"""
I just want to distinguish between numpy and native python,
so choose import numpy as np instead of from numpy import *
"""
import numpy as np

def demo_attribute():
    """
    np.arange(n) is a function that return a continuous integer from 0 to n.
    Pass (n, m , s) to arange means create sequence integer from n to m with interval s.
    np.reshape(*args) is a function that form a new array with specific dimensions.    
    """
    a = np.arange(12).reshape(3,4)
    print('Data :\n', a)
    print('Shape:\n', a.shape)
    print('Rank:\n', a.ndim)
    print('Type:\n', a.dtype.name)
    print('Size of element:\n', a.itemsize)
    print('size of array:\n', a.size)
    
def demo_create():
    """
    Create numpy array by ways:
    1.normal list or tuple.
    2.numpy function. For example, zeros, ones etc.
    """
    a = np.array([1,2,3])
    print('Array create from list\n', a)
    b = np.array([(1.1,2.0,3.6),(4,5,6)])
    print('Two dimensional array create from list of tuple\n',b)
    """
    Pass a type as paramter to array, new array will create as this type.
    """
    f = np.array([[1,2], [3,4]], dtype = complex)
    print('Array with complex type\n', f)
    """
    zeros() will create a array with all zero.
    ones() will create a array with all one.
    empty() will create a array with random number that rely on memory state.
    Pass a tuple as shape to those function.
    Those function use float64 as default type.
    """
    z = np.zeros((3,4))
    print('All zero array\n', z)
    o = np.ones((2,5), dtype = int)
    print('All one array\n', o)
    e = np.empty((2,3))
    print("'empty' array\n", e)
    """
    Create a sequence that contain specific number of element.
    linspace could produce sequence with high precision.
    """
    l = np.linspace(1, 20, 16)
    print('Line space sequence\n', l)
    
def demo_calculation():
    """
    Element-wise calculation is general operation on numpy array.
    """
    a = np.array([2, 4, 7, 9])
    b = np.arange(4)
    c = a + b
    print('First array\n',a,'\nSecond array\n',b,'\nSum\n', c)
    
    p = b** 2
    print('Second array with power 2\n', p)
    
    bool_array = a < 5
    print('Element less than 5 in first array\n', bool_array)
    
    """
    Array multiplication with * operation will element-wise calculation.
    If you want to matrix-like multiplication, please use dot() function.
    """
    A = np.array([[2,3],[1, 4]])
    B = np.array([[3,4],[2, 5]])
    e_p = A * B
    m_p = np.dot(A,B)
    print('\nArray A\n', A, '\nArray B\n', B, '\n* product\n',e_p,
          '\ndot product\n', m_p)
    
    """
    *= , +=, -= etc operator will modify current array, but create
    new one.
    """
    A += 10
    B *= 2
    print('\n A += 10 \n', A, '\n B*= 2 \n', B)
    
    """
    Array Calculation with different data type will produce result that
    upcast to higher precision.
    """
    AF = np.array([[1.1, 2.3, 4.8],[1.4, 4.5, 5.8]])
    BI = np.ones((2,3), dtype = int)
    ABF = AF + BI
    print('\n Array with float data \n', AF, '\n Array with integer data\n', BI,
          '\n Sum \n', ABF)
    
    """
    sum(), min(), max() will work on all element in array, but if you give 
    specific axis or dimension as first parameter, those function will just
    work on that limited range    
    """
    s_af = AF.sum()
    s_af_1 = AF.sum(axis = 0)
    min_af = AF.min()
    min_af_2 = AF.min(axis = 1)
    max_af = AF.max()
    max_af_1 = AF.max(axis = 0)
    print('\n Sum of AF\n', s_af, '\n Sum of AF on dimension 1 \n', s_af_1,
          '\n min of AF\n', min_af, '\n min of AF on dimension 2\n', min_af_2,
          '\n max of AF\n', max_af, '\n max of AF on dimension 1\n', max_af_1)
          
    """
    Numpy include some genral/utility function for element-wise operation.
    Those operation are basic calcuation; for example sqrt , exp etc.    
    """
    e_af = np.exp(AF)
    sq_af = np.sqrt(AF)
    print('\n AF exp \n', e_af, '\n AF sqrt \n',sq_af)
    
def demo_index():
    """
    [] is interface to index element or more than one in array.
    Index one dimension array :
    [n] could index one element
    [n:m] could index a range named slice.
    If miss n means start from 0, m means end to max.    
    """
    a = np.arange(10)**2
    a5 = a[4]
    a37 = a[2:6]
    print('Data\n',a,'\n Fifth element \n', a5, '\n Element from 3 to 7\n',a37)

    """
    If you provide a addtional : and parameter after range : operator means 
    interval on this range.
    If additional paramenter is negtive integer means reversed order to index.
    """    
    a062 = a[: 6 : 2]
    print('\n Element from 0 to 6 with 1 interval \n', a062)
    a942 = a[::-2]
    print('\n Elemnt from 9 to 0 with 1 interval \n', a942) 
    
    """
    Index a element or a range in multi-dimensional array, you need to 
    set index for every axis, use comma to separate different dimension.
    Use : on to a axis means select all element associate with to this dimension.
    Miss parameter on a dimension means use all slice on this dimension.
    ... means more than one :. For example [:,:,:,1] equal [...,1]
    select all dimensions before or after this one.
    """
    b =         np.arange(20).reshape(5,4)    
    b34 =       b[2,3]
    b052 =      b[0:5, 1]       #each row in the second column of b
    b_ar_4 =    b[:,3]          #equivalent to previrous example
    b_24_ac =   b[1:3, :]       # each column in the second and third row of b
    b_last =    b[-1]           #the last row
    print('\n Data \n', b, '\n Element on 3 row , 4 column \n', b34,
          '\n each row in the second column \n', b_ar_4,
          '\n each column in the second and third row \n', b_24_ac,
          '\n last row \n', b_last)
    
    c =         np.arange(24).reshape(2,3,4)
    c1 =        c[...,1]
    c2 =        c[1,...]
    print('\n 3 dimension array\n', c, '\n No.2 element at last dimension\n',c1,
    '\n No.2 element at first dimension\n',c2, '\n Flattened data is :')
    
    """
    flat attribute will provide a iterator that sequence of iteration will 
    flatten as dimensions order.
    """
    for item in c.flat:
        print(item)
    """
    More function about index, please reference newaxis, 
    ndenumerate, indices, index exp
    """
    
def demo_senior_index():
    """
    Use array to index array
    """
    a = np.arange(12)
    i = np.array([1,2,3,6,7])
    r = a[i]
    print('Data a\n', a, '\nIndex array\n',i,'\nResult a[i]\n',r)
    
    """
    Use  a bidimensional array of indices, result will be the same
    shape of indices
    """
    j = np.array([[1,2],[8,10]])
    r = a[j]
    print('Index array\n',j, '\nResult [j]\n',r)
    
    """
    If the data is multi-dimensional array, every unique 
    array of indices will use first dimension.
    """
    palette = np.array( [ [0,0,0],                # black
                    [255,0,0],              # red
                    [0,255,0],              # green
                    [0,0,255],              # blue
                    [255,255,255] ] )       # white
    image = np.array( [ [ 0, 1, 2, 0 ],        
                  [ 0, 3, 4, 0 ]  ] )
    r = palette[image]
    print('Multi-dimension data\n',palette,'\nArray of indices\n',image,
          '\nResult \n',r)
    """
    Use array to preform multi-dimensional index, those array must have 
    same shape.
    This techique could combine with slice or bind indices of array to a list,
    then use this list to preform index.
    """
    a.shape = (3,4)
    x = np.array([[0,1],[1,0]])
    y = np.array([[2,2],[1,3]])
    r = a[x,y]
    r_f = a[x,2]
    r_s = a[:,y]
    l = [x,y]
    r_l = a[l]
    print('Change shape of a as (3,4)\n',a,
          '\nArray of indices x\n',x,'\nArray of indices y\n',y,
          '\nSame result with a[x,y] or l = [x,y] , a[l]\n',r,'\n\n',r_l,
          '\nResult a[x,2]\n',r_f,'\nSlice reslult \n',r_s)
    
    """
    Argmax will return index that max element on specific dimension.
    """
    r = a.argmax(axis = 0)
    print('Max element index on each column\n',r)
    
    """
    Use array of indices to assign value.
    If there are same element on this array of indices,
    reserve last assignment.
    """
    a.shape = (12,)   
    print('Change shape of a to (1,12)\n',a)
    a[[1,3,5]] = 100
    print('\nassign [1,3,5] and to 100\n',a)
    a[[0,0,4]] = 200
    print('\nassign [0,0,4] to 200\n',a)
    
    
def demo_shape():
    """
    Shape of array indicated by length on each axis.
    So ,if you want to reshape array , just change the lenght of axis.
    ravel() will return a flattened array.
    Shape attribute will control shape of itself, change it , shape different.
    reshape() will return a new array with new shape.
    transpose() will switch location of element in array by diagonal.
    resize will change itself, but total element could be changed,
    if the elemet does not exist, pad with zeros.   
    If you give a -1 as length of axis, it will be infered automatically,
    Only 1, or it will confront ambiguousness.
    """
    a = np.floor(10*np.random.random((3,4)))  #floor will reserve integer part.
    print('Data\n',a)
    a.shape = (6,2)
    print('Shape as (6,2)\n',a)
    a.transpose()
    print('Transposed array\n',a)
    a.resize(2,8)
    print('resize as 2,8\n',a)
    a.shape = (2,-1,4)
    print('3D array\n',a)

def demo_formation():
    """
    stack function will assemble two block data.
    Assembly will operate on dimension both they have.
    vstack operate on vertical direction.
    hstack operate on horizontal direction.
    More function, reference column_stack, row_stack, concatenate
    """
    a = np.floor(10*np.random.random((2,2)))
    b = np.floor(10*np.random.random((2,2)))
    avb = np.vstack((a,b))
    ahb = np.hstack((a,b))
    print('Data a\n',a,'\nData b\n',b,'\nvertical assembly\n',avb,
          '\nhorizontal assembly\n',ahb)
          
    """
    hsplit function will split array with horizontal direction.
    vsplit function do it on vertical direction.
    If you give a tuple as second argument, that will be treated as formation
    you want to split.
    """
    c = np.arange(24).reshape(2,12)
    ch = np.hsplit(c, 3)
    cv = np.vsplit(c,2)
    c34 = np.hsplit(c,(3,5,8))
    print('\nData c\n',c,'\nHorizontal split to 3 part\n',ch,
          '\nVertical split to 2 part\n',cv,
          '\nHorizontal split as specific\n',c34)
    
def demo_copy():
    """
    There are 3 satuation about duplication:
    reference copy(No data copy), view copy(No data copy), deep copy(data copy).
    reference copy will not create new object, you can treat it as alias.
    view copy will create new view, new view will share data with orignal one,
    but they colud own different form indpendently, such as shape.
    Slice of array is view of part that you have selected.
    """
    #Reference copy
    a = np.arange(12)
    b = a
    print('Data a\n',a,'\nData b\n',b,'\na is b\n',a is b)
    b.shape = (3,4)
    print('Data b change shape to \n',b.shape, '\nShape of data a \n',a.shape)
    
    #view copy
    c = a.view()
    c.shape = (6,2)
    print('c is view of a, c is a?\n',c is a, 
          '\nbase of c is a?\n', c.base is a,
          '\n Shape of c\n',c.shape,
          '\n Shape of a\n', a.shape)
    c[1,0] = 1000
    print('c change element at [1,0] be 1000, data c now\n',c,
          '\ndata a now\n',a)       #Data has changed.
          
    #Deep copy
    d = a.copy()
    print('Data d \n',d,'\nd is a?\n',d is a,'\nbase of d is a?\n', d.base is a)
    d[1,2] = 500
    print('d change  element at [1,2] be 500, data d now\n',d,
          '\ndata a now\n',a)
          
def demo_broadcast():
    """
    Broadcast rule:
    1.Have same dimensions/shape, if they don't , pid 1 to that part.
    2.Shape of output array is max length on each dimension of input array.
    3.If they don't have same length at same axis, can't do calculation.
    4.Use first group value , if they have 1 length on that dimension.
    Maybe there are some wrong comprehension, i will fixed later.
    """
    a = np.arange(0,60,10).reshape(-1,1)
    b = np.arange(0,5)                     
    c = a + b
    print('Data a\n',a,'\nShape a\n',a.shape,
          '\nData b\n',b,'\nShape b\n',b.shape,
          '\na + b\n',c,'\nShape of reuslt\n',c.shape)
    """
    ogrid return two array that could use broadcast calculation.
    """
    x,y = np.ogrid[0:1:4j, 0:1:3j]
    print('Two array to form grid, use broadcast\n',x,'\n',y)
    