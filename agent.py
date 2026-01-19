import os
import json

import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# Configuração do Groq (principal)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Configuração do Ollama (fallback)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")


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


# ============================================
# Funções para Groq
# ============================================

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
    """
    Chama a API da Groq.
    Retorna (resposta, is_rate_limited)
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            temperature=0.3,
            max_tokens=2048,
        )
        return chat_completion.choices[0].message.content, False
    except Exception as e:
        error_str = str(e).lower()
        # Verifica se é erro de rate limit
        if "rate" in error_str or "limit" in error_str or "429" in error_str or "quota" in error_str:
            return None, True
        raise


# ============================================
# Funções para Ollama (fallback)
# ============================================

def check_ollama_status():
    """Verifica se o Ollama está disponível e se o modelo está carregado."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            model_available = any(
                OLLAMA_MODEL in name or OLLAMA_MODEL.split(":")[0] in name
                for name in model_names
            )
            return True, model_available, model_names
        return False, False, []
    except requests.exceptions.RequestException:
        return False, False, []


def call_ollama(messages):
    """Chama o modelo via Ollama usando a API de chat."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 2048,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=300)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro ao conectar ao Ollama: {e}") from e

    if response.status_code != 200:
        raise RuntimeError(f"Ollama retornou código {response.status_code}: {response.text}")

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Resposta inválida do Ollama: {e}") from e

    msg = data.get("message")
    if not msg or "content" not in msg:
        raise RuntimeError(f"Não foi possível encontrar o conteúdo na resposta: {data}")

    return msg["content"]


# ============================================
# Interface Streamlit
# ============================================

# Inicializa cliente Groq
groq_client, groq_error = init_groq_client()

# Verifica status do Ollama
ollama_online, ollama_model_ready, available_models = check_ollama_status()


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
    st.subheader("📡 Status dos Backends")

    # Status do Groq
    if groq_client:
        st.success(f"☁️ Groq: Online (`{GROQ_MODEL}`)")
    else:
        st.warning(f"☁️ Groq: {groq_error or 'Não configurado'}")

    # Status do Ollama
    if ollama_online and ollama_model_ready:
        st.success(f"🖥️ Ollama: Online (`{OLLAMA_MODEL}`)")
    elif ollama_online:
        st.warning(f"🖥️ Ollama: Modelo não carregado")
        st.caption(f"Execute: `docker exec -it ollama ollama pull {OLLAMA_MODEL}`")
    else:
        st.error("🖥️ Ollama: Offline")

    st.markdown("---")
    st.caption("**Prioridade:** Groq → Ollama (fallback)")
    st.caption("Se o limite diário do Groq acabar, usa modelo local automaticamente.")


st.title("AI Translator Agent")
st.caption(
    "Cole uma frase em qualquer idioma. "
    "O agente vai revisar e traduzir para Português (BR), Espanhol e Inglês."
)


# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Input do usuário
user_input = st.chat_input("Digite o texto a ser traduzido (qualquer idioma)...")

if user_input:
    # Verifica se pelo menos um backend está disponível
    if not groq_client and not (ollama_online and ollama_model_ready):
        st.error(
            "❌ Nenhum backend disponível!\n\n"
            "- Configure `GROQ_API_KEY` no arquivo `.env`\n"
            "- Ou aguarde o Ollama inicializar e baixe o modelo"
        )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        translated_response = None
        backend_used = None

        # Tenta Groq primeiro
        if groq_client:
            with st.spinner("☁️ Gerando traduções via Groq..."):
                try:
                    response, is_rate_limited = call_groq(groq_client, messages_for_api)
                    if response:
                        translated_response = response
                        backend_used = "groq"
                    elif is_rate_limited:
                        st.warning("⚠️ Limite diário do Groq atingido. Usando modelo local...")
                except Exception as e:
                    st.warning(f"⚠️ Erro no Groq: {e}. Tentando modelo local...")

        # Fallback para Ollama se Groq falhou ou não está disponível
        if translated_response is None:
            if ollama_online and ollama_model_ready:
                with st.spinner("🖥️ Gerando traduções via Ollama (GPU local)..."):
                    try:
                        translated_response = call_ollama(messages_for_api)
                        backend_used = "ollama"
                    except Exception as e:
                        st.error(f"❌ Erro ao usar Ollama: {e}")
            else:
                st.error(
                    "❌ Não foi possível gerar a tradução.\n\n"
                    "- Groq atingiu o limite ou está indisponível\n"
                    "- Ollama não está pronto como fallback"
                )

        # Exibe resposta se obtida
        if translated_response:
            # Indicador de qual backend foi usado
            if backend_used == "groq":
                st.caption("_☁️ Resposta gerada via Groq_")
            else:
                st.caption("_🖥️ Resposta gerada via Ollama (GPU local)_")

            st.markdown(translated_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": translated_response}
            )
