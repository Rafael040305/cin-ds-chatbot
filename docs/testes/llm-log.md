# Sprint 3 — Registro de uso de LLM

Este arquivo mantém a rastreabilidade do uso de LLM durante a Sprint 3. Novas interações relevantes devem ser adicionadas sem apagar as anteriores.

## Entrada 001 — Apoio ao planejamento da matriz

- **Data:** 28/10/2026
- **Responsável pela interação:** Rafael
- **Ferramenta:** Codex / modelo da OpenAI disponível na sessão
- **Tipo de uso:** estruturação assistida de requisitos e casos esperados
- **Arquivos de saída:** `docs/testes/matriz-rastreabilidade.md`
- **Não é:** geração da suíte de testes V1

### Contexto fornecido

Foram fornecidos o repositório atualizado, as orientações da professora para a Sprint 3 e o pedido para selecionar funcionalidades da Sprint 2, escrever user stories, definir critérios de aceitação, entradas, partições, valores-limite e casos esperados.

### Resultado produzido

A LLM propôs um rascunho de matriz para três fluxos já implementados:

1. busca semântica filtrada com fontes;
2. decisão de fallback;
3. geração de rascunho de e-mail.

O rascunho foi baseado nos contratos e comportamentos observados no FastAPI e no NestJS. A futura rota de geração por LLM foi excluída por não pertencer à implementação da Sprint 2.

### Limitação e validação necessária

A matriz não deve ser apresentada como elaboração manual independente. Antes da geração da suíte V1, os integrantes devem validar todos os critérios, partições, limites e resultados esperados e registrar a aprovação em novo commit. A conversa destinada à geração da V1 deve ser nova e não deve receber a matriz de referência.

## Modelo para as próximas entradas

Copiar a estrutura abaixo a cada rodada:

```text
## Entrada NNN — Título

- Data:
- Responsável:
- Ferramenta/modelo:
- Objetivo:
- Arquivos afetados:
- Prompt enviado:
- Resposta recebida:
- Ajustes manuais para compilar/executar:
- Resultado dos testes:
- Decisão da equipe:
```
