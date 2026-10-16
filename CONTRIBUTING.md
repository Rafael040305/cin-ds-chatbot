# Guia de Contribuição — SecGrad AI

Este documento estabelece o fluxo de trabalho e os padrões de colaboração adotados pela equipe para o desenvolvimento do projeto.

---

## 1. Fluxo de Trabalho Git (Git Flow)

Para manter a branch principal estável e auditável:
* **Sem commits diretos na `main`:** Todo desenvolvimento deve ocorrer em branches temáticas.
* **Nomenclatura de Branches:**
  * `feat/<nome>`: Novas funcionalidades (ex: `feat/batch-ingestion`, `feat/chat-interface`).
  * `fix/<nome>`: Correção de bugs.
  * `docs/<nome>`: Documentação, guias ou slides.

---

## 2. Padrão de Commits Semânticos

As mensagens de commit devem seguir a convenção:
* `feat:` Novas funcionalidades.
* `fix:` Correções de bugs.
* `docs:` Documentação e instruções.
* `test:` Suítes de testes e QA.

---

## 3. Pull Requests e Revisão de Código

1. Ao concluir uma entrega, abra um Pull Request (PR) apontando para a branch `main`.
2. Preencha a descrição contendo o resumo das alterações, instruções de teste e dependências.
3. Todo PR exige revisão e validação antes do merge definitivo.
4. Após o merge, remova a branch remota para manter o repositório organizado.

---

## 4. Divisão de Papéis da Equipe

* **Rafael Ramos:** IA, embeddings, fatiamento e microsserviço RAG (`ai-service`).
* **Eric:** Front-end, interface de usuário e suíte de benchmark/QA.
* **Ricardo:** Engenharia de dados, catálogo de metadados e curadoria das normas da SecGrad.
* **Victor:** Back-end, orquestração de rotas e autenticação.