import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API a partir das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave da API foi carregada corretamente
if not openai.api_key:
    st.error("Erro: A chave da API OpenAI não foi encontrada. Verifique seu arquivo .env.")
else:
    st.title("Chatbot Union IT")

    # Inicializa o histórico de conversação na sessão
    if "historico" not in st.session_state:
        st.session_state["historico"] = []

    # Inicializa a variável de conteúdo do arquivo na sessão
    if "conteudo_arquivo" not in st.session_state:
        st.session_state["conteudo_arquivo"] = ""

    def obter_resposta(pergunta):
        try:
            # Cria a mensagem de sistema com o conteúdo do arquivo, se houver
            mensagens = []
            if st.session_state["conteudo_arquivo"]:
                mensagens.append({"role": "system", "content": f"Use as informações do seguinte arquivo para responder: {st.session_state['conteudo_arquivo']}"})
            mensagens.append({"role": "user", "content": pergunta})

            # Chama a API da OpenAI para obter a resposta
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ou "gpt-4" se você tiver acesso
                messages=mensagens,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return resposta.choices[0].message['content'].strip()
        except Exception as e:
            st.error(f"Erro ao obter resposta da API: {e}")
            return ""

    # Componente para upload de arquivo
    uploaded_file = st.file_uploader("Faça o upload de um arquivo", type=["txt", "csv"])

    if uploaded_file is not None:
        try:
            # Lê o conteúdo do arquivo e armazena na sessão
            file_contents = uploaded_file.read().decode("utf-8")
            st.session_state["conteudo_arquivo"] = file_contents
            st.text_area("Conteúdo do arquivo:", value=file_contents, height=200)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

    # Caixa de entrada do usuário
    entrada_usuario = st.text_input("Você:", key="entrada")

    # Botão para enviar a mensagem
    if st.button("Enviar"):
        if entrada_usuario:
            resposta = obter_resposta(entrada_usuario)
            if resposta:
                st.session_state.historico.append({"usuario": entrada_usuario, "bot": resposta})
                st.text_input("Você:", value="", key="entrada", on_change=None)  # Limpa a entrada do usuário

    # Mostrar histórico de conversas
    if st.session_state.historico:
        for chat in st.session_state.historico:
            st.write(f"**Você:** {chat['usuario']}")
            st.write(f"**ChatBot:** {chat['bot']}")
