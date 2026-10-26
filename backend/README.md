<p align="center">
  <a href="http://nestjs.com/" target="blank"><img src="https://nestjs.com/img/logo-small.svg" width="120" alt="Nest Logo" /></a>
</p>

[circleci-image]: https://img.shields.io/circleci/build/github/nestjs/nest/master?token=abc123def456
[circleci-url]: https://circleci.com/gh/nestjs/nest

  <p align="center">A progressive <a href="http://nodejs.org" target="_blank">Node.js</a> framework for building efficient and scalable server-side applications.</p>
    <p align="center">
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/v/@nestjs/core.svg" alt="NPM Version" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/l/@nestjs/core.svg" alt="Package License" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/dm/@nestjs/common.svg" alt="NPM Downloads" /></a>
<a href="https://circleci.com/gh/nestjs/nest" target="_blank"><img src="https://img.shields.io/circleci/build/github/nestjs/nest/master" alt="CircleCI" /></a>
<a href="https://discord.gg/G7Qnnhy" target="_blank"><img src="https://img.shields.io/badge/discord-online-brightgreen.svg" alt="Discord"/></a>
<a href="https://opencollective.com/nest#backer" target="_blank"><img src="https://opencollective.com/nest/backers/badge.svg" alt="Backers on Open Collective" /></a>
<a href="https://opencollective.com/nest#sponsor" target="_blank"><img src="https://opencollective.com/nest/sponsors/badge.svg" alt="Sponsors on Open Collective" /></a>
  <a href="https://paypal.me/kamilmysliwiec" target="_blank"><img src="https://img.shields.io/badge/Donate-PayPal-ff3f59.svg" alt="Donate us"/></a>
    <a href="https://opencollective.com/nest#sponsor"  target="_blank"><img src="https://img.shields.io/badge/Support%20us-Open%20Collective-41B883.svg" alt="Support us"></a>
  <a href="https://twitter.com/nestframework" target="_blank"><img src="https://img.shields.io/twitter/follow/nestframework.svg?style=social&label=Follow" alt="Follow us on Twitter"></a>
