import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Dashboard de impacto Inovativa',
                   page_icon=':game_die:',
                   layout='wide')

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

st.sidebar.header('Selecione seus filtros:')

localizacao = st.sidebar.multiselect(
    'Selecione a localização',
    options=df["localizacao"].unique(),
    default=df["localizacao"].unique()
)

genero = st.sidebar.multiselect(
    'Selecione o gênero dos participantes',
    options=df["genero"].unique(),
    default=df["genero"].unique()
)

ramo = st.sidebar.multiselect(
    'Selecione o ramo de atuação',
    options=df["ramo"].unique(),
    default=df["ramo"].unique()
)

escolaridade = st.sidebar.multiselect(
    'Selecione a escolaridade',
    options=df["escolaridade"].unique(),
    default=df["escolaridade"].unique()
)

df_selecttion = df.query(
    "localizacao == @localizacao & genero == @genero & ramo == @ramo"
)


# -------MAIN----------------


st.title(':bar_chart: Dashboard de impacto Inovativa')

st.markdown('##')
st.markdown('---')


# TOP KPI's

# numero total de participantes

total_participantes = df_selecttion['nome'].nunique()

# media de faturamento após o programa

media_faturamento = round(df_selecttion['variacao_faturamento'].mean()*100)

# total de empregos gerados apos o programa

total_empregos = df_selecttion['empregos_gerados'].sum()

# contagem de conexoes feitas == sim

total_conexoes = df_selecttion['fez_conexoes'].value_counts()['Sim']

left_column, midle_column, right_column, far_right = st.columns(4)

with left_column:
    st.subheader(f':people_hugging:{total_participantes}' '  participantes')

with midle_column:
    st.subheader( f':office_worker:{total_empregos}' '  Empregos gerados')


with right_column:
    st.subheader(':heavy_dollar_sign: Aumento médio de  'f'{media_faturamento} %' ' no faturamento')


with far_right:
    st.subheader( f':phone:{total_conexoes}'' novas conexões criadas')

st.markdown('---')

# grafico de barra com as variaveis de variação de faturamento e fez_conexoes

grafico_barra_fat = px.bar(df_selecttion,
                       x='fez_conexoes',
                       y='variacao_faturamento',
                       color='ramo',
                       color_discrete_sequence=px.colors.qualitative.Pastel,
                       template='plotly_white',
                       title='<b>Variação de faturamento x Fez conexões</b>'
                       )
grafico_barra_fat.update_layout(
    xaxis_title='Fez conexões?',
    yaxis_title='Variação de faturamento (%)',
    legend_title='Ramo de atuação',
    title_x=0.5,
    plot_bgcolor='white',
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='Arial',
        size=12,
        color='black'
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
    plot_bgcolor='white',
    yaxis=(dict(showgrid=False)),
    font=dict(
        family='Arial',
        size=12,
        color='black'
    ))

# grafico de gauge com a variável satisfacao_metodologia

                       


main_left_column, main_right_column = st.columns(2)


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_barra_fat, use_container_width=False)
with col2:
    st.plotly_chart(grafico_barra_fase, use_container_width=False)


st.dataframe(df_selecttion)
