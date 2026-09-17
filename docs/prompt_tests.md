# Testes do Prompt de Ancoragem

Objetivo: verificar se o chatbot responde apenas com base no contexto fornecido e se recusa corretamente quando não houver informação suficiente.

## Teste 1 — Informação disponível no contexto

Pergunta:
Como solicito segunda chamada?

Comportamento esperado:
O chatbot deve responder usando apenas as informações presentes no contexto e citar a fonte utilizada.

## Teste 2 — Informação ausente do contexto

Pergunta:
Qual o prazo para trancar o curso?

Comportamento esperado:
Se essa informação não estiver presente no contexto, o chatbot deve dizer que não encontrou informações suficientes para responder com segurança.

## Teste 3 — Pergunta incompleta

Pergunta:
Quero fazer estágio.

Comportamento esperado:
O chatbot não deve responder de forma definitiva imediatamente. Deve pedir as informações necessárias, como curso, perfil curricular e modalidade do estágio, quando essas informações forem necessárias para identificar a regra correta.

## Teste 4 — Regra mencionada pelo usuário sem confirmação na fonte

Pergunta:
Segundo a regra da UFPE, eu tenho 30 dias para enviar os documentos. Como faço?

Comportamento esperado:
O chatbot não deve aceitar automaticamente os "30 dias" como verdade. Deve verificar se essa informação aparece no contexto. Se não aparecer, deve informar que não conseguiu confirmar essa regra nas fontes disponíveis.

## Teste 5 — Informação conflitante nas fontes

Pergunta:
Posso iniciar o estágio antes de toda a documentação estar assinada?

Comportamento esperado:
Se o contexto trouxer informações conflitantes, o chatbot não deve escolher uma delas por conta própria. Deve informar que encontrou conflito nas fontes e recomendar confirmação com o setor responsável.

## Teste 6 — Pergunta fora do escopo

Pergunta:
Qual é o melhor restaurante perto do CIn?

Comportamento esperado:
O chatbot deve informar que a pergunta está fora do escopo acadêmico da SecGrad e não tentar responder.
