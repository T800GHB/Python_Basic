# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:56:05 2018

@author: andrew
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Create a pandas object
Series like a one-dimensional array, but it must store element with same type
DataFrame like a two-dimensional sheet, could be a container of Series
"""


s = pd.Series([1,3,5,np.nan,6,8])
print('\nCreate a pandas series:\n', s)

dates = pd.date_range('20130101', periods=6)
print('\ndata_range: \n', dates)

df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print('\nCreate DataFrame with specific index and columns:\n', df)

df_dict = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20130102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })

print('\nCreate a DataFrame from dict:\n', df_dict)
print('\nType in this DataFrame:\n', df_dict.dtypes)

"""
View data from object
"""

top_rows = df.head()
print('\nTop rows of frame:\n', top_rows)
print('\nType of top rows is:\n', type(top_rows))

bottom_rows = df.tail(3)
print('\nLast 3 rows of data:\n', bottom_rows)

data_index = df.index
print('\nIndex of DataFrame:\n', data_index)

data_columns = df.columns
print('\nColumns of DataFrame:\n', data_columns)

data_content = df.values
print('\nContent in DataFrame:\n', data_content)

data_statistic = df.describe()
print('\nStatistic for this DataFrame:\n', data_statistic)

data_transpose = df.T
print('nTranspose of DataFrame:\n', data_transpose)

index_sort = df.sort_index(axis=0, ascending=False)
print('Sort DataFrame by axis 0(index):\n', index_sort)

columns_sort = df.sort_index(axis=1, ascending=False)
print('Sort DataFrame by axis 1(columns):\n', columns_sort)

one_columns_sort = df.sort_values(by = 'B')
print('Sort DataFrame by column B:\n', one_columns_sort)


"""
Get data from DataFrame by index or columns
"""
# Equivalent to df.A
columns_A = df['A']
print('\nContent from column A:\n', columns_A)

# Selecting via [], which slices the rows.
rows_1_3 = df[0:3]
print('\nSelect data from 1 to 3 rows:\n', rows_1_3)

rows_2_4 = df['20130102':'20130104']
print('\nSelect data by index value:\n', rows_2_4)

"""
Selection by label
"""

corss_section = df.loc[dates[0]]
print('\nGetting a cross section using a label:\n', corss_section)

multi_section = df.loc[:,['A','B']]
print('\nSelecting on a multi-axis by label:\n', multi_section)

range_section = df.loc['20130102':'20130104',['A','B']]
print('\nShowing label slicing, both endpoints are included:\n', range_section)

part_row = df.loc['20130102',['A','B']]
print('\nReduction in the dimensions of the returned object:\n', part_row)

one_element = df.loc[dates[0],'A']
print('\nGetting fast access to a scalar:\n', one_element)

"""
Selection by Position
"""
one_row = df.iloc[3]
print('\nSelect via the position of the passed integers:\n', one_row)

region_selection = df.iloc[3:5,0:2]
print('\nBy integer slices, acting similar to numpy:\n', region_selection)

index_selction = df.iloc[[1,2,4],[0,2]]
print('\nLists of integer position locations, similar to the numpy style:\n', index_selction)

element_at = df.iat[1,1]
print('\nGetting fast access to a scalar:\n', element_at)

"""
Boolean Indexing
"""
above_zeros = df[df.A > 0]
print('\nUsing a single column’s values to select data:\n', above_zeros)

region_boolean = df[df > 0]
print('\nSelecting values from a DataFrame where a boolean condition is met:\n', region_boolean)

"""
Set value is similar to get value
1.Get location or region
2.Assign value to this position
"""
    

 
"""
Missing Data
pandas primarily uses the value np.nan to represent missing data.
"""

# Reindexing allows you to change/add/delete the index on a specified axis. 
# This returns a copy of the data.

df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
df1.loc[dates[0]:dates[1],'E'] = 1
print('\nReindex data:\n', df1)

# To drop any rows that have missing data.
without_nan = df1.dropna(how='any')
print('\nData without Nan:\n', without_nan)

# Filling missing data
fill_data = df1.fillna(value = 5)
print('\nNan element replaced by 5:\n', fill_data)

# To get the boolean mask where values are nan
nan_mask = pd.isna(df1)
print('\nMask for nan elements:\n', nan_mask)
