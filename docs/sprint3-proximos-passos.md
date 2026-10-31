# Sprint 3 — Entrega incremental

Rafael implementou `/api/v1/gerar` com entrada pergunta/contexto e saída resposta textual ou null, modo mock explícito, erro seguro 503 quando desabilitado e testes de regressão. Mock não avalia suficiência documental: contexto não vazio não garante evidência. O provedor real ainda precisa ser conectado. Backend, interface e catálogo dos colegas foram preservados.

## Pendências e dependências

| Integrante | Falta entregar |
|---|---|
| Rafael | Validar matriz com equipe, preservar V1 gerada em conversa nova sem a matriz, medir/analisar cobertura, melhorar V2 e só depois realizar refatorações formais. Conectar provedor real após escolha de modelo/credenciais, tratar timeout/indisponibilidade, verificar fundamentação, atualizar manual e dívida com evidências. |
| Victor | Consumir gerar após busca aceitável, converter null em fallback, propagar erros técnicos seguros, acrescentar resposta ao contrato público e alinhar com Eric. Testar fluxo real e documentar V1/V2, métricas e refatorações da área. |
| Eric | Integrar interface ao NestJS, remover simulação silenciosa, mostrar resposta/fontes/fallback/erros reais, executar benchmark e consolidar manual. Confirmar marco de migração para React com docentes. |
| Ricardo | Revisar duplicação dos textos de extensão, procedência/URL/data/validade e aplicabilidade por curso; adicionar PPCs acordados, validar catálogo e conferir fontes. Documentar testes e dívida de dados. |

## Ordem

1. Todos aprovam histórias/critérios/matriz. Registrar assistência de LLM e confirmar com docente se o rascunho assistido atende à etapa manual.
2. Rafael e Victor integram com mock explícito; Eric adapta contrato público; Ricardo faz curadoria em paralelo.
3. Após curadoria publicada, Rafael atualiza branch, valida/reingere base e mede totais. Não excluir documentos dos colegas unilateralmente.
4. Conectar LLM real, testar sucesso fundamentado, null e erros técnicos; executar fluxo completo e benchmark.
5. Preservar V1, analisar, construir V2 e medir requisitos/partições/limites/branches; refatorar com V2 pronta e registrar antes/depois.
6. Consolidar relatório de qualidade, dívida com plano de pagamento, manual e evidências exigidas nos dois roteiros.

React, Keycloak/LDAP e Compose/Swarm seguem como requisitos gerais ainda pendentes; combinar responsáveis e marco com docentes. Estes testes de desenvolvimento não são automaticamente V1/V2 da atividade. Este planejamento e implementação receberam assistência do Codex; registrar a interação no log.
