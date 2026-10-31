# Dívida Técnica — Serviço de IA/RAG

Este documento registra as dívidas técnicas identificadas no serviço
de IA durante a Sprint 3, incluindo impacto, prioridade, responsável,
plano de pagamento e critério de conclusão.

| ID | Dívida técnica | Impacto | Prioridade | Responsável | Status | Plano de pagamento | Critério de conclusão |
|---|---|---|---|---|---|---|---|
| AI-01 | Filtros de curso e perfil utilizavam `$contains` e não recuperavam documentos | Consultas com curso e perfil retornavam zero fontes e acionavam fallback incorretamente | Crítica | Rafael | Resolvida na Sprint 3 | Substituir busca textual por metadados booleanos e normalização de identificadores | Testes unitários e consultas reais retornam somente documentos do curso e perfil solicitados |
| AI-02 | Serviço de IA não possuía testes unitários | Alterações na ingestão e busca poderiam introduzir regressões sem detecção | Alta | Rafael | Resolvida na Sprint 3 | Criar testes independentes do ChromaDB real | Comando de testes executa oito testes com resultado `OK` |
| AI-03 | Reingestão não removia chunks antigos | Trechos de versões anteriores poderiam permanecer no banco | Alta | Rafael | Resolvida na Sprint 3 | Comparar IDs antigos e atuais e remover chunks obsoletos | Teste automatizado confirma a remoção dos IDs antigos |
| AI-04 | Limiar de distância `0.8` ainda não foi calibrado | O sistema pode aceitar contexto fraco ou acionar fallback desnecessariamente | Alta | Equipe | A avaliar | Registrar distâncias para perguntas conhecidas, desconhecidas e fora de escopo | Limiar documentado e aprovado com evidências do benchmark |
| AI-05 | Geração final por LLM ainda não está integrada ao fluxo | O sistema recupera contexto, mas ainda não produz a resposta final fundamentada | Alta | Rafael e Victor | Pendente | Definir endpoint, contrato, provedor, tratamento de falhas e formato da resposta | NestJS chama a geração somente quando houver contexto suficiente e devolve resposta com fontes |
| DATA-01 | Existem documentos duplicados em `data/raw` e `ai-service/data` | Risco de ingerir versões diferentes, incluindo PDFs sem OCR | Alta | Rafael e Ricardo | A avaliar | Confirmar `data/raw` como fonte canônica e remover a cópia antiga após revisão | Existe somente uma origem documental validada e documentada |
| DATA-02 | PPCs dos quatro cursos ainda não foram incorporados ao catálogo final | A base não cobre integralmente informações curriculares | Alta | Ricardo e Rafael | Pendente | Ricardo adiciona documentos e metadados; Rafael valida e reingere | Validador passa, todos os PPCs são ingeridos e consultas por curso retornam fontes corretas |
| INT-01 | Fluxo completo frontend → NestJS → FastAPI → ChromaDB ainda não foi validado | Testes isolados não comprovam a experiência completa do usuário | Crítica | Equipe | Pendente | Concluir contrato, integrar frontend e executar perguntas reais | Pergunta enviada pela interface retorna resposta ou fallback com fontes corretas |
| DOC-01 | README principal descreve componentes ainda não implementados e um comando de instalação inválido | Novo integrante pode não conseguir executar o projeto | Média | Equipe | Pendente | Atualizar arquitetura implementada e comandos reais | Instalação reproduzida por outro integrante em ambiente limpo |
| REPO-01 | `.gitignore` contém marcadores de conflito de merge | Repositório permanece inconsistente e pode ignorar arquivos incorretamente | Crítica | Equipe | Pendente | Remover os marcadores e consolidar as regras necessárias | Arquivo sem `<<<<<<<`, `=======` ou `>>>>>>>`, revisado pela equipe |

## Evidências da Sprint 3

As seguintes verificações foram concluídas:

- catálogo documental válido;
- ingestão de 8/8 documentos;
- 145 trechos armazenados no ChromaDB;
- oito testes unitários aprovados;
- consulta de CC novo recuperando somente a norma nova de CC;
- consulta de SI antigo recuperando somente a norma anterior de SI;
- endpoint `/health` respondendo HTTP 200;
- endpoint `/api/v1/buscar` respondendo HTTP 200;
- resposta contendo fontes, páginas e distância mínima.

## Próxima revisão

Esta tabela deverá ser revisada depois que:

1. Ricardo adicionar os PPCs;
2. Rafael reingerir e validar a base completa;
3. Victor e Rafael aprovarem o contrato da LLM;
4. Eric integrar a interface ao endpoint NestJS;
5. a equipe executar o benchmark e calibrar o fallback.