import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import random

# Criar dados fictícios para treinamento do modelo
dados = {
    'idade': [random.randint(18, 80) for _ in range(200)],
    'peso': [random.uniform(50.0, 120.0) for _ in range(200)],
    'altura': [random.uniform(150.0, 200.0) for _ in range(200)],
    'sexo_bin': [random.randint(0, 1) for _ in range(200)],
    'doenca_idx': [random.randint(0, 4) for _ in range(200)],
    'dieta': [
        random.choice(['Maçã,Banana,Ovo cozido', 'Peito de frango,Arroz,Brócolis', 'Quinoa,Espinafre,Tomate',
                       'Salmão,Batata-doce,Abacate', 'Pão integral,Queijo,Leite', 'Maçã,Nozes,Iogurte natural',
                       'Peito de frango,Azeite,Espinafre', 'Salmão,Quinoa,Tomate', 'Banana,Batata-doce,Morangos',
                       'Arroz,Abacate,Amêndoas']) for _ in range(200)
    ]
}

# Converter para DataFrame
df = pd.DataFrame(dados)

# Separar features e target
X = df[['idade', 'peso', 'altura', 'sexo_bin', 'doenca_idx']]
y = df['dieta']

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo RandomForest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões e calcular a acurácia
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)
print(f'Acurácia do modelo: {acuracia:.2f}')

# Salvar o modelo treinado
with open('modelo_dieta.pkl', 'wb') as f:
    pickle.dump(modelo, f)

print("Modelo salvo como 'modelo_dieta.pkl'")