import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("API Key for OpenAI is missing. Please check your .env file.")
    st.stop()

openai.api_key = OPENAI_API_KEY

st.title("Assistente Financeiro union it")

# Inicializar o histórico de chat na sessão
if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# Inicializar a lista de descrições dos gráficos
if 'graficos_descricao' not in st.session_state:
    st.session_state['graficos_descricao'] = []

# Função para extrair o nome da empresa e o ramo a partir do nome do arquivo
def obter_nome_empresa_e_ramo(nome_arquivo):
    nome_arquivo_sem_extensao = os.path.splitext(os.path.basename(nome_arquivo))[0]
    partes = nome_arquivo_sem_extensao.split('_')
    if len(partes) >= 2:
        nome_empresa = partes[0]
        ramo = '_'.join(partes[1:])
    else:
        nome_empresa = partes[0]
        ramo = "Desconhecido"
    return nome_empresa, ramo

# Função principal do assistente financeiro
def financial_assistant(pergunta_usuario, resumo_dados, nome_empresa, ramo, descricoes_graficos):
    # Construir a mensagem do sistema com o contexto necessário
    system_message = f"""
    Você é um assistente financeiro especializado em análise de empresas. Utilize as seguintes informações de contexto para responder às perguntas dos usuários.

    **Contexto da Empresa**:
    A empresa que você vai analisar é {nome_empresa}, atuando no ramo de {ramo}.

    **Resumo dos Dados Financeiros**:
    {resumo_dados}

    **Análises Realizadas**:
    {descricoes_graficos}

    Baseie suas respostas nos dados e análises fornecidos e, se possível, forneça sugestões que possam agregar valor à empresa. Agora, responda à pergunta do usuário de forma clara e concisa.
    """

    # Criar a conversa com as mensagens
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": pergunta_usuario}
    ]

    # Obter a resposta do modelo
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Utilize o modelo disponível para você
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        resposta_assistente = response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Erro ao obter resposta do modelo: {e}")
        resposta_assistente = "Desculpe, ocorreu um erro ao processar sua pergunta."

    # Salvar o histórico da conversa
    st.session_state.historico.append({"usuario": pergunta_usuario, "bot": resposta_assistente})

    # Exibir a resposta
    st.write(f"**Assistente:** {resposta_assistente}")

