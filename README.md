
# 🎓 Chatbot SecGrad — Assistente de Orientação Acadêmica

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
- **Git** instalado
- **pip** (gerenciador de pacotes do Python)

### 1. Clonar o Repositório

Clone o repositório e acesse o diretório do projeto:

```bash
git clone https://github.com/Rafael040305/cin-ds-chatbot.git
cd cin-ds-chatbot
```

### 2. Configurar o Ambiente Virtual

Crie um ambiente virtual Python para isolar as dependências:

```bash
python -m venv venv
```

Em seguida, ative o ambiente conforme seu sistema operacional.

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

> **Nota:** mantenha o ambiente virtual ativado durante a instalação das dependências e a execução do projeto.

### 3. Instalar as Dependências

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

Esse comando instala as bibliotecas Python necessárias, conforme especificado no arquivo `requirements.txt`.

### 4. Realizar a Ingestão da Base Documental

O projeto utiliza o **ChromaDB** para indexar e recuperar semanticamente informações dos documentos normativos da SecGrad.

Acesse o diretório do microsserviço de IA:

```bash
cd ai-service
```

Execute o pipeline de ingestão:

```bash
python -m src.ingest_batch
```

Essa etapa é responsável por processar os documentos disponíveis, fragmentar o conteúdo e gerar as representações vetoriais utilizadas pelo sistema de recuperação.

### 5. Executar a Validação Semântica

Para verificar o mecanismo de recuperação de informações, execute:

```bash
python -m src.retriever
```

O objetivo dessa etapa é avaliar a recuperação de trechos documentais relevantes e verificar as referências utilizadas pelo sistema.

### 6. Iniciar a Interface do MVP

Retorne ao diretório raiz do projeto:

```bash
cd ..
```

Execute a interface desenvolvida em Streamlit:

```bash
streamlit run app.py
```

Após a inicialização, abra o endereço exibido no terminal.

Por padrão, o Streamlit utiliza:

**http://localhost:8501**

### ✅ Ambiente Preparado

Com a configuração concluída, o ambiente estará preparado para a execução do protótipo e a realização dos testes de recuperação documental.

> **Importante:** execute a ingestão dos documentos antes de realizar consultas que dependam da base vetorial.

---

## 📚 Contexto Acadêmico

Projeto desenvolvido para a disciplina de **Desenvolvimento de Software**, do Centro de Informática da Universidade Federal de Pernambuco (**CIn-UFPE**).

O objetivo é aplicar conceitos de engenharia de software, arquitetura de microsserviços e inteligência artificial na construção de uma solução de apoio à orientação acadêmica.

---

## ⚠️ Aviso Importante

O Chatbot SecGrad é uma ferramenta de apoio informacional e não substitui os canais oficiais de atendimento da Secretaria de Graduação.

As respostas devem ser interpretadas considerando os documentos normativos utilizados como referência. Em situações de dúvida, conflito de informações ou ausência de respaldo documental, recomenda-se consultar diretamente a SecGrad.
