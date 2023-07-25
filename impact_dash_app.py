import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Dashboard de impacto Inovativa',
                   page_icon=':game_die:',
                   layout='wide')

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

df = pd.read_csv('Dados_Hub.csv')

# Arrumando alguns dados

# Lista de palavras a serem verificadas
palavras = ['crescimento', 'Operação', 'Validação']

# Defina a função de substituição


def substituir_palavra(frase):
    for palavra in palavras:
        if palavra in frase:
            return palavra
    return frase


# Aplica a substituição na coluna 'fase_apos_programa'
df['fase_apos_programa'] = df['fase_apos_programa'].apply(substituir_palavra)


# -------SIDEBAR----------------
# st.sidebar.image('inovativa.png', width=300)
st.sidebar.markdown(
    "<h1 style='text-align: center; color: white'> Selecione seus filtros:", unsafe_allow_html=True)


st.sidebar.markdown(
    "<h3 style='text-align: center; color: white'> localização", unsafe_allow_html=True)
localizacao = st.sidebar.multiselect(
    '',
    options=df["localizacao"].unique(),
    default=df["localizacao"].unique(),
)

st.sidebar.markdown(
    "<h3 style='text-align: center; color: white'> Gênero", unsafe_allow_html=True)

genero = st.sidebar.multiselect(
    ' ',
    options=df["genero"].unique(),
    default=df["genero"].unique()
)
st.sidebar.markdown(
    "<h3 style='text-align: center; color: white'> Ramo", unsafe_allow_html=True)
ramo = st.sidebar.multiselect(
    ' ',
    options=df["ramo"].unique(),
    default=df["ramo"].unique()
)
st.sidebar.markdown(
    "<h3 style='text-align: center; color: white'> Escolaridade", unsafe_allow_html=True)
escolaridade = st.sidebar.multiselect(
    ' ',
    options=df["escolaridade"].unique(),
    default=df["escolaridade"].unique()
)


df_selecttion = df.query(
    "localizacao == @localizacao & genero == @genero & ramo == @ramo & escolaridade == @escolaridade"
)


# -------MAIN----------------

st.markdown(" .<h1 style='text-align: center'>  Dashboard de impacto INOVATIVA :bar_chart: </h1>",
            unsafe_allow_html=True)


st.markdown('---')


# TOP KPI's

# numero total de participantes

total_participantes = df_selecttion['nome'].nunique()

# media de faturamento após o programa

media_faturamento = round(df_selecttion['variacao_faturamento'].mean()*100)

# total de empregos gerados apos o programa

total_empregos = df_selecttion['empregos_gerados'].sum()

# grafico de gauge com a variável satisfacao_metodologia


def calcular_media_categorias(df, coluna):
    df[coluna] = pd.Categorical(df[coluna])
    niveis_categorias = df[coluna].cat.categories
    media_valores = round((df[coluna].cat.codes + 3).mean(), 2)
    return media_valores


media_valores_rating = calcular_media_categorias(
    df_selecttion, 'satisfacao_metodologia')

media_valores_acelerar_negocio = ":star:" * \
    int(round(calcular_media_categorias(
        df_selecttion, df_selecttion.columns[9])))

star_rating = ":star:" * int(round(media_valores_rating, 0))

# contagem de conexoes feitas == sim

total_conexoes = df_selecttion['fez_conexoes'].value_counts()['Sim']

left_column, left_column2, midle_column, right_column, far_right, far_far_right = st.columns(
    6)

with far_far_right:
    st.subheader(f':people_hugging:{total_participantes}' '  Participantes')

with midle_column:
    st.subheader(f':office_worker:{total_empregos}' '  Novos empregos gerados')


with right_column:
    st.subheader(
        ':heavy_dollar_sign: Aumento médio de  'f'{media_faturamento}%' '  no faturamento')


with far_right:
    st.subheader(f':phone:{total_conexoes}'' novas conexões criadas')

with left_column:
    st.subheader('Satisfação com a metodologia:')
    st.subheader(f' {star_rating}')

with left_column2:
    st.subheader('Importância da participação:')
    st.subheader(f'{media_valores_acelerar_negocio}')

st.markdown('---')

# importancias
left_column, midle_column, right_column, far_right, far_far_right = st.columns(
    5)


# Importancia da participação grafico pizza


# grafico de barra com as variaveis de variação de faturamento e fez_conexoes

grafico_barra_fat = px.bar(df_selecttion,
                           x='fez_conexoes',
                           y='variacao_faturamento',
                           color='ramo',
                           color_discrete_sequence=px.colors.qualitative.Pastel,
                           template='plotly_white',
                           title='<b>Variação de faturamento x Fez conexões</b>'
                           )
# mudandno a posi;'ao da legenda
grafico_barra_fat.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

grafico_barra_fat.update_layout(
    xaxis_title='Fez conexões?',
    yaxis_title='Variação de faturamento (%)',
    legend_title='Ramo de atuação',
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='verdana',
        size=12,
        color='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))


# grafico de barra com a contagem de fase_apos_programa

grafico_barra_fase = px.bar(df_selecttion,
                            y='fase_apos_programa',
                            color_discrete_sequence=px.colors.qualitative.Pastel,
                            template='plotly_white',
                            title='<b>Fase após o programa</b>'
                            )
grafico_barra_fase.update_layout(
    xaxis_title='Contagem',
    yaxis_title='Fase após o programa',
    legend_title='Fase após o programa',
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='verdana',
        size=12,
        color='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))


# grafico empregos gerados por setor

grafico_empregos = px.bar(df_selecttion,
                          x='ramo',
                          y='empregos_gerados',
                          color='ramo',
                          color_discrete_sequence=px.colors.qualitative.Pastel,
                          template='plotly_white',
                          title='<b>Empregos gerados por setor</b>'
                          )
grafico_empregos.update_layout(
    xaxis_title='Setor',
    yaxis_title='Empregos gerados',
    legend_title='Setor',
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='verdana',
        size=12,
        color='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))


grafico_importancia = px.bar(df_selecttion,
                             x='localizacao',
                             y='variacao_faturamento',
                             color='ramo',
                             color_discrete_sequence=px.colors.qualitative.Pastel,
                             template='plotly_white',
                             title='<b>Variação do faturamento por localização</b>'
                             )
grafico_importancia.update_layout(
    xaxis_title='localização',
    yaxis_title='variação média do faturamento',
    legend_title='Setor',
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='verdana',
        size=12,
        color='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))


col0, col1, col3 = st.columns(3)

with col0:
    st.plotly_chart(grafico_importancia, use_container_width=False)
with col1:
    st.plotly_chart(grafico_barra_fat, use_container_width=False)
with col3:
    st.plotly_chart(grafico_empregos, use_container_width=False)


# st.dataframe(df_selecttion)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('---')
