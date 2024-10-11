import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
import alimentos

# load data
data = alimentos.todos_alimentos

# Choose columns to keep
columns = ['Energia kcal', 'Proteína', 'Lipídeos', 'Colesterol',
           'Carboidrato', 'Fibra Alimentar', 'Ferro', 'Sódio']

data = data[columns]

# Fill NaN values with 0 and replace Tr with 0 and replace ' ' with 0
data.fillna(0, inplace=True)
data = data.replace('Tr', 0)
data['Ferro'] = data['Ferro'].str.replace(' ', '0')

# delete lines with values equal to *
data = data.replace('*', np.nan)
data = data.dropna()

print(data.info())
print(data.describe())

# Convert other columns to int
int_cols = ['Energia kcal', 'Colesterol', 'Sódio']
data[int_cols] = data[int_cols].apply(
    lambda x: x.astype(int))

# Get all columns that are not int
float_cols = data.columns.drop(int_cols)

# # Convert to float
data[float_cols] = data[float_cols].apply(
    lambda x: x.str.replace(',', '.').astype(float))

# Fill NaN values with 0
data.fillna(0, inplace=True)

print(data.info())
print(data.describe())


# Generate and export the report
profile = ProfileReport(data, title='Relatório de Análise de Dados',
                        html={'style': {'full_width': True}}, sort=None)

profile.to_file("profile.html")
