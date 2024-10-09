import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API a partir das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Chatbot Union IT")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

def obter_resposta(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Ou "gpt-4" se você tiver acesso
        messages=[
            {"role": "user", "content": pergunta},
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return resposta.choices[0].message['content'].strip()

# Componente para upload de arquivo
uploaded_file = st.file_uploader("Faça o upload de um arquivo", type=["txt", "csv"])

if uploaded_file is not None:
    # Lê o conteúdo do arquivo
    file_contents = uploaded_file.read().decode("utf-8")
    st.text_area("Conteúdo do arquivo:", value=file_contents, height=200)

entrada_usuario = st.text_input("Você:", key="entrada")

if st.button("Enviar"):
    if entrada_usuario:
        resposta = obter_resposta(entrada_usuario)
        st.session_state.historico.append({"usuario": entrada_usuario, "bot": resposta})

# Mostrar histórico de conversas
if st.session_state.historico:
    for chat in st.session_state.historico:
        st.write(f"**Você:** {chat['usuario']}")
        st.write(f"**ChatBot:** {chat['bot']}")
