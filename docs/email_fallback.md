# Fallback de E-mail

## Objetivo

Quando o chatbot não tiver contexto suficiente para responder com segurança, ele não deve inventar uma resposta.

Nesse caso, o sistema deve:

1. informar que não encontrou informações suficientes nas fontes disponíveis;
2. coletar os dados necessários do aluno;
3. resumir a situação apresentada na conversa;
4. identificar o setor responsável;
5. gerar um modelo de e-mail pronto para envio.

## Dados que podem ser necessários

- nome completo;
- matrícula;
- curso;
- perfil curricular;
- assunto da solicitação;
- descrição do problema;
- disciplina envolvida, quando aplicável;
- modalidade do estágio, quando aplicável;
- documentos já disponíveis;
- outras informações relevantes para o caso.

## Comportamento esperado

O chatbot não deve enviar o e-mail automaticamente.

Ele deve apenas gerar um texto estruturado para o aluno revisar, copiar e enviar ao setor responsável.

## Estrutura sugerida do e-mail

Assunto:
[assunto resumido]

Corpo:

Olá,

Meu nome é [nome], matrícula [matrícula], aluno(a) do curso de [curso], perfil curricular [perfil].

Estou entrando em contato sobre [assunto].

Resumo da situação:
[resumo gerado com base na conversa]

Minha dúvida é:
[dúvida principal]

Informações adicionais:
[informações relevantes]

Atenciosamente,
[nome]

## Quando acionar o fallback

O fallback deve ser acionado quando ocorrer pelo menos uma das situações abaixo:

1. O contexto recuperado não contém informação suficiente para responder à pergunta.
2. As fontes recuperadas apresentam informações conflitantes.
3. A pergunta depende de dados do aluno que ainda não foram informados e, mesmo após coleta, não há base suficiente para responder.
4. O assunto exige análise humana ou decisão administrativa que o chatbot não pode tomar.
5. A pergunta está relacionada a um setor específico e a base disponível não contém resposta segura.

## Quando NÃO acionar o fallback

O fallback não deve ser acionado quando:

1. A resposta estiver claramente sustentada pelo contexto recuperado.
2. Faltar apenas uma informação simples do aluno que possa ser perguntada antes de responder.
3. O chatbot conseguir orientar o procedimento completo com fonte oficial.
## Identificação do setor responsável

Antes de gerar o e-mail, o chatbot deve identificar qual setor é o mais adequado para receber a solicitação.

### Exemplos iniciais

- Requerimentos acadêmicos → SecGrad
- Estágio → SecGrad
- Questões pedagógicas específicas → NEAP
- Pós-graduação → Secretaria de Pós-Graduação

## Regra

Se o chatbot não conseguir identificar o setor com segurança, ele não deve inventar.

Nesse caso, deve informar que não conseguiu determinar o setor responsável com segurança e sugerir encaminhamento para a SecGrad como ponto inicial de orientação.