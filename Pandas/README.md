# Pandas - Complete Guide

## Table of Contents
- [Basic Operations](#basic-operations)
- [Data Structures](#data-structures)
- [Data Manipulation](#data-manipulation)
- [Data Analysis](#data-analysis)
- [Data Cleaning](#data-cleaning)
- [Advanced Operations](#advanced-operations)
- [Best Practices](#best-practices)
- [Common Interview Questions](#common-interview-questions)

## Basic Operations

### Creating DataFrames

```python
import pandas as pd
import numpy as np

# From dictionary
data_dict = {
    'name': ['John', 'Anna', 'Peter'],
    'age': [28, 22, 35],
    'city': ['New York', 'Paris', 'London']
}
df = pd.DataFrame(data_dict)

# From list of lists
data_list = [
    ['John', 28, 'New York'],
    ['Anna', 22, 'Paris'],
    ['Peter', 35, 'London']
]
df = pd.DataFrame(data_list, columns=['name', 'age', 'city'])

# From CSV
df = pd.read_csv('file.csv')

# From Excel
df = pd.read_excel('file.xlsx')
```

### Basic Information
```python
# DataFrame info
df.shape          # Dimensions (rows, columns)
df.info()         # Data types and non-null counts
df.describe()     # Statistical summary
df.columns        # Column names
df.dtypes         # Data types of columns
df.head(n)        # First n rows
df.tail(n)        # Last n rows
```

## Data Structures

### Series
```python
# Create Series
s = pd.Series([1, 3, 5, np.nan, 6, 8])

# Series operations
s.value_counts()    # Count unique values
s.unique()          # Get unique values
s.nunique()         # Count number of unique values
s.isna()            # Check for missing values
```

### DataFrame Selection
```python
# Column selection
df['column']              # Single column
df[['col1', 'col2']]     # Multiple columns

# Row selection
df.loc[0]                # Row by label
df.iloc[0]               # Row by position
df.loc[0:2]             # Rows by label range
df.iloc[0:2]            # Rows by position range

# Conditional selection
df[df['age'] > 30]                    # Single condition
df[(df['age'] > 25) & (df['age'] < 35)]  # Multiple conditions
```

## Data Manipulation

### Adding/Removing Data
```python
# Add column
df['new_col'] = df['age'] * 2
df.insert(1, 'new_col', values)

# Add row
df.loc[len(df)] = ['New', 25, 'Berlin']
df = df.append({'name': 'New', 'age': 25, 'city': 'Berlin'}, ignore_index=True)

# Remove column
df.drop('column', axis=1, inplace=True)

# Remove row
df.drop(0, axis=0, inplace=True)
```

### Sorting
```python
# Sort by values
df.sort_values('age', ascending=False)
df.sort_values(['age', 'name'], ascending=[True, False])

# Sort by index
df.sort_index()
```

### Grouping Operations
```python
# Basic groupby
df.groupby('city')['age'].mean()
df.groupby('city').agg({
    'age': 'mean',
    'name': 'count'
})

# Multiple groupby
df.groupby(['city', 'gender'])['age'].mean()

# Group operations
grouped = df.groupby('city')
grouped.sum()
grouped.mean()
grouped.size()
```

## Data Analysis

### Statistical Operations
```python
# Basic statistics
df['age'].mean()
df['age'].median()
df['age'].mode()
df['age'].std()
df['age'].var()
df['age'].min()
df['age'].max()

# Correlation and covariance
df.corr()
df.cov()

# Unique values and counts
df['city'].value_counts()
df['city'].nunique()
```

### Aggregation Operations
```python
# Custom aggregation
df.agg({
    'age': ['min', 'max', 'mean', 'median'],
    'name': 'count'
})

# Rolling calculations
df['rolling_mean'] = df['value'].rolling(window=3).mean()
df['rolling_sum'] = df['value'].rolling(window=3).sum()
```

## Data Cleaning

### Handling Missing Values
```python
# Check missing values
df.isna().sum()
df.isnull().sum()

# Fill missing values
df.fillna(0)                    # Fill with constant
df.fillna(method='ffill')       # Forward fill
df.fillna(method='bfill')       # Backward fill
df.fillna(df.mean())            # Fill with mean

# Drop missing values
df.dropna()                     # Drop rows with any missing values
df.dropna(subset=['column'])    # Drop rows with missing values in specific column
```

### Data Type Conversion
```python
# Convert types
df['age'] = df['age'].astype(int)
df['date'] = pd.to_datetime(df['date'])

# Category type
df['city'] = df['city'].astype('category')
```

### Duplicates
```python
# Check duplicates
df.duplicated()
df.duplicated(subset=['city'])

# Remove duplicates
df.drop_duplicates()
df.drop_duplicates(subset=['city'], keep='last')
```

## Advanced Operations

### Merge and Join
```python
# Merge DataFrames
pd.merge(df1, df2, on='key')
pd.merge(df1, df2, left_on='key1', right_on='key2')

# Different join types
pd.merge(df1, df2, how='left')    # Left join
pd.merge(df1, df2, how='right')   # Right join
pd.merge(df1, df2, how='outer')   # Outer join
pd.merge(df1, df2, how='inner')   # Inner join
```

### Pivot and Melt
```python
# Pivot table
pivot_table = df.pivot_table(
    values='value',
    index='row_category',
    columns='col_category',
    aggfunc='sum'
)

# Melt DataFrame
melted_df = pd.melt(
    df,
    id_vars=['id'],
    value_vars=['col1', 'col2'],
    var_name='category',
    value_name='value'
)
```

### Window Functions
```python
# Ranking
df['rank'] = df.groupby('category')['value'].rank(method='dense')

# Shifting
df['prev_value'] = df.groupby('category')['value'].shift(1)
df['next_value'] = df.groupby('category')['value'].shift(-1)

# Cumulative calculations
df['cumsum'] = df.groupby('category')['value'].cumsum()
df['cummax'] = df.groupby('category')['value'].cummax()
```

## Best Practices

1. Memory Efficiency
```python
# Optimize data types
df = df.astype({
    'int_col': 'int32',
    'float_col': 'float32',
    'category_col': 'category'
})

# Read large files in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process(chunk)
```

2. Performance Tips
```python
# Use vectorized operations instead of loops
# Good:
df['new_col'] = df['col'] * 2

# Bad:
for i in range(len(df)):
    df.loc[i, 'new_col'] = df.loc[i, 'col'] * 2

# Use query for complex filtering
df.query('age > 25 and city == "London"')
```

## Common Interview Questions

1. How to handle missing values in a DataFrame?
```python
# Multiple strategies
df.fillna(df.mean())                 # Fill with mean
df.fillna(method='ffill')            # Forward fill
df['col'].interpolate()              # Interpolation
```

2. How to find and remove duplicates?
```python
# Find duplicates
duplicates = df[df.duplicated(keep=False)]

# Remove duplicates keeping first occurrence
df.drop_duplicates(subset=['key_column'])
```

3. How to reshape data?
```python
# Wide to Long
pd.melt(df, id_vars=['id'], value_vars=['col1', 'col2'])

# Long to Wide
df.pivot(index='id', columns='category', values='value')
```

4. How to perform group operations?
```python
# Multiple aggregations
df.groupby('category').agg({
    'numeric_col': ['mean', 'sum', 'count'],
    'string_col': lambda x: ','.join(x)
})
```

Remember:
- Always check data types before operations
- Use vectorized operations when possible
- Consider memory usage for large datasets
- Document complex transformations
- Handle edge cases and missing values
- Use appropriate data types for columns
- Leverage built-in Pandas functions instead of writing custom logic