# Ler os dados pré-definidos do arquivo CSV
caminho_arquivo = r'data/sheet_1.csv'  # Certifique-se de que o caminho está correto
try:
    # Especificar o encoding correto e tratar separadores
    df = pd.read_csv(caminho_arquivo, header=0, encoding='iso-8859-1', sep=';')

    # Renomear colunas para remover espaços e caracteres especiais
    df.columns = df.columns.str.strip().str.replace('�', 'ã').str.replace(' ', '_')

    # Exibir as primeiras linhas do DataFrame
    st.session_state['data'] = df
    st.write("Conteúdo do DataFrame (as primeiras linhas):")
    st.write(df.head())

    # Obter o nome da empresa e o ramo a partir do nome do arquivo
    nome_empresa, ramo = obter_nome_empresa_e_ramo(caminho_arquivo)

    # Gerar um resumo dos dados financeiros
    resumo_estatistico = df.describe(include='all').to_string()
    resumo_personalizado = f"""
    Total de registros: {len(df)}
    Colunas disponíveis: {', '.join(df.columns)}
    """
    # Combinar os resumos conforme necessário
    resumo_dados = resumo_personalizado + "\n" + resumo_estatistico

    # Adicionar análises prévias interativas
    st.sidebar.header("Análises Prévias")

    if st.sidebar.checkbox("Mostrar Resumo Estatístico"):
        st.subheader("Resumo Estatístico")
        st.write(df.describe(include='all'))
        # Adicionar descrição ao contexto
        descricao = "O usuário visualizou o resumo estatístico dos dados."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Gráfico de Ocorrências ao Longo do Tempo"):
        st.subheader("Ocorrências ao Longo do Tempo")
        # Criar uma coluna de data
        df['Data'] = pd.to_datetime(df['Dia'].astype(str) + '/' + df['Mês'] + '/' + df['Ano'].astype(str), errors='coerce', dayfirst=True)
        df_time = df.dropna(subset=['Data'])
        ocorrencias_por_data = df_time.groupby('Data').size().reset_index(name='Total de Ocorrências')
        fig = px.line(ocorrencias_por_data, x='Data', y='Total de Ocorrências', title='Ocorrências ao Longo do Tempo')
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Gráfico de ocorrências ao longo do tempo foi visualizado, mostrando como as ocorrências variam em diferentes datas."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Gráfico de Ocorrências por Mês"):
        st.subheader("Total de Ocorrências por Mês")
        # Remover valores ausentes na coluna 'Mês'
        df_mes = df.dropna(subset=['Mês'])
        # Contar o número de ocorrências por mês
        contagem_por_mes = df_mes.groupby('Mês').size().reset_index(name='Total de Ocorrências por mês')
        # Ordenar os meses corretamente
        meses_ordem = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        contagem_por_mes['Mês'] = pd.Categorical(contagem_por_mes['Mês'], categories=meses_ordem, ordered=True)
        contagem_por_mes = contagem_por_mes.sort_values('Mês')
        # Criar o gráfico de barras
        fig = px.bar(contagem_por_mes, x='Mês', y='Total de Ocorrências por mês', text='Total de Ocorrências por mês')
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Gráfico de ocorrências por mês foi visualizado, mostrando quais meses têm mais ocorrências."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Gráfico de Ocorrências por Ano"):
        st.subheader("Total de Ocorrências por Ano")
        # Remover valores ausentes na coluna 'Ano'
        df_ano = df.dropna(subset=['Ano'])
        # Convertendo a coluna 'Ano' para int
        df_ano['Ano'] = df_ano['Ano'].astype(int)
        # Contar o número de ocorrências por ano
        contagem_por_ano = df_ano.groupby('Ano').size().reset_index(name='Total de Ocorrências')
        # Criar o gráfico de barras
        fig = px.bar(contagem_por_ano, x='Ano', y='Total de Ocorrências', text='Total de Ocorrências')
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Gráfico de ocorrências por ano foi visualizado, indicando tendências ao longo dos anos."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Gráfico de Ocorrências por Dia da Semana"):
        st.subheader("Distribuição de Ocorrências por Dia da Semana")
        # Remover valores ausentes na coluna 'Dia_semana'
        df_dia = df.dropna(subset=['Dia_semana'])
        # Contar o número de ocorrências por dia da semana
        ocorrencias_por_dia = df_dia['Dia_semana'].value_counts()
        # Ordenar os dias da semana corretamente
        dias_ordem = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
        ocorrencias_por_dia = ocorrencias_por_dia.reindex(dias_ordem)
        # Criar o gráfico de barras
        fig = px.bar(ocorrencias_por_dia.reset_index(), x='index', y='Dia_semana', text='Dia_semana',
                     labels={'index': 'Dia da Semana', 'Dia_semana': 'Número de Ocorrências'})
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Gráfico de ocorrências por dia da semana foi visualizado, mostrando a distribuição ao longo da semana."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Ocorrências por Tipo"):
        st.subheader("Ocorrências por Tipo (NATDESCRIC)")
        df_tipo = df.dropna(subset=['NATDESCRIC'])
        ocorrencias_por_tipo = df_tipo['NATDESCRIC'].value_counts().reset_index()
        ocorrencias_por_tipo.columns = ['Tipo de Ocorrência', 'Total']
        fig = px.bar(ocorrencias_por_tipo, x='Tipo de Ocorrência', y='Total', text='Total')
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Gráfico de ocorrências por tipo foi visualizado, destacando os tipos mais frequentes."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

    if st.sidebar.checkbox("Mostrar Duração dos Eventos"):
        st.subheader("Análise de Duração dos Eventos")
        # Converter colunas de hora para datetime
        df['COMHORBLOQ'] = pd.to_datetime(df['COMHORBLOQ'], format='%H:%M', errors='coerce')
        df['COMHORTERM'] = pd.to_datetime(df['COMHORTERM'], format='%H:%M', errors='coerce')
        # Calcular a duração
        df['Duração'] = (df['COMHORTERM'] - df['COMHORBLOQ']).dt.total_seconds() / 60  # Em minutos
        df_duracao = df.dropna(subset=['Duração'])
        fig = px.histogram(df_duracao, x='Duração', nbins=50, title='Distribuição da Duração dos Eventos')
        st.plotly_chart(fig)
        # Adicionar descrição ao contexto
        descricao = "Análise da duração dos eventos foi realizada, mostrando a distribuição das durações."
        if descricao not in st.session_state['graficos_descricao']:
            st.session_state['graficos_descricao'].append(descricao)

except Exception as e:
    st.error(f"Erro ao ler o arquivo CSV: {e}")
    resumo_dados = "Dados financeiros não disponíveis."
    nome_empresa = "Desconhecido"
    ramo = "Desconhecido"

# Concatenar as descrições dos gráficos para o contexto
descricoes_graficos = "\n".join(st.session_state['graficos_descricao'])

# Campo de entrada para a pergunta do usuário
pergunta_usuario = st.text_input("Faça sua pergunta ao assistente financeiro:")

if st.button("Enviar"):
    if pergunta_usuario:
        with st.spinner('Gerando resposta...'):
            financial_assistant(pergunta_usuario, resumo_dados, nome_empresa, ramo, descricoes_graficos)

# Mostrar histórico de conversas
if st.session_state.historico:
    st.write("---")
    st.write("### Histórico de Conversa")
    for chat in st.session_state.historico:
        st.write(f"**Você:** {chat['usuario']}")
        st.write(f"**Assistente:** {chat['bot']}")
