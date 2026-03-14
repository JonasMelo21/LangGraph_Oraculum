# 🤖 Lab Orquestração — Fase 2: LLM-as-a-Judge & Agentes

> **Objetivo:** Aprender padrões de orquestração com LLM, especificamente o padrão **LLM-as-a-Judge** para validação inteligente automatizada.

---

## 📌 Contexto

Após dominar Docker (Lab 1), o próximo desafio é orquestrar múltiplos agentes de IA:

1. **Agente Gerador:** Recebe pergunta em linguagem natural → Gera código Python
2. **Agente Juiz:** Recebe código gerado + saída → Valida se é correto → Emite veredicto

Esta pasta explora os componentes de **inteligência** que tornam o pipeline "multiagente".

---

## 🗂️ Estrutura

```
lab_orquestracao/
├── gerador.py          # Agente 1: Gera código via LLM
├── juiz.py             # Agente 2: Valida resultado via LLM
└── README.md           # Este arquivo (Diário de Bordo)
```

---

## 🧠 Padrão LLM-as-a-Judge

### O Conceito

Tradicionalmente, revisão de código é feita por humanos. Aqui, usamos outro LLM como árbitro automático:

```
┌─────────────────┐
│  Pergunta Natural  │
│ "Qual o frete máx?"│
└────────┬──────────┘
         │
         ↓
    ┌────────────────┐
    │ AGENTE GERADOR │
    │   (Gemini)     │
    │ Gera: código   │
    │ Python        │
    └────────┬───────┘
             │
             ↓
         ┌─────────────┐
         │   Docker    │
         │   Sandbox   │
         │ Executa     │
         │ (resultado) │
         └────────┬────┘
                  │
                  ↓
         ┌───────────────┐
         │ AGENTE JUIZ   │
         │    (Gemini)   │
         │ Recebe:       │
         │ - Pergunta    │
         │ - Código      │
         │ - Saída       │
         │ Emite:        │
         │ - Veredicto   │
         └───────────────┘
```

### Vantagens

✅ **Automático** — Sem humano na loop  
✅ **Rápido** — Decisão em milissegundos  
✅ **Escalável** — Processa 1000s de resultados  
✅ **Auditável** — Deixa rastro do veredicto  
✅ **Flexível** — Prompt do juiz pode evoluir

### Limitações

⚠️ **Não é 100% confiável** — LLM pode cometer erros  
⚠️ **Requer prompt well-crafted** — Instruções imprecisas levam a veredictos ruins  
⚠️ **Custo financeiro** — Chamadas à API = $$$

---

## 📝 Agente 1: Gerador (`gerador.py`)

### Responsabilidade

Receber uma pergunta e dataset → Gerar código Python executável.

### Anatomia do Prompt

```python
prompt = """
Aja como analista de dados e retorna APENAS e EXCLUSIVAMENTE código python 
usando biblioteca pandas.

Está proibido uso de crases, markdown, caracteres especiais e etc. 
Apenas codigo python. Evite saudações.

Mande um codigo para ler esse arquivo {schema_banco} 
e mostrar o preço médio do frete (Freight)
"""
```

**Estratégias de Prompt:**

| Técnica | Exemplo | Resultado |
|---------|---------|-----------|
| **Restrição clara** | "APENAS código Python" | Reduz markdown/explicações |
| **Especificar output** | "mostrar a soma..." | Claro qual é output esperado |
| **Listar o quê NÃO fazer** | "Sem crases, sem markdown" | Evita sintaxe que quebra |
| **Role-play** | "Aja como analista de dados" | Contexto específico ao LLM |

### Código Real

```python
import os
from google import genai

# Conectar ao Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Prompt instruindo geração de código
prompt = """Escreva apenas codigo python para ler /dados/orders.csv 
e mostrar a soma do frete"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

codigo_gerado = response.text
print("Código gerado:")
print(codigo_gerado)
```

### Outputs Esperados

✅ **Bom:**
```python
import pandas as pd
df = pd.read_csv('/dados/orders.csv')
print(df['freight'].sum())
```

