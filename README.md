# 🌐 AI Translator Agent

Um agente de tradução inteligente que usa **apenas a API Groq** (rápida e gratuita) para revisar e traduzir textos.

## ✨ Funcionalidades

- **Tradução Multi-idioma**: Recebe texto em qualquer idioma e traduz para PT-BR, ES e EN
- **Correção Gramatical**: Corrige automaticamente erros gramaticais e melhora a sintaxe
- **Melhoria de Clareza**: Aprimora a fluidez e clareza do texto mantendo o sentido original
- **Interface Web Moderna**: Interface intuitiva construída com Streamlit
- **Histórico de Conversas**: Mantém o contexto das traduções anteriores na sessão

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│                  Usuário                    │
│                     │                       │
│                     ▼                       │
│            ┌─────────────────┐              │
│            │   Streamlit     │              │
│            │   (Interface)   │              │
│            └────────┬────────┘              │
│                     │                       │
│               ┌─────▼─────┐                 │
│               │   Groq    │                 │
│               │  (Cloud)  │                 │
│               └───────────┘                 │
└─────────────────────────────────────────────┘
```

## 🚀 Pré-requisitos

1. **Docker** e **Docker Compose** instalados
2. **Chave de API da Groq** (gratuita): [console.groq.com/keys](https://console.groq.com/keys)

## 📦 Instalação

1. **Clone ou navegue até o diretório do projeto**:
```bash
cd ai-translator-agent
```

2. **Crie o arquivo `.env`** com sua chave da Groq:
```bash
echo 'GROQ_API_KEY=sua_chave_aqui' > .env
```

   > 📝 Obtenha sua chave gratuita em: [console.groq.com/keys](https://console.groq.com/keys)

3. **Suba o container**:
```bash
docker compose up -d --build
```

4. **Acesse a aplicação**:
   - Abra: `http://localhost:5000`
   - Se estiver no WSL: use o IP do WSL (`hostname -I`)

## 🏃 Como Usar

### Comandos Principais

```bash
# Iniciar a aplicação
docker compose up -d

# Ver logs da aplicação
docker compose logs -f ai-translator

# Parar tudo
docker compose down

# Reiniciar
docker compose restart

# Reconstruir após mudanças
docker compose up -d --build
```

### Verificar Status

```bash
# Status dos containers
docker compose ps
```

## 📁 Estrutura do Projeto

```
ai-translator-agent/
├── agent.py              # Aplicação principal (Streamlit + Groq)
├── Dockerfile            # Configuração da imagem Docker
├── docker-compose.yml    # Orquestração da aplicação
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (criar manualmente)
└── README.md             # Esta documentação
```

## 🔧 Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **Streamlit 1.40.0**: Framework para interface web
- **Groq API**: Backend de tradução (cloud, rápido, limites diários)
- **Llama 3.3 70B**: Modelo cloud via Groq
- **Docker**: Containerização

## 💡 Exemplo de Uso

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

### Groq: "Rate limit exceeded" ou erro de autenticação

- Confira se a variável `GROQ_API_KEY` está correta no arquivo `.env`
- Verifique no painel da Groq se sua chave ainda é válida

### Aplicação não abre (WSL)

```bash
# Descobrir IP do WSL
hostname -I

# Acessar pelo IP, ex: http://172.30.242.142:5000
```

## 🔒 Privacidade e Custos

| Backend | Privacidade | Custo | Limite |
|---------|-------------|-------|--------|
| Groq    | Dados vão para cloud | Gratuito | Depende do plano atual |

## 📄 Licença

Este projeto é de uso pessoal/educacional.

---

**Desenvolvido com ❤️ usando Streamlit e Groq**