</p>
  <!--[![Backers on Open Collective](https://opencollective.com/nest/backers/badge.svg)](https://opencollective.com/nest#backer)
  [![Sponsors on Open Collective](https://opencollective.com/nest/sponsors/badge.svg)](https://opencollective.com/nest#sponsor)-->

## Description

[Nest](https://github.com/nestjs/nest) framework TypeScript starter repository.

## Project setup

Use Node.js 24.x (also declared in `.nvmrc` and `package.json`).

```bash
$ nvm use
$ npm ci
```

## Docker

From the repository root, build and run the backend independently:

```bash
docker build -t secgrad-backend ./backend
docker run --rm -p 3000:3000 secgrad-backend
```

The image uses Node.js 24 for build and runtime, installs only production
dependencies in the final stage, and runs as the unprivileged `node` user.
The API listens on port 3000 by default; when setting `PORT`, adjust the port
mapping accordingly.

## Integração com o ai-service

`AiServiceModule` exporta `AiService.buscarContexto(consulta)`, usado pela
orquestração NestJS. O `AppController` expõe `POST /api/v1/conversa` e delega
para `OrchestrationService.processar(request)`. Os módulos estão registrados
no `AppModule`.

Configure `AI_SERVICE_URL` no ambiente com a origem HTTP/HTTPS do ai-service
(esquema, host e porta, sem caminho, query, fragmento ou credenciais). Por exemplo,
para execução local do FastAPI na porta 8000:

```bash
AI_SERVICE_URL=http://localhost:8000 npm run start:dev
```

No Docker, passe `-e AI_SERVICE_URL=...` com o endereço acessível ao container.
Não existe host padrão; arquivos `.env` não são carregados automaticamente.
A configuração é verificada ao chamar a busca; sua ausência não impede o backend
de iniciar, mas a busca retorna uma exceção de indisponibilidade.

O serviço faz `POST /api/v1/buscar` com `pergunta` obrigatória e os opcionais
`curso` (padrão `Geral`), `perfil` (`Todos`) e `top_k` (inteiro positivo, padrão 3).
Retorna `contexto`, `fontes` (`arquivo`, `pagina` numérica e `curso`) e
`distancia_minima`, após validar o contrato em runtime. Uma busca vazia válida
é preservada; não é confundida com erro de comunicação.

O timeout é de 5 segundos, incluindo leitura do corpo; não há retries automáticos.
Consulta inválida gera `BadRequestException` (400); configuração inválida ou erro
de conexão, `ServiceUnavailableException` (503); timeout,
`GatewayTimeoutException` (504); HTTP não bem-sucedido, JSON inválido ou contrato
incompatível, `BadGatewayException` (502). Mensagens não expõem respostas internas,
URLs ou detalhes da exceção original. Redirecionamentos não são seguidos.

Os testes unitários simulam o fetch; a suíte e2e inclui um servidor HTTP local
para verificar transporte e resolução do serviço no NestJS. Isso não substitui a
validação futura com o FastAPI/ChromaDB reais. O `AiService` não implementa LLM,
Keycloak ou decisão de fallback; a decisão pertence à orquestração descrita abaixo.

## POST /api/v1/conversa

Recebe JSON com `consulta` obrigatória e `dados_email` opcional:

```bash
curl -X POST http://localhost:3000/api/v1/conversa \
  -H 'Content-Type: application/json' \
  -d '{"consulta":{"pergunta":"Como solicitar dispensa?","curso":"Ciência da Computação","perfil":"novo","top_k":3}}'
```

`consulta.pergunta` deve ser uma string não vazia. `curso` e `perfil`, quando
informados, devem ser strings; `top_k` deve ser inteiro positivo. `dados_email`
aceita `nome`, `matricula`, `assunto` e `resumo`, todos strings opcionais.
Sucesso retorna **HTTP 201**, com `contexto`, `fontes`, `distancia_minima` e
`fallback_acionado`. Se houver fallback, também retorna `setor_sugerido` e
`template_email`. Entrada inválida retorna 400; falhas da busca retornam
502/503/504 conforme descrito acima, sem gerar fallback de e-mail.
A rota devolve trechos recuperados: **não gera respostas por LLM**, não mantém
histórico e não envia e-mail.

### Curso/perfil: valores atuais e pendências da equipe

O backend não define enum nem converte siglas/anos: repassa as strings recebidas.
Quando omitidos, envia `curso: "Geral"` e `perfil: "Todos"`; no retriever esses
valores desativam o respectivo filtro (strings vazias também não aplicam filtro).

O catálogo `../data/raw/metadata.json`, utilizado por
`../ai-service/src/ingest_batch.py`, contém:

- `curso_alvo`: `Ciência da Computação`, `Engenharia da Computação`,
  `Sistemas de Informação`, `Sistemas de Informações` e `Inteligência Artificial`.
- `perfil_curricular`: `novo`, `anterior` e `ambos`.

A ingestão une listas de cursos em strings; o retriever aplica `$contains` em
`curso_alvo` e `perfil_curricular`. O backend não traduz `CC`/`2023`, usados em
alguns testes de transporte, para nomes de cursos/perfis do catálogo. Esses testes
não comprovam recuperação semântica para tais valores. Há também divergência
entre `Sistemas de Informação` e `Sistemas de Informações`; `ambos` não recebe
tratamento especial que o inclua automaticamente nas buscas por `novo`/`anterior`.
Além disso, a rota de ingestão do ai-service fornece `curso`/`perfil`, enquanto o
retriever filtra `curso_alvo`/`perfil_curricular` usados pela ingestão em lote.

**Pendências compartilhadas:** equipe de IA/curadoria/frontend deve acordar o
vocabulário e a semântica dos filtros, alinhar as formas de ingestão e validar
consultas com a base real. A calibração de `FALLBACK_DISTANCE_THRESHOLD` também
depende do corpus e da métrica reais. Nenhuma conversão ou mudança de contrato
é introduzida pelo backend nesta entrega.

## Orquestração e fallback por e-mail

`OrchestrationModule` importa `AiServiceModule` e exporta
`OrchestrationService.processar(request)`, chamado pela rota de conversa. `FallbackService` gera somente texto para revisão e
cópia pelo usuário: não envia e-mail nem define endereço de destinatário.

Exemplo de entrada do serviço:

```typescript
const resultado = await orchestrationService.processar({
  consulta: {
    pergunta: 'Como solicitar dispensa?',
    curso: 'Ciência da Computação',
    perfil: 'novo',
    top_k: 3,
  },
  dados_email: {
    nome: 'Ana',
    matricula: '123',
    assunto: 'Dispensa de disciplina',
    resumo: 'Gostaria de orientação sobre a solicitação.',
  },
});
```

`dados_email` e seus campos são opcionais. Campos pessoais ausentes ou vazios
viram marcadores editáveis; sem assunto, usa-se a pergunta. Curso e perfil vêm
da consulta e a dúvida é a própria pergunta. Somente `consulta` é enviada ao
ai-service; os dados adicionais do e-mail não são enviados nem registrados em log.

A regra aciona fallback quando `distancia_minima >= FALLBACK_DISTANCE_THRESHOLD`
(inclusive na igualdade) **ou** quando `contexto.trim()` está vazio. Assim, contexto
vazio ou composto apenas por espaços em branco aciona fallback mesmo abaixo do
limiar. **O padrão 0.8 é provisório, herdado da prova de conceito e NÃO é
validado cientificamente nem definitivo.** Distância não representa probabilidade
ou percentual de confiança. O limiar precisa ser calibrado com a métrica, os
embeddings e o corpus reais antes de uso como critério validado.

`FALLBACK_DISTANCE_THRESHOLD` é opcional. Quando ausente, usa 0.8; quando presente,
deve ser um número decimal finito não negativo (aceita notação científica).
Valor vazio, negativo, não numérico ou infinito impede a inicialização do módulo
com mensagem de configuração inválida. Não há teto arbitrário de 1, pois o domínio
depende da métrica de distância. A configuração é lida uma vez na inicialização;
mudanças exigem reiniciar o backend. `AI_SERVICE_URL` continua sendo validada pelo
`AiService` ao chamar a busca, conforme a seção anterior. Não há carregamento
automático de `.env`.

```bash
AI_SERVICE_URL=http://localhost:8000 FALLBACK_DISTANCE_THRESHOLD=0.8 npm run start:dev
```

Os resultados são uma união discriminada por `fallback_acionado`:

- `false`: retorna `contexto`, `fontes` e `distancia_minima` para uma futura etapa
  de LLM; não gera resposta de LLM nesta tarefa.
- `true`: preserva os mesmos dados recuperados e acrescenta `setor_sugerido` e
  `template_email`. Os trechos não são inseridos automaticamente no e-mail.

As sugestões de setor preservam a ordem da referência Python: estágio,
requerimento, dispensa e segunda chamada sugerem SecGrad; assunto pedagógico
sugere NEAP; pós-graduação sugere Secretaria de Pós-Graduação; demais assuntos
sugerem SecGrad. São sugestões da prova de conceito, não novas regras
administrativas ou garantia de competência do setor.

Erros seguros do `AiService` são propagados sem transformar indisponibilidade em
fallback. Ausência de contexto sempre aciona fallback, independentemente do
limiar customizado. Contexto válido abaixo do limite continua no fluxo normal.
O contexto original é preservado no resultado; `trim()` serve apenas à decisão.
Não há LLM, autenticação ou envio de e-mail. Os arquivos Python antigos permanecem
apenas como referência conceitual.

Testes unitários cobrem limiar padrão/customizado/inválido, igualdade, geração do
template, sugestões de setor, contexto vazio/em branco e propagação de erros.
`test/app.e2e-spec.ts` exercita a rota HTTP com `OrchestrationService`,
`FallbackService` e `AiService` reais, simulando o `fetch` externo e o sinal de
timeout. Cobre sucesso, filtros/padrões, privacidade dos dados de e-mail, fallback,
entradas inválidas e erros 502/503/504. `test/ai-service.e2e-spec.ts` usa um servidor
HTTP local simulado para verificar transporte e decisão. Nenhum desses testes
exige FastAPI/ChromaDB reais; a validação integrada e a calibração continuam pendentes.

## Compile and run the project

```bash
# development
$ npm run start

# watch mode
$ npm run start:dev

# production mode
$ npm run start:prod
```

## Run tests

```bash
# unit tests
$ npm run test

# e2e tests
$ npm run test:e2e

# test coverage
$ npm run test:cov
```

## Deployment

When you're ready to deploy your NestJS application to production, there are some key steps you can take to ensure it runs as efficiently as possible. Check out the [deployment documentation](https://docs.nestjs.com/deployment) for more information.

If you are looking for a cloud-based platform to deploy your NestJS application, check out [Mau](https://mau.nestjs.com), our official platform for deploying NestJS applications on AWS. Mau makes deployment straightforward and fast, requiring just a few simple steps:

```bash
$ npm install -g @nestjs/mau
$ mau deploy
```

With Mau, you can deploy your application in just a few clicks, allowing you to focus on building features rather than managing infrastructure.

## Observability

In production applications, observability is essential for understanding how your system behaves, detecting issues early, and maintaining reliable performance.

[NestJS Observe](https://observe.nestjs.com) automatically instruments your NestJS application, giving you deep visibility into your system with minimal setup:

- **Distributed tracing:** Follow requests across services and understand how they flow through your system.
- **Waterfall analysis:** Visualize request execution and identify slow operations, bottlenecks, and unexpected delays.
- **Performance analysis:** Analyze application performance in real time and quickly pinpoint areas that need optimization.
- **Metrics:** Track key application and infrastructure metrics to understand system health and performance trends.
- **Logging:** Centralize and correlate logs with traces and other telemetry to make debugging easier.
- **Error tracking:** Detect errors quickly and investigate their root causes with the surrounding context.
- **SLA monitoring:** Track service-level objectives and identify when your application is approaching or exceeding defined thresholds.
- **Alarms and alerts:** Set up alerts for critical errors, performance degradation, SLA violations, and other anomalies so your team can react quickly.

To add it to this project:

```bash
$ npm install @nestjs/observe
```

Then follow the [setup guide](https://docs.nestjs.com/observability/overview) - it takes a single import and an app key.

The free plan needs no payment details and covers 300,000 events a month. You can also browse the [live demo](https://www.observe-demo.nestjs.com/dashboard) first - the whole dashboard over a busy service's data, with nothing to install.

## Resources

Check out a few resources that may come in handy when working with NestJS:

- Visit the [NestJS Documentation](https://docs.nestjs.com) to learn more about the framework.
- For questions and support, please visit our [Discord channel](https://discord.gg/G7Qnnhy).
- To dive deeper and get more hands-on experience, check out our official video [courses](https://courses.nestjs.com/).
- Deploy your application to AWS with the help of [NestJS Mau](https://mau.nestjs.com) in just a few clicks.
- Auto-instrument your application with [NestJS Observe](https://observe.nestjs.com). Distributed tracing, metrics, and logging made easy. Error tracking and performance monitoring for your NestJS applications.
- Visualize your application graph and interact with the NestJS application in real-time using [NestJS Devtools](https://devtools.nestjs.com).
- Need help with your project (part-time to full-time)? Check out our official [enterprise support](https://enterprise.nestjs.com).
- To stay in the loop and get updates, follow us on [X](https://x.com/nestframework) and [LinkedIn](https://linkedin.com/company/nestjs).
- Looking for a job, or have a job to offer? Check out our official [Jobs board](https://jobs.nestjs.com).

## Support

Nest is an MIT-licensed open source project. It can grow thanks to the sponsors and support by the amazing backers. If you'd like to join them, please [read more here](https://docs.nestjs.com/support).

## Stay in touch

- Author - [Kamil Myśliwiec](https://twitter.com/kammysliwiec)
- Website - [https://nestjs.com](https://nestjs.com/)
- Twitter - [@nestframework](https://twitter.com/nestframework)

## License

Nest is [MIT licensed](https://github.com/nestjs/nest/blob/master/LICENSE).
