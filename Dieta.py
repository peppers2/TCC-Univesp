import streamlit as st
import random
import pandas as pd
import pickle

# Configuração da página para layout wide
st.set_page_config(
    page_title="Previsão de Dieta Ideal",
    page_icon=":herb:",
    layout="wide"
)

# Lista de condições de saúde para a sugestão de dieta
opcoes_doencas = ['Diabetes', 'Hipertensão', 'Colesterol Alto', 'Obesidade', 'Nenhuma']

# Definição dos fatores de atividade física
fatores_atividade = {
    'Sedentário': 1.2,
    'Levemente ativo': 1.375,
    'Moderadamente ativo': 1.55,
    'Muito ativo': 1.725,
    'Extremamente ativo': 1.9
}

# Função para calcular TMB
def calcular_tmb(sexo, peso, altura, idade):
    if sexo == 'Masculino':
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

# Função para filtrar alimentos com base na condição de saúde
def filtrar_alimentos_por_condicao(condicao, alimentos):
    restricoes = {
        'Diabetes': ['Banana', 'Arroz', 'Azeite'],
        'Hipertensão': ['Queijo', 'Salmão', 'Nozes'],
        'Colesterol Alto': ['Queijo', 'Ovo cozido', 'Amêndoas'],
        'Obesidade': ['Arroz', 'Queijo', 'Azeite'],
        'Nenhuma': []
    }
    alimentos_filtrados = {k: v for k, v in alimentos.items() if k not in restricoes[condicao]}
    return alimentos_filtrados

# Função para sugerir refeições de maneira variada
def sugerir_refeicoes(alimentos, calorias_por_refeicao):
    alimentos_disponiveis = list(alimentos.keys())
    refeicoes = [[] for _ in range(4)]
    calorias_refeicoes = [0] * 4

    for i in range(4):
        random.shuffle(alimentos_disponiveis)  # Embaralha a lista a cada nova refeição para maior variedade
        while calorias_refeicoes[i] < calorias_por_refeicao * 0.9:
            if not alimentos_disponiveis:  # Reinicia a lista de alimentos se todos já tiverem sido usados
                alimentos_disponiveis = list(alimentos.keys())
                random.shuffle(alimentos_disponiveis)
            alimento = alimentos_disponiveis.pop(0)
            calorias_alimento = alimentos[alimento]['calorias']
            if calorias_refeicoes[i] + calorias_alimento <= calorias_por_refeicao:
                refeicoes[i].append(alimento)
                calorias_refeicoes[i] += calorias_alimento

    return refeicoes, calorias_refeicoes

# Carregar modelo de Machine Learning (RandomForest)
try:
    with open('modelo_dieta.pkl', 'rb') as f:
        modelo_dieta = pickle.load(f)
except FileNotFoundError:
    st.error("Modelo de Machine Learning não encontrado. Por favor, treine e forneça o modelo adequado.")
    st.stop()

