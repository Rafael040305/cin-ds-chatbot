# 🎓 Chatbot SecGrad — Assistente de Orientação Acadêmica

> **Estado atual:** Integração de ponta a ponta (Streamlit UI ➔ NestJS Orchestrator ➔ FastAPI AI-Service) totalmente operacional. O protótipo consome o contrato `/api/v1/conversa`, suportando busca vetorial com indicação de fontes e ativando o serviço de *fallback* com minuta de e-mail personalizada para dúvidas fora do escopo normativo.

### Execução corrigida do serviço de IA

Na raiz, instale `python -m pip install -r ai-service/requirements-dev.txt`; entre em `ai-service`, execute `python -m src.validate_catalog`, `python -m src.ingest_batch` e `python -m uvicorn main:app --reload --port 8000`. Swagger: http://localhost:8000/docs. Para testes: `python -m unittest discover -s tests -v`. A dependência `httpx` é usada nos testes HTTP.

O catálogo canônico é `data/raw/metadata.json`; `ai-service/data/` é legado. Contagens antigas precisam ser medidas novamente após atualizar os documentos. A geração simulada requer `SECGRAD_GENERATION_MODE=mock` e retorna aviso explícito. Sem configuração retorna 503 para contexto não vazio; contexto vazio retorna `resposta: null`.

Assistente conversacional baseado em **RAG (Retrieval-Augmented Generation)**, desenvolvido para responder a dúvidas frequentes sobre procedimentos acadêmicos, normas e requerimentos da Secretaria de Graduação (SecGrad) do Centro de Informática da Universidade Federal de Pernambuco (**CIn-UFPE**).

O projeto adota uma arquitetura de microsserviços conteinerizada, integrando recuperação vetorial especializada, citação obrigatória de fontes normativas e autenticação institucional.

---

## 🎯 Escopo do MVP — Sprint 2

O Produto Mínimo Viável (MVP) contempla as seguintes funcionalidades:

- **Requerimentos Acadêmicos:** orientações sobre dispensa de disciplinas, segunda chamada de prova, revisão de nota e requerimentos gerais da secretaria.

- **Normas de Estágio:** consulta às regras de estágio supervisionado por curso (Ciência da Computação, Engenharia da Computação e Sistemas de Informação) e perfis curriculares.

- **Respostas Auditáveis com Citação:** indicação obrigatória do documento oficial utilizado como referência e do número da página correspondente.

- **Tratamento de Incerteza (Fallback Estruturado):** recusa de respostas sem respaldo documental e geração de um rascunho de e-mail formal para a SecGrad quando não houver informações suficientes na base de conhecimento.

> **Princípio do sistema:** priorizar a confiabilidade das informações acadêmicas, garantindo rastreabilidade das fontes e reduzindo a ocorrência de respostas não fundamentadas.

---

## 🏛️ Arquitetura do Sistema

A solução é organizada em serviços desacoplados, com responsabilidades específicas:

| Serviço | Tecnologias | Responsabilidades |
|---------|-------------|-------------------|
| `frontend/` | React 18, Vite, TypeScript, Cinnamon | Interface conversacional e interação com o usuário |
| `backend/` | NestJS 11, Prisma, PostgreSQL | API Gateway, orquestração de rotas, sessões e segurança |
| `ai-service/` | Python, FastAPI, LangChain, ChromaDB | Ingestão documental, geração de embeddings e recuperação vetorial |
| `keycloak` | Keycloak, LDAP | Gerenciamento de identidade e autenticação institucional |

### 🔍 Funcionamento do RAG

O mecanismo de recuperação aumentada por geração segue o fluxo conceitual:

1. **Ingestão documental:** processamento dos documentos normativos fornecidos pela SecGrad.
2. **Fragmentação (Chunking):** divisão dos documentos em trechos menores, preservando metadados relevantes.
3. **Vetorização (Embeddings):** representação semântica dos trechos para permitir buscas por similaridade.
4. **Armazenamento vetorial:** indexação dos documentos no ChromaDB.
5. **Recuperação semântica:** identificação dos trechos mais relevantes para a pergunta do usuário.
6. **Geração fundamentada:** construção de respostas com base nos documentos recuperados, acompanhadas das respectivas referências.
7. **Fallback:** quando não houver suporte documental suficiente, o sistema evita gerar uma resposta não fundamentada e oferece um rascunho de e-mail para a secretaria.

---

## 👥 Equipe e Responsabilidades

| Integrante | Área | Responsabilidades |
|------------|------|-------------------|
| **Rafael Ramos** | Inteligência Artificial & RAG | Microsserviço de IA (`ai-service`), pipeline RAG, chunking, embeddings e ChromaDB |
| **Eric** | Front-end & QA | Interface de usuário, benchmarks de qualidade e registros de arquitetura |
| **Ricardo** | Engenharia de Conhecimento | Curadoria documental, organização das normas da SecGrad e catálogo de metadados (`metadata.json`) |
| **Victor** | Back-end & Autenticação | Serviço NestJS (`backend`), integração com Keycloak e orquestração de rotas |

---

## 🛠️ Stack Tecnológica

A arquitetura do projeto utiliza as seguintes tecnologias:

| Camada | Tecnologias |
|--------|-------------|
| **Front-end** | React 18, TypeScript, Vite, Cinnamon |
| **Protótipo do MVP** | Streamlit |
| **Back-end** | NestJS 11, Node.js 24, Prisma ORM, PostgreSQL |
| **Autenticação** | Keycloak, LDAP |
| **Microsserviço de IA** | Python 3.11+, FastAPI, Uvicorn |
| **Busca Vetorial & RAG** | ChromaDB, PyPDF, LangChain Text Splitters |
| **LLM / Provedores** | Google Gemini API, OpenAI API |
| **Infraestrutura** | Docker, Docker Compose |

---

## 🚀 Como Executar o Projeto Localmente

Siga as etapas abaixo para configurar o ambiente de desenvolvimento e executar o MVP.

### 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir:

- **Python 3.11 ou superior**
- **Node.js 20+ / npm**
- **Git** instalado
- **pip** (gerenciador de pacotes do Python)

### 1. Clonar o Repositório

Clone o repositório e acesse o diretório do projeto:

```bash
git clone [https://github.com/Rafael040305/cin-ds-chatbot.git](https://github.com/Rafael040305/cin-ds-chatbot.git)
cd cin-ds-chatbot