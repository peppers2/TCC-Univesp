import streamlit as st
import random
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página para layout wide
st.set_page_config(
    page_title="Previsão de Dieta Ideal",
    page_icon=":herb:",
    layout="wide"
)

# Funções para cálculos
def calcular_tmb(sexo, peso, altura, idade):
    if sexo == 'Masculino':
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        tmb = 447.0 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)
    return tmb

def calcular_gasto_calorico(tmb, nivel_atividade):
    fatores_atividade = {
        'Sedentário': 1.2,
        'Levemente ativo': 1.375,
        'Moderadamente ativo': 1.55,
        'Muito ativo': 1.725,
        'Extremamente ativo': 1.9
    }
    return tmb * fatores_atividade[nivel_atividade]

# Dados dos alimentos
alimentos_calorias = {
    'Maçã': {'calorias': 95, 'imagem': 'https://e7.pngegg.com/pngimages/399/447/png-clipart-red-apple-illustration-juice-apple-fruit-graphy-red-apple-natural-foods-food-thumbnail.png'},
    'Banana': {'calorias': 105, 'imagem': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Bananas_%28Alabama_Extension%29.jpg/1008px-Bananas_%28Alabama_Extension%29.jpg'},
    'Ovo cozido': {'calorias': 78, 'imagem': 'https://static.itdg.com.br/images/auto-auto/4fcb5ddef21a1861d9680063cabe8f10/ovo-cozido.jpg'},
    'Peito de frango': {'calorias': 165, 'imagem': 'https://www.svicente.com.br/on/demandware.static/-/Sites-storefront-catalog-sv/default/dw96334b03/Produtos/20311-0000000002031-peito%20de%20frango%20com%20pele%20e%20osso%20bandeja-acougue-1.jpg'},
    'Arroz': {'calorias': 200, 'imagem': 'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/7c44045d2e8577819cb76b2b404902dd.jpg'},
    'Brócolis': {'calorias': 55, 'imagem': 'https://image.tuasaude.com/media/article/jd/ms/7-boas-razoes-para-comer-brocolis_14108_l.jpg'},
    'Queijo': {'calorias': 113, 'imagem': 'https://img.fazendinha.me/production/produtor/528/produtos/4558/laticinios-moedense-quejo-minas-frescal-moedense-1kg-1660131815.jpg'},
    'Pão integral': {'calorias': 80, 'imagem': 'https://conteudo.imguol.com.br/c/entretenimento/24/2016/12/06/pao-integral-fatia-de-pao-integral-1481039924167_v2_1170x540.jpg'},
    'Leite': {'calorias': 149, 'imagem': 'https://s3.static.brasilescola.uol.com.br/be/2022/06/leite.jpg'},
    'Iogurte natural': {'calorias': 59, 'imagem': 'https://cdn.irmaospatrocinio.com.br/img/p/1/7/4/0/6/8/174068-large_default.jpg'},
    'Abacate': {'calorias': 160, 'imagem': 'https://saude.abril.com.br/wp-content/uploads/2017/07/abacate3.jpg?quality=85&strip=info&w=680&h=453&crop=1'},
    'Salmão': {'calorias': 206, 'imagem': 'https://www.publicdomainpictures.net/pictures/30000/velka/salmon.jpg'},
    'Batata-doce': {'calorias': 86, 'imagem': 'https://go-organic.com.au/wp-content/uploads/2022/01/Sweet-potato.jpg'},
    'Quinoa': {'calorias': 120, 'imagem': 'https://alternativedish.com/wp-content/uploads/2023/07/popped-quinoa.jpg'},
    'Espinafre': {'calorias': 23, 'imagem': 'https://www.proativaalimentos.com.br/image/cachewebp/catalog/img_prod/espinafre[1]-500x500.webp'},
    'Tomate': {'calorias': 18, 'imagem': 'https://webrun.com.br/wp-content/uploads/2024/02/AdobeStock_69282769.jpeg'},
    'Nozes': {'calorias': 654, 'imagem': 'https://livup-cms.imgix.net/nozes_4981e4117e.jpg'},
    'Amêndoas': {'calorias': 579, 'imagem': 'https://seivanutri.com.br/wp-content/uploads/2020/06/amendoa-defumanda-min.jpg'},
    'Azeite': {'calorias': 884, 'imagem': 'https://diawine.agilecdn.com.br/4189_1.jpg?v=82-845148806'},
    'Melancia': {'calorias': 30, 'imagem': 'https://fly.metroimg.com/upload/q_85,w_700/https://uploads.metroimg.com/wp-content/uploads/2024/06/27152419/melancia-4.jpg'},
    'Morangos': {'calorias': 32, 'imagem': 'https://media.istockphoto.com/id/1412854156/pt/foto/strawberries-isolated-strawberry-whole-and-a-half-on-white-background-strawberry-slice-with.jpg?s=612x612&w=0&k=20&c=qjoZ9imnXieGFQapcmjFvTRgHr-noWSGjFwqfMcj-nw='}
}

def sugerir_refeicoes(calorias_maximas, num_refeicoes=4):
    alimentos = list(alimentos_calorias.items())
    random.shuffle(alimentos)
    refeicoes = [[] for _ in range(num_refeicoes)]
    calorias_refeicoes = [0] * num_refeicoes
    alimentos_utilizados = set()

    for alimento, info in alimentos:
        if alimento in alimentos_utilizados:
            continue

        alocado = False
        for i in range(num_refeicoes):
            if calorias_refeicoes[i] + info['calorias'] <= calorias_maximas:
                refeicoes[i].append((alimento, info['calorias'], info['imagem']))
                calorias_refeicoes[i] += info['calorias']
                alimentos_utilizados.add(alimento)
                alocado = True
                break

        if not alocado:
            break

    return refeicoes, calorias_refeicoes

# Layout do Streamlit
st.sidebar.title('Menu')
opcao = st.sidebar.radio('Escolha uma opção', ['Calculadora de Gasto Calórico', 'Seleção de Alimentos', 'Sugestão de Dieta', 'Sugestão de Refeições'])
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
    gasto_calorico = calcular_gasto_calorico(tmb, nivel_atividade)

    st.session_state.gasto_calorico = gasto_calorico

    st.write(f"Sua Taxa Metabólica Basal (TMB) é: {tmb:.2f} calorias por dia.")
    st.write(f"Seu gasto calórico diário, considerando o nível de atividade física, é: {gasto_calorico:.2f} calorias por dia.")

elif opcao == 'Seleção de Alimentos':
    st.title('Seleção de Alimentos')
    st.header('Escolha os alimentos desejados para a dieta')

    st.image('https://www.hormel.com/var/hormel/storage/images/hormel/products/canadian_bacon_pizza/bacon_pizza-3693/3629-1-eng-US/bacon_pizza.jpg', use_column_width=True)

    alimento_selecionado = st.selectbox('Escolha um alimento', list(alimentos_calorias.keys()))
    if alimento_selecionado:
        info_alimento = alimentos_calorias[alimento_selecionado]
        st.write(f'**{alimento_selecionado}**')
        st.write(f'Calorias: {info_alimento["calorias"]} kcal')
        st.image(info_alimento['imagem'], use_column_width=True)

elif opcao == 'Sugestão de Dieta':
    st.title('Sugestão de Dieta Ideal')
    
    calorias_maximas = st.number_input('Calorias máximas por refeição', min_value=100, max_value=2000, value=500)
    num_refeicoes = st.number_input('Número de refeições por dia', min_value=1, max_value=10, value=4)
    
    if st.button('Gerar Sugestão'):
        refeicoes, calorias_refeicoes = sugerir_refeicoes(calorias_maximas, num_refeicoes)
        
        for i, refeicao in enumerate(refeicoes):
            st.subheader(f'Refeição {i+1} - {calorias_refeicoes[i]:.2f} kcal')
            for alimento, calorias, imagem in refeicao:
                st.write(f'**{alimento}**: {calorias} kcal')
                st.image(imagem, use_column_width=True)

elif opcao == 'Sugestão de Refeições':
    st.title('Sugestão de Refeições e Análise Nutricional')
    
    calorias_maximas = st.number_input('Calorias máximas por refeição', min_value=100, max_value=2000, value=500)
    num_refeicoes = st.number_input('Número de refeições por dia', min_value=1, max_value=10, value=4)

    if st.button('Gerar Sugestão'):
        refeicoes, calorias_refeicoes = sugerir_refeicoes(calorias_maximas, num_refeicoes)
        
        for i, refeicao in enumerate(refeicoes):
            st.subheader(f'Refeição {i+1} - {calorias_refeicoes[i]:.2f} kcal')
            for alimento, calorias, imagem in refeicao:
                st.write(f'**{alimento}**: {calorias} kcal')
                st.image(imagem, use_column_width=True)

        # Gráfico de boxplot das calorias das refeições
        st.subheader('Distribuição Calórica das Refeições')
        fig_boxplot = go.Figure()
        fig_boxplot.add_trace(go.Box(
            y=calorias_refeicoes,
            name='Calorias das Refeições',
            marker_color='rgba(219, 64, 82, 0.6)'
        ))
        fig_boxplot.update_layout(title='Boxplot das Calorias das Refeições', yaxis_title='Calorias')
        st.plotly_chart(fig_boxplot)

        # Gráfico de gasto metabólico versus consumo energético
        st.subheader('Gasto Metabólico vs Consumo Energético Diário')
        horas = ['6h', '8h', '10h', '12h', '14h', '16h', '18h', '20h', '22h']
        gasto_metabolico = [0.1 * gasto_calorico * (i + 1) for i in range(len(horas))]
        consumo_energetico = [gasto_calorico * (i + 1) / len(horas) for i in range(len(horas))]

        df = pd.DataFrame({
            'Horas': horas,
            'Gasto Metabólico (kcal)': gasto_metabolico,
            'Consumo Energético (kcal)': consumo_energetico
        })

        fig_gasto = px.line(df, x='Horas', y=df.columns[1:], title='Gasto Metabólico e Consumo Energético ao Longo do Dia')
        st.plotly_chart(fig_gasto)