# Dados dos alimentos com valores nutricionais adicionais e imagens
alimentos_calorias = {
    'Maçã': {'calorias': 95, 'proteinas': 0.5, 'carboidratos': 25, 'gorduras': 0.3, 'imagem': 'https://e7.pngegg.com/pngimages/399/447/png-clipart-red-apple-illustration-juice-apple-fruit-graphy-red-apple-natural-foods-food-thumbnail.png'},
    'Banana': {'calorias': 105, 'proteinas': 1.3, 'carboidratos': 27, 'gorduras': 0.3, 'imagem': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Bananas_%28Alabama_Extension%29.jpg/1008px-Bananas_%28Alabama_Extension%29.jpg'},
    'Ovo cozido': {'calorias': 78, 'proteinas': 6.3, 'carboidratos': 1.1, 'gorduras': 5.3, 'imagem': 'https://static.itdg.com.br/images/auto-auto/4fcb5ddef21a1861d9680063cabe8f10/ovo-cozido.jpg'},
    'Peito de frango': {'calorias': 165, 'proteinas': 31, 'carboidratos': 0, 'gorduras': 3.6, 'imagem': 'https://www.svicente.com.br/on/demandware.static/-/Sites-storefront-catalog-sv/default/dw96334b03/Produtos/20311-0000000002031-peito%20de%20frango%20com%20pele%20e%20osso%20bandeja-acougue-1.jpg'},
    'Arroz integral': {'calorias': 215, 'proteinas': 5, 'carboidratos': 45, 'gorduras': 1.8, 'imagem': 'https://image.tuasaude.com/media/article/jd/ms/7-boas-razoes-para-comer-brocolis_14108_l.jpg'},
    'Brócolis': {'calorias': 55, 'proteinas': 3.7, 'carboidratos': 11, 'gorduras': 0.6, 'imagem': 'https://image.tuasaude.com/media/article/jd/ms/7-boas-razoes-para-comer-brocolis_14108_l.jpg'},
    'Queijo cottage': {'calorias': 98, 'proteinas': 11, 'carboidratos': 3, 'gorduras': 4.3, 'imagem': 'https://cdn.panelinha.com.br/receita/958014000000-Queijo-cottage.jpg'},
    'Pão integral': {'calorias': 80, 'proteinas': 4, 'carboidratos': 14, 'gorduras': 1, 'imagem': 'https://conteudo.imguol.com.br/c/entretenimento/24/2016/12/06/pao-integral-fatia-de-pao-integral-1481039924167_v2_1170x540.jpg'},
    'Leite desnatado': {'calorias': 83, 'proteinas': 8, 'carboidratos': 12, 'gorduras': 0.2, 'imagem': 'https://s3.static.brasilescola.uol.com.br/be/2022/06/leite.jpg'},
    'Iogurte natural': {'calorias': 59, 'proteinas': 10, 'carboidratos': 4, 'gorduras': 0.5, 'imagem': 'https://cdn.irmaospatrocinio.com.br/img/p/1/7/4/0/6/8/174068-large_default.jpg'}
}

# Layout do Streamlit
st.sidebar.title('Menu')
opcao = st.sidebar.radio('Escolha uma opção', ['Calculadora de Gasto Calórico', 'Sugestão de Dieta com Machine Learning'])
st.sidebar.write("")
st.sidebar.image('Logo.png', use_column_width=True)

if opcao == 'Calculadora de Gasto Calórico':
    st.title('Calculadora de Gasto Calórico Diário')
    
    sexo = st.selectbox('Sexo', ['Masculino', 'Feminino'])
    idade = st.number_input('Idade', min_value=0, max_value=120, value=25)
    peso = st.number_input('Peso (kg)', min_value=0.0, max_value=200.0, value=70.0)
    altura = st.number_input('Altura (cm)', min_value=0.0, max_value=250.0, value=170.0)
    nivel_atividade = st.selectbox('Nível de Atividade Física', ['Sedentário', 'Levemente ativo', 'Moderadamente ativo', 'Muito ativo', 'Extremamente ativo'])

    tmb = calcular_tmb(sexo, peso, altura, idade)
    gasto_calorico = tmb * fatores_atividade[nivel_atividade]

    st.write(f"Sua Taxa Metabólica Basal (TMB) é: {tmb:.2f} calorias por dia.")
    st.write(f"Seu gasto calórico diário, considerando o nível de atividade física, é: {gasto_calorico:.2f} calorias por dia.")

elif opcao == 'Sugestão de Dieta com Machine Learning':
    st.title('Sugestão de Dieta com Machine Learning')
    
    # Inputs do usuário para o modelo
    st.subheader('Informe seus dados pessoais:')
    sexo = st.selectbox('Sexo', ['Masculino', 'Feminino'])
    idade = st.number_input('Idade', min_value=0, max_value=120, value=25)
    peso = st.number_input('Peso (kg)', min_value=0.0, max_value=200.0, value=70.0)
    altura = st.number_input('Altura (cm)', min_value=0.0, max_value=250.0, value=170.0)
    condicao_saude = st.selectbox('Alguma condição de saúde?', opcoes_doencas)
    nivel_atividade = st.selectbox('Nível de Atividade Física', ['Sedentário', 'Levemente ativo', 'Moderadamente ativo', 'Muito ativo', 'Extremamente ativo'])
    
    # Calcular calorias e sugerir refeições
    tmb = calcular_tmb(sexo, peso, altura, idade)
    calorias_por_refeicao = (tmb * fatores_atividade[nivel_atividade]) / 4
    alimentos_filtrados = filtrar_alimentos_por_condicao(condicao_saude, alimentos_calorias)
    refeicoes, calorias_refeicoes = sugerir_refeicoes(alimentos_filtrados, calorias_por_refeicao)
    
    # Exibir as refeições sugeridas com imagens e detalhes
    for i, refeicao in enumerate(refeicoes):
        st.subheader(f'Refeição {i + 1}')
        if refeicao:
            colunas = st.columns(len(refeicao))
            for j, alimento in enumerate(refeicao):
                with colunas[j]:
                    st.image(alimentos_calorias[alimento]['imagem'], width=100)
                    st.write(f"{alimento} - Calorias: {alimentos_calorias[alimento]['calorias']}")
        st.write(f"Calorias totais da refeição: {calorias_refeicoes[i]} cal")
    
    total_calorias = sum(calorias_refeicoes)
    st.write(f"**Total de calorias sugeridas: {total_calorias:.2f} calorias**")
