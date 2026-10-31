import requests

NESTJS_API_URL = "http://localhost:3000/api/v1/conversa"

def enviar_pergunta(prompt: str, curso: str, perfil: str):
    """
    Envia a pergunta do aluno para a rota pública do NestJS e retorna a resposta com fontes.
    """
    payload = {
        "question": prompt,
        "curso": curso,
        "perfil": perfil
    }
    
    try:
        response = requests.post(NESTJS_API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Retorna o texto da resposta e a lista de fontes tratadas
            return {
                "sucesso": True,
                "resposta": data.get("answer") or data.get("response") or "Sem resposta gerada.",
                "fontes": data.get("sources", [])
            }
        else:
            return {
                "sucesso": False,
                "erro": f"Erro HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": f"Falha de ligação ao servidor backend: {str(e)}"
        }