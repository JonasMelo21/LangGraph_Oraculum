# 🐳 Lab Docker — Fase 1: Aprendizado de Containerização

> **Objetivo:** Dominar os fundamentos de Docker para entender isolamento de ambientes, volumes e execução de aplicações em containers.

---

## 📌 Contexto

Antes de orquestrar agentes de IA, foi necessário aprender Docker do zero. Esta pasta contém exercícios progressivos que levaram à capacidade de:

1. Criar imagens personalizadas
2. Mapear volumes (injetar código, acessar dados)
3. Capturar stdout/stderr de containers
4. Controlar containers via Python (subprocess)

**Foco:** Garantir que código gerado por LLM rodar isolado e seguro em sandbox.

---

## 🗂️ Estrutura dos Exercícios

```
lab_docker/
├── Dockerfile              # Imagem base usada em todos os exercícios
├── helloworld.py          # Ex00: Verificar Docker basicamente
├── ex02.py                # Ex02: Variáveis de ambiente
├── ex03.py                # Ex03: Volumes + leitura de dados
├── ex04.py                # Ex04: Controlar containers via subprocess
├── ex05.py                # Ex05: Captura de err/out + tratamento
└── README.md              # Este arquivo
```

---

## 🚀 Executar Exercícios

### Setup Inicial

```bash
# Entrar no diretório
cd lab_docker/

# Build da imagem Docker (uma vez)
docker build -t imagem_lab_docker .

# Agora qualquer exercício consegue rodar
```

### Exercício 00: Hello World

```bash
python helloworld.py

# Output esperado:
# Hello from Docker!
# E informações sobre Python inside
```

**O que aprendemos:**
- Estrutura básica de `docker run`
- Imagem vs Container
- Verificar se Docker está instalado

---

### Exercício 02: Variáveis de Ambiente

```bash
python ex02.py

# Output esperado:
# MY_ENV_VAR=hello_from_docker
```

**O que aprendemos:**
- Flag `-e` para passagem de variáveis
- Acesso a env via `os.environ`
- Útil para injetar GEMINI_API_KEY later

**Código-chave:**
```python
comando = [
    "docker", "run", "--rm",
    "-e", "MY_ENV_VAR=hello_from_docker",
    "imagem_lab_docker",
    "python", "-c", "import os; print(os.environ['MY_ENV_VAR'])"
]
```

---

### Exercício 03: Volumes + Dados

```bash
python ex03.py

# Output esperado:
# Conteúdo do arquivo local injetado no container
```

**O que aprendemos:**
- Flag `-v` para mapear volumes
- Sintaxe: `-v /caminho/host:/caminho/container`
- Permite compartilhamento de dados bidirecional

**Código-chave:**
```python
vol_dados = f"{raiz}/dados_lab:/dados"

comando = [
    "docker", "run", "--rm",
    "-v", vol_dados,
    "imagem_lab_docker",
    "python", "script_que_le_dados.py"
]
```

**Relevância para o projeto:**
Este conceito é CRUCIAL no pipeline. Salvamos código gerado em `pipeline_integrado/codigo_ia.py` e mapeamos via volume:
```python
vol_codigo = f"{raiz}/pipeline_integrado:/app"
```

---

### Exercício 04: subprocess + Docker

```bash
python ex04.py

# Output esperado:
# Resultado da execução interna do container capturado
```

**O que aprendemos:**
- Usar `subprocess.run()` para controlar Docker via Python
- Evitar terminal manual → Automação
- `capture_output=True` para pegar stdout/stderr

**Código-chave:**
```python
resultado = subprocess.run(
    comando,
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print("Sucesso:", resultado.stdout)
else:
    print("Erro:", resultado.stderr)
```

**Relevância para o projeto:**
Passo 1 do pipeline (`passo1_ponte.py`) usa exatamente esse padrão para fazer build da imagem sandbox.

---

### Exercício 05: Tratamento de Erros

```bash
python ex05.py

# Testa diferentes cenários:
# 1. Execução bem-sucedida
# 2. Erro de sintaxe Python
# 3. FileNotFoundError (arquivo não existe)
```

