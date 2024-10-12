import pandas as pd
import numpy as np

tipos = [
    'Cereais e derivados',
    'Verduras, hortaliças e derivados',
    'Frutas e derivados',
    'Gorduras e óleos',
    'Pescados e frutos do mar',
    'Carnes e derivados',
    'Leite e derivados',
    'Bebidas (alcoólicas e não alcoólicas)',
    'Ovos e derivados',
    'Produtos açucarados',
    'Miscelâneas',
    'Outros alimentos industrializados',
    'Alimentos preparados',
    'Leguminosas e derivados',
    'Nozes e sementes'
]

print(tipos)

cereais_derivados = pd.read_csv('data/cereais_derivados.csv', sep=';')

verduras_hortalicas_derivados = pd.read_csv(
    'data/verduras_hortalicas_derivados.csv', sep=';')

frutas_derivados = pd.read_csv('data/frutas_derivados.csv', sep=';')

gorduras_oleos = pd.read_csv('data/gorduras_oleos.csv', sep=';')

pescados_frutos_do_mar = pd.read_csv(
    'data/pescados_frutos_do_mar.csv', sep=';')

carnes_derivados = pd.read_csv('data/carnes_derivados.csv', sep=';')

leite_derivados = pd.read_csv('data/leite_derivados.csv', sep=';')

bebidas = pd.read_csv('data/bebidas.csv', sep=';')

ovos_derivados = pd.read_csv('data/ovos_derivados.csv', sep=';')

produtos_acucarados = pd.read_csv('data/produtos_acucarados.csv', sep=';')

miscelaneas = pd.read_csv('data/miscelaneas.csv', sep=';')

outros_alimentos_industrializados = pd.read_csv(
    'data/outros_alimentos_industrializados.csv', sep=';')

alimentos_preparados = pd.read_csv('data/alimentos_preparados.csv', sep=';')

leguminosas_derivados = pd.read_csv('data/leguminosas_derivados.csv', sep=';')

nozes_sementes = pd.read_csv('data/nozes_sementes.csv', sep=';')

todos_alimentos = pd.concat([cereais_derivados, verduras_hortalicas_derivados, frutas_derivados, gorduras_oleos, pescados_frutos_do_mar, miscelaneas,
                             carnes_derivados, leite_derivados, bebidas, ovos_derivados, produtos_acucarados, outros_alimentos_industrializados, alimentos_preparados, leguminosas_derivados, nozes_sementes], ignore_index=True)

# print(todos_alimentos.info())

# print(todos_alimentos.head())

# Fill NaN values with 0 and replace Tr with 0 and replace ' ' with 0
todos_alimentos.fillna(0, inplace=True)
todos_alimentos = todos_alimentos.replace('Tr', 0)

# delete lines with values equal to *
todos_alimentos = todos_alimentos.replace('*', np.nan)
todos_alimentos = todos_alimentos.dropna()

# int_cols = ['Energia kcal', 'Colesterol', 'Sódio']
# int_cols = ['Energia kcal']

# todos_alimentos[int_cols] = todos_alimentos[int_cols].apply(
#     lambda x: x.astype(int))
todos_alimentos['Energia kcal'] = todos_alimentos['Energia kcal'].astype(int)

todos_alimentos.describe()
