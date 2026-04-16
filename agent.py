import json
import os

import streamlit as st
import streamlit.components.v1 as components
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


def _parse_translation_sections(text: str) -> dict[str, str]:
    """Extrai blocos PT / ES / EN do Markdown retornado pelo modelo."""
    markers: list[tuple[str, str]] = [
        ("pt", "### Português (Brasil)"),
        ("es", "### Español"),
        ("en", "### English"),
    ]
    result = {lang: "" for lang, _ in markers}
    for i, (lang, marker) in enumerate(markers):
        start = text.find(marker)
        if start == -1:
            continue
        body_start = start + len(marker)
        while body_start < len(text) and text[body_start] in "\r\n":
            body_start += 1
        end = len(text)
        for _, next_marker in markers[i + 1 :]:
            n = text.find(next_marker, body_start)
            if n != -1:
                end = min(end, n)
        result[lang] = text[body_start:end].strip()
    return result


def _render_translation_copy_buttons(text: str, *, row_id: str) -> None:
    """Três botões para copiar cada idioma (clipboard no navegador)."""
    parts = _parse_translation_sections(text)
    pt_js = json.dumps(parts["pt"])
    es_js = json.dumps(parts["es"])
    en_js = json.dumps(parts["en"])
    safe_id = "".join(c if c.isalnum() else "-" for c in row_id)
    # Identificador JS válido (sem hífen).
    js_suffix = "".join(c if c.isalnum() else "_" for c in row_id)
    # Funções com sufixo único: vários iframes na página não sobrescrevem umas às outras.
    components.html(
        f"""
        <script>
        function copyExecFallback_{js_suffix}(text) {{
            var ta = document.createElement("textarea");
            ta.value = text;
            ta.setAttribute("readonly", "");
            ta.style.position = "fixed";
            ta.style.left = "-9999px";
            ta.style.top = "0";
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            try {{
                document.execCommand("copy");
            }} finally {{
                document.body.removeChild(ta);
            }}
        }}
        function copyText_{js_suffix}(text) {{
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).catch(function () {{
                    copyExecFallback_{js_suffix}(text);
                }});
            }} else {{
                copyExecFallback_{js_suffix}(text);
            }}
        }}
        </script>
        <div id="copy-row-{safe_id}" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:0.35rem 0 0 0;">
            <button type="button"
                style="padding:0.2rem 0.5rem;font-size:0.78rem;border-radius:6px;border:1px solid #d0d7de;background:#f6f8fa;cursor:pointer;color:#24292f;"
                onclick='copyText_{js_suffix}({pt_js})'>Copiar PT-BR</button>
            <button type="button"
                style="padding:0.2rem 0.5rem;font-size:0.78rem;border-radius:6px;border:1px solid #d0d7de;background:#f6f8fa;cursor:pointer;color:#24292f;"
                onclick='copyText_{js_suffix}({es_js})'>Copiar ES</button>
            <button type="button"
                style="padding:0.2rem 0.5rem;font-size:0.78rem;border-radius:6px;border:1px solid #d0d7de;background:#f6f8fa;cursor:pointer;color:#24292f;"
                onclick='copyText_{js_suffix}({en_js})'>Copiar EN</button>
        </div>
        """,
        height=48,
    )


def _render_chat_bubble(role: str, content: str, *, message_index: int) -> None:
    if role == "assistant":
        st.markdown(content)
        _render_translation_copy_buttons(content, row_id=f"a-{message_index}")
    else:
        st.markdown(content)


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

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        _render_chat_bubble(message["role"], message["content"], message_index=idx)


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
        assistant_index = len(st.session_state.messages)
        with st.spinner("☁️ Gerando traduções via Groq..."):
            try:
                translated_response = call_groq(groq_client, messages_for_api)
                _render_chat_bubble(
                    "assistant",
                    translated_response,
                    message_index=assistant_index,
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": translated_response}
                )
            except Exception as e:
                st.error(f"❌ Erro ao gerar tradução: {e}")
