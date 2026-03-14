# Text-to-Insight Lab 🚀

## Visão Geral

**Text-to-Insight Lab** é um laboratório de arquitetura multiagente que demonstra a integração de LLMs (Large Language Models), orquestração de containers Docker e engenharia de prompts para construir sistemas de IA aplicados. O projeto implementa um pipeline de dois agentes inteligentes que geram, validam e executam código Python dinamicamente.

**Contexto**: Desenvolvido como parte do projeto **LangGraph_Oraculum** em colaboração com a RAIA (Rede de Apoio em Inteligência Artificial) @ USP.

---

## 🎯 Objetivo Principal

Criar um sistema onde:
1. **Agente 1 (Gerador)**: Recebe um dataset em CSV e uma pergunta em linguagem natural → gera código Python
2. **Agente 2 (Validador)**: Executa o código gerado em sandbox Docker → valida se passou ou falhou
3. **Pipeline**: Toda a orquestração acontece em containers isolados com Docker

---

## 📁 Estrutura do Projeto

```
text-to-insight-lab/
├── README.md                          # Este arquivo
├── main.py                            # Entrada principal
├── pyproject.toml                     # Dependências do projeto
│
├── lab_docker/                        # 📚 Aprendizado: Fundamentos de Docker
│   ├── README.md                      # Diário de bordo do Docker
│   ├── Dockerfile                     # Dockerfile base
│   └── ex*.py                         # Exercícios de aprendizado (5 exercícios)
│
├── lab_orquestracao/                  # 📚 Aprendizado: Arquitetura de Agentes
│   ├── README.md                      # Diário de bordo de orquestração
│   ├── gerador.py                     # Estudo de geração de código
│   └── juiz.py                        # Estudo de validação/julgamento
│
├── pipeline_integrado/                # 🎯 APLICAÇÃO PRINCIPAL
│   ├── README.md                      # Diário técnico da aplicação
│   ├── passo1_ponte.py                # Build da imagem Docker
│   ├── passo2_sandbox.py              # Agente Gerador (LLM → Código)
│   ├── passo3_loop.py                 # Agente Validador (Execução → Validação)
│   ├── Dockerfile_sandbox             # Container isolado para execução
│   ├── codigo_ia.py                   # Código gerado dinamicamente
│   └── codigo_loop.py                 # Código de loop/validação
│
└── northwind/                         # 📊 Dataset (Northwind Database)
    ├── *.csv                          # 7 arquivos CSV
    └── docs_northwind/                # Documentação do dataset
```

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────┐
│         AGENTE 1: GERADOR (passo2_sandbox.py)       │
│  Prompt Natural → API Gemini 2.5 Flash → Python    │
│  "Soma os fretes"  →  [código gerado dinamicamente]│
└──────────────┬──────────────────────────────────────┘
               │ escreve em volume Docker
               ↓
        ┌──────────────────┐
        │  Docker Sandbox  │
        │  (isolado, --rm) │
        └──────────────────┘
               │ executa
               ↓
      ┌─────────────────────┐
      │  Terminal Output    │
      │  (stdout/stderr)    │
      └──────────┬──────────┘
                 │
┌────────────────┴────────────────────────────────────┐
│      AGENTE 2: VALIDADOR (passo3_loop.py)          │
│  Pergunta + Código + Saída → API Gemini → Passou? │
│  "Máximo frete?" + output + [regra] →  SIM/NÃO    │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Pré-requisitos
```bash
python 3.9+
Docker
API Key do Google Gemini
```

### Setup
```bash
# Clone e configure
git clone <repo>
cd text-to-insight-lab

# Crie um arquivo .env na raiz
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Instale dependências
pip install -r pyproject.toml   # ou use `uv`

# Build da imagem Docker
python pipeline_integrado/passo1_ponte.py

# Execute o pipeline
python pipeline_integrado/passo2_sandbox.py  # Gera código
python pipeline_integrado/passo3_loop.py     # Valida código
```

---

## 📚 Jornada de Aprendizado

Este projeto foi desenvolvido em **três etapas progressivas**:

