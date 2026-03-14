# 📓 Diário de Bordo: Integração TextToInsight

**Objetivo desta fase:** Unir as três frentes de nivelamento (Geração de Código, Sandboxing com Docker e Orquestração com LLM-as-a-Judge) em um fluxo único e automatizado.

No projeto TextToInsight, não teremos um humano rodando `docker run` no terminal. O próprio orquestrador em Python (futuramente usando LangGraph) precisará instanciar o ambiente isolado, injetar o código gerado pelo modelo, capturar a saída (ou o erro) e mandar para o agente validador. 

## 🏗️ Arquitetura da Integração
1. **Passo 1 (A Ponte):** Fazer o Python controlar o Docker via biblioteca `subprocess`.
2. **Passo 2 (A Sandbox Dinâmica):** Fazer o LLM gerar um código, salvar fisicamente, mapear via volume e executar isolado.
3. **Passo 3 (O Loop MVP):** Avaliar a saída da Sandbox usando o LLM-as-a-Judge para decidir se a execução foi um sucesso ou se precisa de correção.

---