**O que aprendemos:**
- Exit code != 0 = erro
- stderr é onde mensagens de erro aparecem
- Logging e tratamento robusto

**Código-chave:**
```python
resultado = subprocess.run(
    comando,
    capture_output=True,
    text=True,
    timeout=30
)

if resultado.returncode == 0:
    # Sucesso
    pass
else:
    # Falha — stderr contém mensagem
    error_msg = resultado.stderr
    # Registrar log, retry, notify user
```

**Relevância para o projeto:**
Passo 3 (`passo3_loop.py`) captura stderr e o passa ao "Juiz" para análise. Se a IA gerou código que dá erro, o stderr diz o quê.

---

## 🔑 Conceitos-Chave Fixados

### 1. **Isolamento via Container**
```
Host (seu PC)           Container (sandbox)
├── /home/user/   ←→   /app (volume)
├── dados.csv     ←→   /dados (volume)
└── [Código executado isolado, sem afetar host]
```

### 2. **Volumes = Injeção Segura**
- Host controla entrada/saída
- Container não consegue sair do escopo
- Perfeito para executar código gerado por LLM

### 3. **subprocess = Orquestração**
```python
# Em vez de digitar no terminal:
# $ docker run --rm -v ... imagem python script.py

# Fazemos em Python:
subprocess.run([
    "docker", "run", "--rm", 
    "-v", volume,
    "imagem",
    "python", "script.py"
])
```

### 4. **Exit Code = Verdade**
- `returncode == 0` ✓ Sucesso
- `returncode != 0` ✗ Falha
- Permite decisões automáticas no Judge

---

## 📊 Mapa Mental: Docker → Pipeline

```
LAB_DOCKER (Fundamentals)
├── Hello World              → Verificar setup
├── Env Vars                 → Passar GEMINI_API_KEY
├── Volumes                  → Injetar código gerado
├── subprocess               → Orquestração
└── Error Handling           → Detectar falhas

         ↓ (Aplicado em)

PIPELINE_INTEGRADO (Production)
├── Passo 1: Ponte Docker
│   └── Build image via subprocess
├── Passo 2: Sandbox Dinâmica
│   ├── Gera código via Gemini
│   ├── Salva em arquivo
│   ├── Mapeia via volume
│   └── Executa isolado
└── Passo 3: Loop + Judge
    ├── Captura saída (do Lab_Docker Ex05)
    ├── Passa ao LLM-Judge
    └── Emite veredicto
```

---

## 🎯 Lições Aprendidas

| Conceito | Aprendizado | Evitado |
|----------|-------------|---------|
| **Dockerfile** | Criar imagem customizada com Python + pandas | Usar imagem genérica sem dependências |
| **Volumes** | Mapear `/dados` e `/app` para komunikação | Copiar arquivos manualmente (lento) |
| **subprocess** | Controlar Docker via Python | Executar tudo manualmente no terminal |
| **Error Handling** | Capturar stderr e exit codes | Ignorar erros, deixar silent failures |
| **Security** | Container isolado contra código malicioso | Executar código LLM diretamente no host |

---

## 🔧 Troubleshooting

### Docker não encontrado
```bash
sudo apt-get install docker.io
sudo usermod -aG docker $USER
# Logout e login
```

### Permissão negada ao build
```bash
sudo docker build -t imagem_lab_docker .
# ou
sudo usermod -aG docker $USER
```

### Imagem não encontrada
```bash
# Verificar imagens existentes
docker images

# Rebuildar
docker build -t imagem_lab_docker lab_docker/
```

---

## 🚀 Próximos Passos

Após dominar os conceitos aqui, seguir para:

1. **lab_orquestracao/** → Aprender LLM como agente de decisão
2. **pipeline_integrado/** → Integrar Docker + LLM num fluxo automático

---

## 📝 Diário de Bordo

- **Semana 1:** Aprender Docker basics (hello world → volumes)
- **Semana 2:** Dominar subprocess e captura de erros
- **Semana 3:** Preparado para sandboxing seguro de código LLM

---

**Última atualização:** Março 13, 2025 | Laboratório completo e funcional
