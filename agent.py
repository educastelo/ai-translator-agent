import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# Lê a chave de API da Groq da variável de ambiente
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


SYSTEM_PROMPT = """
Você é um assistente de tradução e revisão de texto.

REGRAS GERAIS:
1. Receba uma mensagem em qualquer idioma.
2. Sempre:
   - Corrija erros gramaticais.
   - Melhore a sintaxe, fluidez e clareza.
   - Mantenha o sentido original da mensagem.
3. Gere SEMPRE as três versões abaixo, todas já corrigidas e melhoradas:
   - Português do Brasil.
   - Espanhol (neutro).
   - Inglês (internacional).

DETECÇÃO DE E-MAIL:
1. Se a entrada do usuário for um e-mail (por exemplo, possuir assunto, saudação, corpo, despedida, assinatura ou claramente parecer um e-mail profissional):
   - Para CADA idioma (PT-BR, ES, EN), devolva o texto nesse formato exato:

     Saudação

     Corpo da mensagem

     Fechamento (ex: \"Atenciosamente\", \"Best regards\", \"Saludos\")

   - NÃO inclua o nome do remetente, pois a assinatura já é adicionada automaticamente pelo cliente de e-mail.

FORMATO DA RESPOSTA:
Responda sempre em Markdown seguindo exatamente esta estrutura:

### Português (Brasil)
<texto em português formatado conforme as regras acima>

### Español
<texto em espanhol formatado conforme as regras acima>

### English
<texto em inglês formatado conforme as regras acima>
"""


st.set_page_config(
    page_title="AI Translator Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)


with st.sidebar:
    st.title("🌐 AI Translator Agent")
    st.markdown(
        """
        Envie uma frase ou texto em qualquer idioma.

        O agente vai:
        - **Corrigir gramática e clareza**  
        - **Traduzir para PT-BR, Espanhol e Inglês**  
        - **Detectar e-mails** e devolver já formatados com saudação, corpo e despedida.
        """
    )

    if not GROQ_API_KEY:
        st.error(
            "A variável de ambiente `GROQ_API_KEY` não foi encontrada.\n\n"
            "Crie um arquivo `.env` na raiz do projeto com a linha:\n"
            "`GROQ_API_KEY=SUAS_CHAVE_AQUI`"
        )


st.title("AI Translator Agent")
st.caption(
    "Cole uma frase ou um e-mail em qualquer idioma. "
    "O agente vai revisar e traduzir para Português (BR), Espanhol e Inglês."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


client = None
groq_error = None

if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        groq_error = str(e)
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.sidebar.info("💡 Dica: Tente reconstruir a imagem Docker com: docker compose up --build")
else:
    groq_error = "API Key não encontrada"


user_input = st.chat_input("Digite o texto a ser traduzido (qualquer idioma)...")

if user_input:
    if not client:
        if groq_error:
            st.error(f"❌ Erro na inicialização: {groq_error}")
        else:
            st.warning(
                "Cliente Groq não foi inicializado. "
                "Verifique se a variável de ambiente `GROQ_API_KEY` está configurada corretamente no arquivo `.env`."
            )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        with st.spinner("Gerando traduções..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.3,
                    max_tokens=1024,
                )

                translated_response = chat_completion.choices[0].message.content

                st.markdown(translated_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": translated_response}
                )
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")
