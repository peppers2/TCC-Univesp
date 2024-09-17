import streamlit as st
import random

# Configuração da página para layout wide
st.set_page_config(
    page_title="Previsão de Dieta Ideal",
    page_icon=":herb:",
    layout="wide"
)

# Função para calcular a TMB usando a fórmula de Harris-Benedict
def calcular_tmb(sexo, peso, altura, idade):
    if sexo == 'Masculino':
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        return 447.0 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

# Função para calcular o gasto calórico diário
def calcular_gasto_calorico(tmb, nivel_atividade):
    fatores_atividade = {
        'Sedentário': 1.2,
        'Levemente ativo': 1.375,
        'Moderadamente ativo': 1.55,
        'Muito ativo': 1.725,
        'Extremamente ativo': 1.9
    }
    return tmb * fatores_atividade[nivel_atividade]

# Lista de alimentos, suas calorias e imagens
alimentos_calorias = {
    'Maçã': {'calorias': 95, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/red-apple.jpg'},
    'Banana': {'calorias': 105, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/banana.jpg'},
    # Outros alimentos...
}

# Função para sugerir refeições diárias
def sugerir_refeicoes(calorias_maximas, num_refeicoes=4):
    alimentos = list(alimentos_calorias.items())
    random.shuffle(alimentos)
    refeicoes = [[] for _ in range(num_refeicoes)]
    calorias_refeicoes = [0] * num_refeicoes

    for alimento, info in alimentos:
        for i in range(num_refeicoes):
            if calorias_refeicoes[i] + info['calorias'] <= calorias_maximas:
                refeicoes[i].append((alimento, info['calorias'], info['imagem']))
                calorias_refeicoes[i] += info['calorias']
                break

    return refeicoes, calorias_refeicoes

# Layout do Streamlit
st.sidebar.title('Menu')
opcao = st.sidebar.radio('Escolha uma opção', ['Calculadora de Gasto Calórico', 'Seleção de Alimentos', 'Sugestão de Dieta', 'Sugestão de Refeições'])

if opcao == 'Calculadora de Gasto Calórico':
    st.title('Calculadora de Gasto Calórico Diário')
    sexo = st.selectbox('Sexo', ['Masculino', 'Feminino'])
    idade = st.number_input('Idade', min_value=0, max_value=120, value=0)
    peso = st.number_input('Peso (kg)', min_value=0.0, max_value=200.0, value=0)
    altura = st.number_input('Altura (cm)', min_value=0.0, max_value=250.0, value=0)
    nivel_atividade = st.selectbox('Nível de Atividade Física', ['Sedentário', 'Levemente ativo', 'Moderadamente ativo', 'Muito ativo', 'Extremamente ativo'])

    tmb = calcular_tmb(sexo, peso, altura, idade)
    gasto_calorico = calcular_gasto_calorico(tmb, nivel_atividade)
    st.session_state.gasto_calorico = gasto_calorico

    st.write(f"Sua Taxa Metabólica Basal (TMB) é: {tmb:.2f} calorias/dia")
    st.write(f"Seu gasto calórico diário estimado é: {gasto_calorico:.2f} calorias/dia")

elif opcao == 'Seleção de Alimentos':
    st.title('Seleção de Alimentos')
    alimentos_selecionados = st.multiselect('Escolha seus alimentos', list(alimentos_calorias.keys()))
    calorias_consumidas = sum(alimentos_calorias[alimento]['calorias'] for alimento in alimentos_selecionados)
    st.write(f"Calorias totais consumidas: {calorias_consumidas:.2f} kcal")

    if 'gasto_calorico' in st.session_state:
        calorias_restantes = st.session_state.gasto_calorico - calorias_consumidas
        st.write(f"Calorias restantes para atingir sua meta diária: {calorias_restantes:.2f} kcal")

elif opcao == 'Sugestão de Dieta':
    st.title('Sugestão de Dieta Baseada em Calorias')
    calorias_maximas = st.number_input('Calorias máximas para a dieta (ex: 2000)', min_value=1000, max_value=5000, value=2000)
    refeicoes, calorias_refeicoes = sugerir_refeicoes(calorias_maximas)

    st.header('Sugestão de Refeições')
    for i, (refeicao, calorias) in enumerate(zip(refeicoes, calorias_refeicoes)):
        st.subheader(f'Refeição {i + 1} - Total de calorias: {calorias:.2f}')
        for alimento, caloria, imagem in refeicao:
            st.write(f"- {alimento} ({caloria} kcal)")
            st.image(imagem, width=100)

    total_calorias = sum(calorias_refeicoes)
    st.write(f"**Total de calorias propostas:** {total_calorias:.2f} kcal")

elif opcao == 'Sugestão de Refeições':
    st.title('Sugestão de Refeições Aleatórias')
    calorias_maximas = st.number_input('Calorias máximas por refeição', min_value=100, max_value=1500, value=600)
    refeicoes, calorias_refeicoes = sugerir_refeicoes(calorias_maximas)

    st.header('Sugestões de Refeições')
    for i, (refeicao, calorias) in enumerate(zip(refeicoes, calorias_refeicoes)):
        st.subheader(f'Refeição {i + 1} - Total de calorias: {calorias:.2f}')
        for alimento, caloria, imagem in refeicao:
            st.write(f"- {alimento} ({caloria} kcal)")
            st.image(imagem, width=100)


    total_calorias = sum(calorias_refeicoes)
    st.write(f"**Total de calorias propostas:** {total_calorias:.2f} kcal")
