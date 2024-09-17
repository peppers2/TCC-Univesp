import streamlit as st
import random
import streamlit_authenticator as stauth

# Configuração da página para layout wide
st.set_page_config(
    page_title="Previsão de Dieta Ideal",
    page_icon=":herb:",
    layout="wide"
)

# --- Configuração de autenticação ---
# Criação de credenciais com hash de senha
names = ['Pedro Siqueira']
usernames = ['pedro']
passwords = ['123']  # A senha deve ser hashada para maior segurança em um ambiente de produção

# Geração de hashes de senha (use isso para armazenar de maneira segura)
hashed_passwords = stauth.Hasher(passwords).generate()

# Definição de credenciais no formato esperado
credentials = {
    "usernames": {
        "pedro": {
            "name": "Pedro Siqueira",
            "password": hashed_passwords[0]  # Utilizando o hash gerado
        }
    }
}

# Autenticador (ajuste aqui, removendo o 'cookie_expiry_days')
authenticator = stauth.Authenticate(credentials, 'app_dieta', 'abcdef')

# Widget de login
location = 'main'  # Use 'main' ou 'sidebar' conforme necessário
name, authentication_status, username = authenticator.login('Login', location)

# Verifica o status de autenticação
if authentication_status:
    st.sidebar.success(f'Bem-vindo, {name}!')
elif authentication_status == False:
    st.error('Nome de usuário ou senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')

if authentication_status:
    # Função para calcular a TMB usando a fórmula de Harris-Benedict
    def calcular_tmb(sexo, peso, altura, idade):
        if sexo == 'Masculino':
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
        else:
            tmb = 447.0 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)
        return tmb

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
        'Ovo cozido': {'calorias': 78, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/cooked-egg.jpg'},
        'Peito de frango': {'calorias': 165, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/chicken-breast.jpg'},
        'Arroz': {'calorias': 200, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/cooked-rice.jpg'},
        'Brócolis': {'calorias': 55, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/broccoli.jpg'},
        'Queijo': {'calorias': 113, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/cheese.jpg'},
        'Pão integral': {'calorias': 80, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/whole-wheat-bread.jpg'},
        'Leite': {'calorias': 149, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/milk.jpg'},
        'Iogurte natural': {'calorias': 59, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/plain-yogurt.jpg'},
        'Abacate': {'calorias': 160, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/avocado.jpg'},
        'Salmão': {'calorias': 206, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/salmon.jpg'},
        'Batata-doce': {'calorias': 86, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/sweet-potato.jpg'},
        'Quinoa': {'calorias': 120, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/quinoa.jpg'},
        'Espinafre': {'calorias': 23, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/spinach.jpg'},
        'Tomate': {'calorias': 18, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/tomato.jpg'},
        'Nozes': {'calorias': 654, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/walnuts.jpg'},
        'Amêndoas': {'calorias': 579, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/almonds.jpg'},
        'Azeite': {'calorias': 884, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/olive-oil.jpg'},
        'Melancia': {'calorias': 30, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/watermelon.jpg'},
        'Morangos': {'calorias': 32, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/strawberries.jpg'}
    }

    # Função para sugerir refeições diárias
    def sugerir_refeicoes(calorias_maximas, num_refeicoes=4):
        alimentos = list(alimentos_calorias.items())
        random.shuffle(alimentos)  # Embaralha a lista para aleatoriedade
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

        # Entrada de dados do usuário
        sexo = st.selectbox('Sexo', ['Masculino', 'Feminino'])
        idade = st.number_input('Idade', min_value=0, max_value=120, value=25)
        peso = st.number_input('Peso (kg)', min_value=0.0, max_value=200.0, value=70.0)
        altura = st.number_input('Altura (cm)', min_value=0.0, max_value=250.0, value=170.0)
        nivel_atividade = st.selectbox('Nível de Atividade Física', ['Sedentário', 'Levemente ativo', 'Moderadamente ativo', 'Muito ativo', 'Extremamente ativo'])

        # Cálculo da TMB e do gasto calórico
        tmb = calcular_tmb(sexo, peso, altura, idade)
        gasto_calorico = calcular_gasto_calorico(tmb, nivel_atividade)

        # Armazenar o gasto calórico no estado da sessão
        st.session_state.gasto_calorico = gasto_calorico

       
