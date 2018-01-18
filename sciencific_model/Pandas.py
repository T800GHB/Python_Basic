# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:56:05 2018

@author: andrew

Content on this script is from:
http://pandas.pydata.org/pandas-docs/stable/10min.html
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Create a pandas object
Series like a one-dimensional array, but it must store element with same type
DataFrame like a two-dimensional sheet, could be a container of Series

"""

def demo_data():
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
    
    # Performing a descriptive statistic
    row_mean = df.mean()
    print('\nMean on every columns:\n', row_mean)
    
    # Same operation on the other axis
    column_mean = df.mean(1)
    print('\nMean on every column:\n',column_mean)
    
    # Broadcasts
    transpose_series = pd.Series([1,3,5,np.nan,6,8], index = dates).shift(2)
    sub_frame = df.sub(transpose_series, axis='index')
    print('\n DataFrame substrct a Series:\n', sub_frame)
    
    # Applying functions to the data
    cumsum_column = df.apply(np.cumsum)
    print('\nColumn cumsum:\n', cumsum_column)
    
    # Use lambda expression to handle data
    lambda_column = df.apply(lambda x: x.max() - x.min())
    print('Lambda apply on every column:\n', lambda_column)
    
    # Calculate histogram of data
    random_series = pd.Series(np.random.randint(0, 7, size=10))
    histogram = random_series.value_counts()
    print('\nOrignal data in Series:\n', random_series)
    print('\nFirst column is element, Second column is counter:\n', histogram)
    
    """
    Series is equipped with a set of string processing methods in the str attribute 
    that make it easy to operate on each element of the array
    """
    str_series = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
    lower_series = str_series.str.lower()
    print('\nString as lower format:\n', lower_series)
    
    """
    Merge
    pandas provides various facilities for easily combining together Series, DataFrame, 
    and Panel objects with various kinds of set logic for 
    the indexes and relational algebra functionality 
    in the case of join / merge-type operations.
    """
    
    # Concatenating pandas objects together with concat
    matrix_frame = pd.DataFrame(np.random.randn(10, 4))
    # break it into pieces
    pieces = [matrix_frame[:3], matrix_frame[3:7], matrix_frame[7:]]
    concat_frame = pd.concat(pieces)
    print('\nContent in matrix_frame:\n', matrix_frame)
    print('\nConcatenate pieces as orignal:\n', concat_frame)
    
    # SQL style merges. Merge along specific column
    left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
    right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
    merge_frame = pd.merge(left, right, on='key')
    print('\nLeft first:\n', left)
    print('\nRight first:\n', right)
    print('\nMerged result first:\n', merge_frame)
    
    # Merge different key
    left = pd.DataFrame({'key': ['foo', 'bar'], 'lval': [1, 2]})
    right = pd.DataFrame({'key': ['foo', 'bar'], 'rval': [4, 5]})
    merge_frame = pd.merge(left, right, on='key')
    print('\nLeft second:\n', left)
    print('\nRight second:\n', right)
    print('\nMerged result second:\n', merge_frame)
    
    # Append rows to a dataframe
    matrix_sheet = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
    print('\nOrignal matrix_sheet:\n',matrix_sheet)
    signal_row = matrix_sheet.iloc[3]
    matrix_sheet.append(signal_row, ignore_index=True)
    print('\nExtended matrix_sheet:\n', matrix_sheet)
    
    """
    Grouping
    
    Process involving one or more of the following steps
    
        Splitting the data into groups based on some criteria
        Applying a function to each group independently
        Combining the results into a data structure
    
    """
    mix_frame = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
                               'foo', 'bar', 'foo', 'foo'],
                        'B' : ['one', 'one', 'two', 'three',
                               'two', 'two', 'one', 'three'],
                        'C' : np.random.randn(8),
                        'D' : np.random.randn(8)})
    print('\nMix_frame:\n', mix_frame)
    
    # Group element without same value
    # Group element in A column, as key-'foo' and 'bar'
    group_A = mix_frame.groupby('A').sum()
    print('\nSum of group A:\n', group_A)
    # First group as A then B
    group_A_B = mix_frame.groupby(['A','B']).sum()
    print('\nSum of group A followed B:\n', group_A_B)
    
    """
    Reshaping
    """
    
    tuples = list(zip(*[['bar', 'bar', 'baz', 'baz',
                          'foo', 'foo', 'qux', 'qux'],
                         ['one', 'two', 'one', 'two',
                          'one', 'two', 'one', 'two']]))
    
    tuples_index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
    
    small_matrix = pd.DataFrame(np.random.randn(8, 2), index=tuples_index, columns=['A', 'B'])
    
    small_part = small_matrix[:4]
    
    print('\nTuples_index:\n', tuples_index)
    print('\nMatrix construct by tuple_index:\n', small_matrix)
    print('\nPart of small matrix:\n', small_part)
    
    # The stack() method “compresses” a level in the DataFrame’s columns.
    stacked_part = small_part.stack()
    print('\nStack part:\n', stacked_part)
    # Inverse operation of stack() is unstack(), which by default unstacks the last level
    unstack_part = stacked_part.unstack()   #Same as unstack(2)
    print('\nUnstack part:\n', unstack_part)
    # Specify unstack level
    unstack_first = stacked_part.unstack(1)
    unstack_root = stacked_part.unstack(0)
    print('\nUnstack part first level:\n', unstack_first)
    print('\nUnstack part root level:\n', unstack_root)
    
    """
    Pivot Tables
    """
    
    pivot_data = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
                        'B' : ['A', 'B', 'C'] * 4,
                        'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                        'D' : np.random.randn(12),
                        'E' : np.random.randn(12)})
    print('\nOrignal content in piovt:\n', pivot_data)
    # Use 'A' and 'B' as root and first level index, make 'C' as column
    piovt_frame = pd.pivot_table(pivot_data, values='D', index=['A', 'B'], columns=['C'])
    print('\nPivot table:\n', piovt_frame)
    
    """
    Time Series
    Use freq to represent interval
    M - month
    W - week
    D - day
    H - hour
    T - minute
    S - second
    """
    
    # Generate Time series from 2012-1-1, sample 100 time stamp by 1 second 
    rng = pd.date_range('1/1/2012', periods=20, freq='S')
    # Construct a series, rng as index
    ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
    print('\nTime series:\n', ts)
    sum_ts = ts.resample('10S').sum()
    print('\nResample time series:\n', sum_ts)
    # Time zone representation
    ts_utc = ts.tz_localize('UTC')
    print('\nUTC time series:\n', ts_utc)
    ts_us_eastern = ts_utc.tz_convert('US/Eastern')
    print('\nUs Eastern time series:\n', ts_us_eastern)
    
    # Converting between time span representations
    month_rng = pd.date_range('1/1/2012', periods=5, freq='M')
    month_ts = pd.Series(np.random.randn(len(month_rng)), index=rng)
    month_period_series = month_ts.to_period()
    month_time_stamp = month_period_series.to_timestamp()
    print('\nMonth range data:\n', month_ts)
    print('\nMonth period:\n', month_period_series)
    print('\nMonth time stamp:\n', month_time_stamp)
    
    """
    Categorical data
    """
    
    categorical_org = pd.DataFrame({"id":[1,2,3,4,5,6], 
                                      "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})
    print('\nOrignal data in categorical frame:\n', categorical_org)
    
    categorical_org["grade"] = categorical_org["raw_grade"].astype("category")
    print('\nCategorical data as grade:\n', categorical_org["grade"])
    
    # Replace "a","b","c" to "very good", "good", "very bad"
    categorical_org["grade"].cat.categories = ["very good", "good", "very bad"]
    print('\nFirst replace:\n', categorical_org["grade"])
    # Reset categories as "very bad", "bad", "medium", "good", "very good"
    categorical_org["grade"] = categorical_org["grade"].cat.set_categories(
            ["very bad", "bad", "medium", "good", "very good"])
    print('\nReplace grade:\n', categorical_org["grade"])
    
    # Sorting is per order in the categories, not lexical order
    sorted_categorical = categorical_org.sort_values(by="grade")
    print('\nSorted categorical data:\n', sorted_categorical)
    
    # Grouping by a categorical column shows also empty categories
    group_categorical = categorical_org.groupby("grade").size()
    print('\nGrouped categorical data:\n', group_categorical)

def demo_plot():
    # Plot a series    
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    cumsum_ts = ts.cumsum()
    cumsum_ts.plot()
    
    # Plot a DataFrame
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
                      columns=['A', 'B', 'C', 'D'])
    cumsum_df = df.cumsum()
    cumsum_df.plot()
    plt.legend(loc = 'best')
    

def demo_save_load():
    """
    Save and load as csv file
    """
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
                          columns=['A', 'B', 'C', 'D'])
    
    df.to_csv('foo.csv')  
    received_csv = pd.read_csv('foo.csv')
    # Set first column as index. Loaded frame will treat orignal index as first column
    received_csv.set_index('Unnamed: 0', inplace = True)
    
    """
    Save and load as HDF5 file
    """
    # File name and group name
    df.to_hdf('foo.h5','df')
    received_hdf = pd.read_hdf('foo.h5','df')
    
    """
    Reading and writing to MS Excel
    """
    df.to_excel('foo.xlsx', sheet_name='Sheet1')
    recieve_xlsx = pd.read_excel('foo.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
