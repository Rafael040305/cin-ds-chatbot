# Chatbot SecGrad — Assistente de Orientação Acadêmica

Assistente conversacional baseado em RAG (Retrieval-Augmented Generation) para responder a dúvidas frequentes sobre procedimentos académicos, normas e requerimentos da Secretaria de Graduação (SecGrad) do Centro de Informática (CIn-UFPE).

O projeto adota uma **arquitetura de microsserviços** conteinerizada, integrando autenticação federada institucional e recuperação vetorial especializada.

---

## 🎯 Escopo do MVP
- **Requerimentos Acadêmicos:** Orientações sobre dispensa de disciplinas, segunda chamada, revisão de provas e requerimentos gerais[cite: 1].
- **Normas de Estágios:** Consulta a regras de estágio obrigatório e não obrigatório, requisitos de aptidão e regras específicas por curso (CC, EC, SI) e perfil curricular[cite: 1].
- **Respostas Ancoradas com Citação:** Indicação explícita do documento oficial consultado e do número da página correspondente[cite: 1].
- **Fallback Humano Estruturado:** Geração automática de modelo de e-mail pré-preenchido para a SecGrad quando o sistema detetar baixa confiança ou ausência de evidências normativas[cite: 1].

---

## 🏛️ Arquitetura de Microsserviços

A solução é distribuída em serviços independentes orquestrados via Docker:

- **`frontend/` (React):** Interface web do utilizador com chat conversacional e exibição de fontes auditáveis[cite: 1, 12].
- **`backend/` (NestJS · Node 24):** API Gateway responsável pela regra de negócio, gestão de sessão e integração com autenticação institucional.
- **`ai-service/` (Python / FastAPI):** Microsserviço dedicado de IA responsável pela ingestão de PDFs, banco vetorial (ChromaDB) e pipeline de RAG.
- **`keycloak`:** Gestão de identidade e autenticação federada via LDAP[cite: 12].

---

## 👥 Equipe e Responsabilidades
- **Ricardo:** Engenharia de Conhecimento, Curadoria de Documentos da SecGrad e Mapeamento de Metadados (JSON)[cite: 1, 2].
- **Rafael:** Microsserviço de IA (`ai-service`), Pipeline RAG, Chunking de PDFs, Embeddings e Banco Vetorial (ChromaDB)[cite: 2, 12].
- **Victor:** Back-end (`backend`), Serviço NestJS, Integração de Autenticação (Keycloak) e Orquestração de Fallback[cite: 12, 14].
- **Eric:** Front-end (`frontend`), Aplicação React, Benchmark de QA, PRD e Registos de Decisão Arquitetural (ADRs)[cite: 12].

---

## 🛠️ Stack Tecnológica
- **Front-end:** React, TypeScript, TailwindCSS[cite: 12]
- **Back-end:** NestJS, Node 24[cite: 12]
- **Autenticação:** Keycloak / LDAP[cite: 12]
- **Microsserviço de IA:** Python 3.11+, FastAPI, Uvicorn[cite: 12]
- **Busca Vetorial & RAG:** ChromaDB, PyPDF, LangChain Text Splitters[cite: 2, 12]
- **LLM / Provedor:** Google Gemini API / OpenAI API[cite: 2]
- **Deploy & Infraestrutura:** Docker e Docker Compose[cite: 12]

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados na máquina.
- Git instalado.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/Rafael040305/cin-ds-chatbot.git](https://github.com/Rafael040305/cin-ds-chatbot.git)
cd cin-ds-chatbot