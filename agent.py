import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


SYSTEM_PROMPT = """Você é um assistente de tradução e revisão de texto.

REGRAS GERAIS:
1. Receba uma mensagem em qualquer idioma (pode ser uma frase completa ou uma palavra simples).
2. IMPORTANTE: Você DEVE SEMPRE traduzir o que foi enviado. NUNCA converse com o usuário, não faça perguntas, não dê explicações. Apenas traduza.
3. Se receber uma palavra simples, traduza a palavra simples.
4. Se receber uma frase, traduza a frase.
5. Sempre:
   - Corrija erros gramaticais (quando aplicável).
   - Melhore a sintaxe, fluidez e clareza (quando aplicável a frases).
   - Mantenha o sentido original da mensagem.
6. Gere SEMPRE as três versões abaixo, todas já corrigidas e melhoradas:
   - Português do Brasil.
   - Espanhol (neutro).
   - Inglês (internacional).

FORMATO DA RESPOSTA:
Responda sempre em Markdown seguindo exatamente esta estrutura:

### Português (Brasil)
<texto em português formatado conforme as regras acima>

### Español
<texto em espanhol formatado conforme as regras acima>

### English
<texto em inglês formatado conforme as regras acima>

LEMBRE-SE: Você é apenas um tradutor. Traduza sempre, sem conversar ou explicar.
"""


st.set_page_config(
    page_title="AI Translator Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_groq_client():
    """Inicializa o cliente Groq se a API key estiver disponível."""
    if not GROQ_API_KEY:
        return None, "API Key não configurada"
    try:
        client = Groq(api_key=GROQ_API_KEY)
        return client, None
    except Exception as e:
        return None, str(e)


def call_groq(client, messages):
    """Chama a API da Groq e retorna a resposta."""
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=0.3,
        max_tokens=2048,
    )
    return chat_completion.choices[0].message.content


groq_client, groq_error = init_groq_client()


with st.sidebar:
    st.title("🌐 AI Translator Agent")
    st.markdown(
        """
        Envie uma frase ou texto em qualquer idioma.

        O agente vai:
        - **Corrigir gramática e clareza**  
        - **Traduzir para PT-BR, Espanhol e Inglês**
        """
    )

    st.markdown("---")
    st.subheader("📡 Status")

    if groq_client:
        st.success(f"☁️ Groq: Online (`{GROQ_MODEL}`)")
    else:
        st.error(f"☁️ Groq: {groq_error or 'Não configurado'}")


st.title("AI Translator Agent")
st.caption(
    "Cole uma frase em qualquer idioma. "
    "O agente vai revisar e traduzir para Português (BR), Espanhol e Inglês."
)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Digite o texto a ser traduzido (qualquer idioma)...")

if user_input:
    if not groq_client:
        st.error(
            "❌ Backend indisponível!\n\n"
            "Configure `GROQ_API_KEY` no arquivo `.env`"
        )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        with st.spinner("☁️ Gerando traduções via Groq..."):
            try:
                translated_response = call_groq(groq_client, messages_for_api)
                st.markdown(translated_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": translated_response}
                )
            except Exception as e:
                st.error(f"❌ Erro ao gerar tradução: {e}")
