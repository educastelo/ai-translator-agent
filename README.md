# 🌐 AI Translator Agent

Um agente de tradução inteligente com **sistema híbrido de IA**: usa a API Groq (rápida e gratuita) como principal e faz fallback automático para modelo local na GPU quando o limite diário é atingido.

## ✨ Funcionalidades

- **🔄 Sistema Híbrido**: Groq como principal, Ollama (GPU local) como fallback automático
- **Tradução Multi-idioma**: Recebe texto em qualquer idioma e traduz para PT-BR, ES e EN
- **Correção Gramatical**: Corrige automaticamente erros gramaticais e melhora a sintaxe
- **Melhoria de Clareza**: Aprimora a fluidez e clareza do texto mantendo o sentido original
- **Detecção de E-mails**: Identifica automaticamente e-mails e formata com saudação, corpo e despedida
- **Interface Web Moderna**: Interface intuitiva construída com Streamlit
- **Histórico de Conversas**: Mantém o contexto das traduções anteriores na sessão

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                    Usuário                          │
│                       │                             │
│                       ▼                             │
│              ┌─────────────────┐                    │
│              │   Streamlit     │                    │
│              │   (Interface)   │                    │
│              └────────┬────────┘                    │
│                       │                             │
│         ┌─────────────┼─────────────┐               │
│         ▼                           ▼               │
│   ┌───────────┐              ┌───────────┐          │
│   │   Groq    │  ──fallback──▶│  Ollama   │          │
│   │  (Cloud)  │              │  (Local)  │          │
│   │           │              │   GPU     │          │
│   └───────────┘              └───────────┘          │
│    Principal                   Backup               │
└─────────────────────────────────────────────────────┘
```

## 🖥️ Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| GPU NVIDIA | 8GB VRAM | 12GB+ VRAM |
| RAM | 16GB | 32GB |
| CPU | Qualquer x64 | Ryzen 5000+ / Intel 10th+ |

> ✅ **Testado com**: RTX 3060 12GB, 32GB RAM, Ryzen 5800X

## 🚀 Pré-requisitos de Software

1. **Docker** e **Docker Compose** instalados
2. **NVIDIA Driver** atualizado (versão 525+)
3. **NVIDIA Container Toolkit** instalado
4. **Chave de API da Groq** (gratuita): [console.groq.com/keys](https://console.groq.com/keys)

### Instalar NVIDIA Container Toolkit (se necessário)

```bash
# Adicionar repositório NVIDIA
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Instalar
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configurar Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verificar instalação
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

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

3. **Inicie os containers**:
```bash
docker compose up -d --build
```

4. **Baixe o modelo de fallback** (primeira execução):
```bash
docker exec -it ollama ollama pull qwen2.5:7b-instruct
```

5. **Acesse a aplicação**:
   - Abra: `http://localhost:5000`
   - Se estiver no WSL: use o IP do WSL (`hostname -I`)

## 🏃 Como Usar

### Comandos Principais

```bash
# Iniciar a aplicação
docker compose up -d

# Ver logs da aplicação
docker compose logs -f ai-translator

# Ver logs do Ollama
docker compose logs -f ollama

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

# Uso da GPU
nvidia-smi

# Modelos carregados no Ollama
docker exec -it ollama ollama list
```

## 📁 Estrutura do Projeto

```
ai-translator-agent/
├── agent.py              # Aplicação principal (Groq + Ollama)
├── Dockerfile            # Configuração da imagem Docker
├── docker-compose.yml    # Orquestração (app + Ollama)
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (criar manualmente)
└── README.md             # Esta documentação
```

## 🔧 Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **Streamlit 1.40.0**: Framework para interface web
- **Groq API**: Backend principal (cloud, rápido, limites diários)
- **Ollama**: Backend de fallback (local, GPU)
- **Qwen2.5 7B**: Modelo local para tradução
- **Llama 3.3 70B**: Modelo cloud via Groq
- **Docker**: Containerização
- **NVIDIA CUDA**: Aceleração por GPU

## ⚙️ Configuração Avançada

### Modelos Disponíveis

**Groq (cloud)**:
| Modelo | Descrição |
|--------|-----------|
| `llama-3.3-70b-versatile` | **Padrão** - Melhor qualidade |
| `llama-3.1-8b-instant` | Mais rápido, menos preciso |
| `mixtral-8x7b-32768` | Boa alternativa |

**Ollama (local)**:
| Modelo | VRAM | Uso |
|--------|------|-----|
| `qwen2.5:7b-instruct` | ~4.4GB | **Padrão** - Melhor para tradução |
| `qwen2.5:3b-instruct` | ~2GB | Mais leve |
| `llama3.2:8b-instruct` | ~4.5GB | Alternativa |

### Trocar Modelos

Edite as variáveis no `docker-compose.yml`:
```yaml
environment:
  - GROQ_MODEL=llama-3.3-70b-versatile  # Modelo Groq
  - OLLAMA_MODEL=qwen2.5:7b-instruct     # Modelo local
```

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

### Groq: "Rate limit exceeded"

**Isso é normal!** Quando o limite diário do Groq é atingido, o sistema automaticamente usa o modelo local (Ollama).

Para evitar:
- Use menos requisições
- Espere o reset diário (meia-noite UTC)
- O fallback para Ollama é automático

### Ollama: "Modelo não carregado"

```bash
# Baixar o modelo
docker exec -it ollama ollama pull qwen2.5:7b-instruct

# Verificar modelos
docker exec -it ollama ollama list
```

### Ollama: "Container unhealthy"

```bash
# Aguardar inicialização (pode levar 30-60s)
docker compose ps

# Verificar logs
docker compose logs ollama
```

### GPU não detectada

```bash
# Verificar driver NVIDIA
nvidia-smi

# Reinstalar NVIDIA Container Toolkit (ver seção de pré-requisitos)

# Reiniciar Docker
sudo systemctl restart docker
```

### Aplicação não abre (WSL)

```bash
# Descobrir IP do WSL
hostname -I

# Acessar pelo IP, ex: http://172.30.242.142:5000
```

## 📊 Monitoramento

```bash
# GPU em tempo real
watch -n 1 nvidia-smi

# Logs em tempo real
docker compose logs -f

# Status dos containers
docker compose ps
```

## 🔒 Privacidade e Custos

| Backend | Privacidade | Custo | Limite |
|---------|-------------|-------|--------|
| Groq | Dados vão para cloud | Gratuito | ~14.400 req/dia |
| Ollama | 100% local | Gratuito | Ilimitado |

- ✅ Quando Groq atinge o limite, usa automaticamente Ollama (100% local)
- ✅ Seus dados só saem da máquina quando usando Groq

## 📄 Licença

Este projeto é de uso pessoal/educacional.

---

**Desenvolvido com ❤️ usando Streamlit, Groq e Ollama**

*Sistema híbrido: velocidade do cloud + privacidade do local!* 🚀
