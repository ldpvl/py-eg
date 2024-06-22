import pandas as pd
import numpy as np

# create a sample dataframe
df = pd.DataFrame({'A': ['foo', 'foo', 'bar', 'bar', 'foo', 'foo', 'bar', 'bar'],
                   'C': [5, 6, 7, 8, 9, 1, 2, 3]})

# define custom function to calculate coefficient of variation
def calc_cv(x):
    return np.std(x, ddof=0) / np.mean(x)


agg = df.groupby('A').agg(sum_c=('C', 'sum'))
print(agg)
print(f"Coefficient of variation is {calc_cv(agg['sum_c'].tolist())}")

# in this special case, we need to pass .values to calc_cv as calc_cv expects an numpy array or panda Series
agg = df.groupby('A').agg(sum_c=('C', 'sum')).agg(cv=('sum_c', lambda _: calc_cv(_.values)))

# The below will raise ValueError: Length mismatch: Expected axis has 2 elements, new values have 1 elements
# agg = df.groupby('A').agg(sum_c=('C', 'sum')).agg(cv=('sum_c', calc_cv))