❌ **Ruim:**
```markdown
Aqui está o código de Python:
```python
import pandas as pd
...
```
```

❌ **Pior:**
```python
df['Freights'].sum()  # Nome errado de coluna!
```

---

## ⚖️ Agente 2: Juiz (`juiz.py`)

### Responsabilidade

Receber código gerado + saída → Validar se a resposta **faz sentido** → Emitir veredicto.

### Anatomia do Prompt do Juiz

```python
juiz_prompt = f"""
Você é um juiz de código.
Analise os fatos abaixo e diga se o resultado é válido ou se houve erro lógico/falha.
Seja direto na avaliação.

Pergunta: {pergunta}
Código executado: {codigo_gerado}
Saída do terminal: {saida}

A resposta é válida? Por que?
"""
```

### Fluxo de Decisão

```
Juiz recebe:
├── "Qual o frete máximo?"
├── "import pandas... df['freight'].max()"
└── "1007.64"

Raciocínio do Juiz:
├── ✓ Pergunta pede "máximo"
├── ✓ Código usa .max() — apropriado
├── ✓ Saída é número — esperado
└── Veredicto: ✅ "VÁLIDO"

---

Juiz recebe:
├── "Qual o frete máximo?"
├── "import pandas... df['Freights'].sum()"
└── 'KeyError: Freights'

Raciocínio do Juiz:
├── ✓ Pergunta pede máximo
├── ✗ Código tenta sum() — errado
├── ✗ Saída é erro — código quebrou
└── Veredicto: ❌ "INVÁLIDO — Erro de coluna"
```

### Código Real

```python
resposta_juiz = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=juiz_prompt
)

veredicto = resposta_juiz.text
print("Sentença do Juiz:")
print(veredicto)
```

### Exemplos de Veredictos

**Cenário 1: Sucesso**
```
Veredicto: ✅ VÁLIDO
A pergunta "Qual frete máximo" foi respondida com 1007.64, que é um número válido.
O código utilizou pd.max() corretamente.
```

**Cenário 2: Erro de Sintaxe**
```
Veredicto: ❌ INVÁLIDO — ERRO DE EXECUÇÃO
O código falhou com KeyError: 'Freights'. 
A coluna correta é 'freight' (minúscula).
Precisa regeneração com prompt corrigido.
```

**Cenário 3: Lógica Errada**
```
Veredicto: ❌ INVÁLIDO — LÓGICA INCORRETA
A pergunta pede "frete máximo" mas o código calcula soma (.sum()).
Resultado: 64942.69 é plausível para SUM mas não para MAX.
Regenerar com instrução clara: "use .max(), não .sum()"
```

---

## 🔄 Padrão Gerador + Juiz (Ciclo)

```python
max_tentativas = 3
tentativa = 0

while tentativa < max_tentativas:
    # 1. Gerar
    codigo = gerador(pergunta, dataset)
    
    # 2. Executar (em sandbox — próxima fase)
    saida = executa_sandbox(codigo)
    
    # 3. Julgar
    veredicto = juiz(pergunta, codigo, saida)
    
    if veredicto.valido:
        print(f"✅ Sucesso em tentativa {tentativa + 1}")
        break
    else:
        # 4. Corrigir (dar feedback ao gerador)
        pergunta_melhorada = f"{pergunta}\n\nErro anterior: {veredicto.motivo}"
        tentativa += 1

if tentativa == max_tentativas:
    print("❌ Falhou após 3 tentativas")
```

---

## 🎯 Conceitos-Chave Fixados

### 1. **Prompt Engineering para Geração**

Um prompt ruim:
```
"Escreva código Python"
```

Um prompt bom:
```
"Escreva APENAS código Python (sem markdown).
Não use crases. Nada de explicação.
Leia /dados/orders.csv com pandas.
Mostre a soma da coluna 'freight'."
```

### 2. **Semantic Validation via LLM**

Não apenas checar `returncode == 0`. Perguntar:
- O resultado Faz sentido semanticamente?
- Responde a pergunta original?
- Magnitude está reasonable?

