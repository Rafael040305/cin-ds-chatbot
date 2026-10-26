# Manual do Desenvolvedor — Serviço de IA/RAG

## 1. Objetivo

O `ai-service` é o microsserviço responsável pela recuperação de
informações acadêmicas utilizadas pelo Chatbot SecGrad.

Suas responsabilidades atuais são:

- processar documentos PDF e TXT;
- dividir o conteúdo em trechos;
- gerar e armazenar embeddings no ChromaDB;
- filtrar documentos por curso e perfil curricular;
- recuperar trechos semanticamente relacionados à pergunta;
- devolver contexto, fontes e distância para o backend NestJS.

A geração final por LLM ainda depende da aprovação do contrato entre o
serviço de IA e o backend.

## 2. Estrutura principal

```text
ai-service/
├── main.py
├── requirements.txt
├── chroma_db/
├── src/
│   ├── config.py
│   ├── index_utils.py
│   ├── ingest.py
│   ├── ingest_batch.py
│   ├── metadata_utils.py
│   ├── retriever.py
│   └── validate_catalog.py
└── tests/
    ├── __init__.py
    ├── test_index_utils.py
    ├── test_metadata_utils.py
    └── test_retriever.py