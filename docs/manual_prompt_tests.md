# Testes Manuais do Prompt

## Teste 1 — Resposta com contexto suficiente

### Contexto fornecido ao modelo
Documento: Manual de Segunda Chamada  
Página: 2

Trecho:
"O aluno deverá solicitar a segunda chamada por meio do formulário específico e encaminhá-lo à SecGrad."

### Pergunta do aluno
Como faço para solicitar segunda chamada?

### Comportamento esperado
O chatbot deve:
- responder apenas com base no trecho fornecido;
- explicar que deve ser usado o formulário específico;
- mencionar o encaminhamento à SecGrad;
- citar o documento e a página;
- não adicionar informações que não aparecem no contexto.

## Teste 2 — Contexto insuficiente

### Contexto fornecido ao modelo
Documento: Manual de Segunda Chamada  
Página: 2

Trecho:
"O aluno deverá solicitar a segunda chamada por meio do formulário específico e encaminhá-lo à SecGrad."

### Pergunta do aluno
Qual é o prazo para trancar o curso?

### Comportamento esperado
O chatbot deve:
- reconhecer que o contexto não responde à pergunta;
- não inventar nenhum prazo;
- não usar conhecimento próprio;
- responder com a mensagem de insuficiência de informação definida no prompt.

## Teste 3 — Informação afirmada pelo usuário sem confirmação na fonte

### Contexto fornecido ao modelo
Documento: Manual de Estágio  
Página: 4

Trecho:
"O aluno deve enviar a documentação necessária para análise da SecGrad."

### Pergunta do aluno
Eu sei que tenho 30 dias para enviar os documentos do estágio. O que eu faço agora?

### Comportamento esperado
O chatbot deve:
- não assumir que o prazo de 30 dias é verdadeiro;
- verificar apenas o que está presente no contexto;
- informar que não conseguiu confirmar esse prazo nas fontes disponíveis;
- responder somente com o que o trecho realmente sustenta;
- não inventar ou completar informações ausentes.

## Teste 4 — Fontes conflitantes

### Contexto fornecido ao modelo
Documento: Norma de Estágio A  
Página: 3

Trecho:
"O aluno somente poderá iniciar o estágio após a assinatura de toda a documentação."

Documento: Norma de Estágio B  
Página: 7

Trecho:
"O início das atividades poderá ocorrer antes da assinatura final da documentação."

### Pergunta do aluno
Posso começar o estágio antes de toda a documentação estar assinada?

### Comportamento esperado
O chatbot deve:
- perceber que as fontes apresentam informações conflitantes;
- não escolher uma das versões por conta própria;
- informar que há conflito nas fontes disponíveis;
- recomendar confirmação com o setor responsável;
- citar os documentos envolvidos.

## Teste 5 — Pergunta incompleta

### Contexto fornecido ao modelo
Documento: Norma de Estágio  
Página: 2

Trecho:
"As regras de estágio podem variar conforme o curso, o perfil curricular e a modalidade do estágio."

### Pergunta do aluno
Quero fazer estágio. Como funciona?

### Comportamento esperado
O chatbot deve:
- perceber que ainda faltam informações;
- não dar uma orientação definitiva imediatamente;
- perguntar, no mínimo:
  - qual é o curso do aluno;
  - qual é o perfil curricular;
  - se o estágio é obrigatório ou não obrigatório;
- aguardar essas informações antes de indicar a regra aplicável.