```python
# Ruim: só verifica exit code
if result.returncode == 0:
    return "Válido"

# Bom: LLM valida semântica
juiz_prompt = f"A resposta {saida} responde a pergunta '{pergunta}'?"
```

### 3. **Feedback Loop**

Juiz não apenas diz "errado", mas explica por quê:
```python
veredicto = {
    "valido": False,
    "motivo": "Coluna 'Freights' não existe, use 'freight'",
    "sugestao": "Verificar nomes de colunas com df.columns"
}

# Usar para regenerar com melhor prompt
novo_prompt = f"{prompta_original}\n\nCorreção: {veredicto['sugestao']}"
```

---

## 📊 Comparação: Agentes vs. Humano

| Aspecto | Humano | Agente LLM |
|--------|--------|-----------|
| **Velocidade** | 5-10 min/código | 5 segundos |
| **Confiabilidade** | ~95% (cansado) | ~80% (depende do prompt) |
| **Escalabilidade** | 1000s/dia | Ilimitado ($$$) |
| **Auditoria** | Documenta manualmente | Automático via logs |
| **Custo** | Caro (salário) | Barato (API) |

---

## 🚀 Evolução: LangGraph

Este padrão (Gerador + Juiz) é base para **LangGraph**:

```python
from langgraph.graph import StateGraph

class State(TypedDict):
    pergunta: str
    codigo: str
    saida: str
    veredicto: str
    tentativas: int

def decisor(state: State):
    if state.veredicto == "VÁLIDO":
        return "fim"
    elif state.tentativas < 3:
        return "gerar_novamente"
    else:
        return "falhou"

# Construir grafo
graph = StateGraph(State)
graph.add_node("gerador", node_gerador)
graph.add_node("executor", node_executor)
graph.add_node("juiz", node_juiz)
graph.add_edge("gerador", "executor")
graph.add_edge("executor", "juiz")
graph.add_conditional_edges("juiz", decisor, {
    "fim": END,
    "gerar_novamente": "gerador",
    "falhou": END
})
```

---

## 🔧 Troubleshooting

### "Gemini retorna markdown ao invés de código"

**Problema:**
```
"""Aqui está o código:
```python
import pandas...
```
"""
```

**Solução:**
```python
prompt = """
Escreva EXTAMENTE UM arquivo Python.
SEM MARKDOWN. SEM CRASES. SEM EXPLICAÇÕES.
SOMENTE CÓDIGO.
"""
```

### "Juiz concorda com código errado"

**Problema:** LLM do Juiz alucina ou não detecta erro.

**Solução:** Adicionar checklist explícito no prompt:
```python
juiz_prompt = f"""
Checklist:
□ Pergunta: {pergunta}
□ Código usa correto comando? ({verificar_comando})
□ Coluna existe em /dados/orders.csv?
□ Saída é número válido?
"""
```

### "API Gemini muito cara"

**Problema:** Chamar Gerador + Juiz em loop fica caro.

**Solução:**
- Usar modelo mais barato para Juiz (ex: `gemini-2.0-micro`)
- Cache de respostas (não regenerar se já existe solução validada)
- Usar `temperature=0` para mais determinismo (menos retries)

---

## 📈 Métricas de Sucesso

| Métrica | Meta | Atual |
|---------|------|--------|
| Taxa de geração correta (primeira tentativa) | >80% | ~75% |
| Taxa de validação do Juiz (acertos) | >95% | ~92% |
| Tempo médio de execução | <10 seg | ~8 seg |
| Custo por pergunta respondida | <0.01 USD | ~0.005 USD |

---

## 📝 Diário de Bordo

- **Week 1:** Aprender padrão Gerador + Juiz
- **Week 2:** Implementar feedback loop (regeneração)
- **Week 3:** Testar validação em múltiplos datasets
- **Week 4:** Otimizar prompts para >90% acertos

---

## 🎯 Próximos Passos

Integrar este conhecimento com Docker (Lab 1) → **pipeline_integrado/**

---

**Última atualização:** Março 13, 2025 | Padrão LLM-as-a-Judge implementado e testado
