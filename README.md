# Chatbot SecGrad — Assistente de Orientação Acadêmica

Assistente conversacional baseado em RAG (Retrieval-Augmented Generation) para responder dúvidas frequentes sobre procedimentos acadêmicos, normas e requerimentos da Secretaria de Graduação (SecGrad) do Centro de Informática (CIn-UFPE).

---

## 🎯 Escopo do MVP
- **Requerimentos Acadêmicos:** Orientações sobre dispensa de disciplinas, segunda chamada, revisão de prova e requerimento geral.
- **Estágios:** Consulta a normas de estágio obrigatório e não obrigatório, requisitos de aptidão e regras específicas por curso e perfil curricular.
- **Respostas Ancoradas com Citação:** Indicação do documento oficial e número da página utilizada para a resposta.
- **Fallback Humano Estruturado:** Geração automática de modelo de e-mail pronto para envio quando o sistema detectar baixa confiança ou falta de evidências nas normas.

---

## 👥 Equipe e Responsabilidades
- **Ricardo:** Engenharia de Conhecimento, Coleta e Higienização de Documentos e Metadados (JSON).
- **Rafael:** Pipeline RAG, Estratégia de Chunking, Embeddings e Banco Vetorial (ChromaDB).
- **Victor:** Lógica Conversacional, System Prompts, Ancoragem e Gerador de E-mail de Fallback.
- **Eric:** Interface Web (Streamlit), Dataset de QA Benchmark e Documentação (PRD e ADRs).

---

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.11+
- **Banco Vetorial:** ChromaDB (execução local / localhost)
- **Framework RAG:** LangChain / LlamaIndex
- **Interface:** Streamlit
- **LLM / Embeddings:** API Google Gemini / OpenAI

---

## 🚀 Como Rodar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/cin-ds-chatbot.git](https://github.com/SEU_USUARIO/cin-ds-chatbot.git)
   cd cin-ds-chatbot