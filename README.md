# 🌐 AI Translator Agent

Um agente de tradução inteligente baseado em IA que traduz, corrige gramática e melhora a clareza de textos em qualquer idioma. A aplicação gera automaticamente traduções para **Português (Brasil)**, **Espanhol** e **Inglês**, com detecção automática de e-mails e formatação adequada.

## ✨ Funcionalidades

- **Tradução Multi-idioma**: Recebe texto em qualquer idioma e traduz para PT-BR, ES e EN
- **Correção Gramatical**: Corrige automaticamente erros gramaticais e melhora a sintaxe
- **Melhoria de Clareza**: Aprimora a fluidez e clareza do texto mantendo o sentido original
- **Detecção de E-mails**: Identifica automaticamente e-mails e formata com saudação, corpo e despedida apropriados
- **Interface Web Moderna**: Interface intuitiva construída com Streamlit
- **Histórico de Conversas**: Mantém o contexto das traduções anteriores na sessão

## 🚀 Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Chave de API da Groq** ([obtenha aqui](https://console.groq.com/keys))

## 📦 Instalação

1. **Clone o repositório** (ou navegue até o diretório do projeto):
```bash
cd ai-translator-agent
```

2. **Crie o arquivo `.env`** na raiz do projeto:
```bash
echo 'GROQ_API_KEY=sua_chave_aqui' > .env
```

   Ou crie manualmente o arquivo `.env` com o seguinte conteúdo:
```
GROQ_API_KEY=sua_chave_da_groq_aqui
```

   > ⚠️ **Importante**: Substitua `sua_chave_da_groq_aqui` pela sua chave de API real da Groq.

## 🏃 Como Executar

### Usando Docker Compose (Recomendado)

1. **Construa e inicie o container**:
```bash
docker compose up --build
```

2. **Acesse a aplicação**:
   - Abra seu navegador e acesse: `http://localhost:5000`
   - Se estiver usando WSL, você pode precisar usar o IP do WSL: `http://172.30.242.142:5000` (substitua pelo IP do seu WSL)

3. **Para executar em background** (detached mode):
```bash
docker compose up -d --build
```

### Comandos Úteis

- **Ver logs**: `docker compose logs -f`
- **Parar a aplicação**: `docker compose down`
- **Reiniciar**: `docker compose restart`
- **Ver status**: `docker compose ps`

## 📁 Estrutura do Projeto

```
ai-translator-agent/
├── agent.py              # Aplicação principal Streamlit
├── Dockerfile            # Configuração da imagem Docker
├── docker-compose.yml    # Orquestração dos containers
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (criar manualmente)
└── README.md             # Esta documentação
```

## 🔧 Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **Streamlit 1.40.0**: Framework para interface web
- **Groq API**: API de IA para processamento de linguagem natural
- **Docker**: Containerização da aplicação
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 💡 Como Usar

1. **Acesse a interface web** em `http://localhost:5000`

2. **Digite ou cole um texto** em qualquer idioma no campo de entrada

3. **Aguarde o processamento** - o agente irá:
   - Corrigir erros gramaticais
   - Melhorar a clareza
   - Gerar traduções para os três idiomas (PT-BR, ES, EN)

4. **Para e-mails**: Se você colar um e-mail, o agente detectará automaticamente e formatará com:
   - Saudação apropriada
   - Corpo da mensagem
   - Despedida (sem incluir seu nome, pois a assinatura é adicionada automaticamente)

## 📝 Exemplo de Uso

**Entrada:**
```
Hello, I want to send a email to my boss about the project delay.
```

**Saída:**
```
### Português (Brasil)
Olá, gostaria de enviar um e-mail ao meu chefe sobre o atraso do projeto.

### Español
Hola, me gustaría enviar un correo electrónico a mi jefe sobre el retraso del proyecto.

### English
Hello, I would like to send an email to my boss about the project delay.
```

## 🐛 Troubleshooting

### Problema: "Connection reset by peer" ao acessar

**Solução**: 
- Verifique se o container está rodando: `docker compose ps`
- Verifique os logs: `docker compose logs`
- Certifique-se de que a porta 5000 não está sendo usada por outro processo

### Problema: "API Key não encontrada"

**Solução**:
- Verifique se o arquivo `.env` existe na raiz do projeto
- Confirme que o arquivo contém: `GROQ_API_KEY=sua_chave_aqui`
- Reinicie o container: `docker compose restart`

### Problema: Erro ao inicializar cliente Groq

**Solução**:
- Verifique se sua chave de API está correta
- Reconstrua a imagem: `docker compose up --build`
- Verifique se há problemas de conectividade com a API da Groq


## 🔒 Segurança

- **Nunca commite o arquivo `.env`** no controle de versão
- Mantenha sua chave de API segura e privada
- O arquivo `.env` já deve estar no `.gitignore`

## 📄 Licença

Este projeto é de uso pessoal/educacional.

## 🤝 Contribuindo

Sinta-se à vontade para abrir issues ou pull requests com melhorias!

---