### 1️⃣ **lab_docker/** - Fundamentos (Semana 1)
- **O quê**: Aprendizado de Docker e containers
- **Objetivo**: Entender isolamento, volumes, flags (`--rm`, `-v`)
- **Resultado**: 5 exercícios progressivos de Docker
- **Lição chave**: "A flag `--rm` é VITAL — ela mata o container após execução"

### 2️⃣ **lab_orquestracao/** - Orquestração (Semana 2)
- **O quê**: Arquitetura de agentes inteligentes
- **Objetivo**: Separação de responsabilidades (Gerador vs Juiz)
- **Resultado**: Protótipos de agentes isolados
- **Lição chave**: "Um agente não pode ser juiz de si mesmo"

### 3️⃣ **pipeline_integrado/** - Integração (Semana 3-4) ⭐
- **O quê**: Fusão de tudo → Sistema de 2 agentes funcional
- **Objetivo**: Pipeline end-to-end com LLM + Docker + Validação
- **Resultado**: Sistema que gera e valida código automaticamente
- **Inovação**: Uso de Gemini para validação, não só geração

---

## 🔬 Casos de Uso Implementados

### ✅ Caso 1: Agregação (passo2_sandbox.py)
```
Entrada: "Soma o valor do frete (freight)"
Saída:   "64942.69"
Validado: SIM
```

### ✅ Caso 2: Busca de Extremo (passo3_loop.py)
```
Entrada: "Qual foi o frete mais caro?"
Saída:   "1007.64"
Validado: SIM/NÃO (depende da resposta da IA)
```

---

## 🛠️ Tecnologias

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| **LLM** | Google Gemini 2.5 Flash | Latest |
| **Container** | Docker | Latest |
| **Orquestração** | Python subprocess | 3.9+ |
| **Dataset** | Northwind (CSV) | Histórico |
| **Prompting** | Chain-of-Thought | Manual |

---

## 🎓 Lições Técnicas Aprendidas

### Docker
- ✅ Flag `--rm` para limpeza automática
- ✅ Volumes `-v` para comunicação host-container
- ✅ Isolamento de ambientes com Dockerfile

### LLMs & Prompting
- ✅ Especificidade em prompts (ex: "coluna 'freight'" vs "coluna Freights")
- ✅ Duas chamadas de API (geração + validação)
- ✅ Tratamento de erros via stderr capturado

### Arquitetura
- ✅ Separação de agentes por responsabilidade
- ✅ Pipeline de validação em dois passos
- ✅ Isolamento total com containers

---

## 📊 Métricas de Maturidade

- ✅ **Documentação**: Diários de bordo em cada pasta
- ✅ **Código**: Comentários explicativos (diários técnicos)
- ✅ **Testes**: Casos validados com IA
- ✅ **DevOps**: Containers, volumes, limpeza automática
- ✅ **Comunicação**: READMEs estruturados

---

## 🔮 Próximos Passos (Roadmap)

- [ ] Integrar com LangGraph formal (com langgraph library)
- [ ] Persistência de logs (banco de dados)
- [ ] Dashboard web para visualizar execuções
- [ ] Suporte a múltiplos formatos de dados (JSON, Parquet)
- [ ] Retry automático com backoff exponencial
- [ ] Testes unitários e integração
- [ ] CI/CD (GitHub Actions)

---

## 📝 Como Contribuir

1. Entenda a estrutura das pastas (lab_docker → lab_orquestracao → pipeline_integrado)
2. Siga o padrão de "diário de bordo" nos comentários (`# [DIÁRIO DE BORDO]`)
3. Documente suas decisões técnicas nos READMEs
4. Teste com passo1 → passo2 → passo3 em sequência

---

## 📬 Contato & Context

**Projeto**: Text-to-Insight Lab  
**Afiliação**: RAIA (Rede de Apoio em Inteligência Artificial) @ USP  
**GitHub**: JonasMelo21/LangGraph_Oraculum  
**Data de Início**: Março 2026

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes

---

**"Onde código encontra cognição, e insight emerge da engenharia."** ✨