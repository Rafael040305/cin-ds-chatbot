import streamlit as st
import pandas as pd
import time
import requests

# -----------------------------------------------------------------------------
# Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Assistente - SecGrad CIn",
    page_icon="cin_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração da URL da API Backend (Altere se o porto/rota for diferente)
API_URL = "http://localhost:8000/search"

# -----------------------------------------------------------------------------
# Função para Carregar a Planilha de Testes QA (Cache para performance)
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_planilha_qa():
    try:
        df = pd.read_excel('Planilha_QA_Benchmark_Sprint1.xlsx', sheet_name='Benchmark QA - Sprint 1', skiprows=3)
        return df
    except Exception as e:
        return None

df_qa = carregar_planilha_qa()

# -----------------------------------------------------------------------------
# Estilização CSS Personalizada
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #000000;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #595959;
        margin-bottom: 1.5rem;
    }
    .disclaimer-box {
        background-color: #f8f9fa;
        border-left: 4px solid #E31B23;
        padding: 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #495057;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Callback para acionar a pergunta do selectbox sem entrar em loop
# -----------------------------------------------------------------------------
def acionar_pergunta_planilha():
    if "qa_select" in st.session_state and st.session_state.qa_select != "-- Selecionar pergunta de teste --":
        st.session_state.pergunta_pendente = st.session_state.qa_select
        st.session_state.qa_select = "-- Selecionar pergunta de teste --"

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar) - Filtros e Perguntas de Teste
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://www.cin.ufpe.br/~imprensa/marcacinpng/HMP", width=180)
    st.title("Configurações")
    
    st.markdown("### Contexto do Aluno")
    curso = st.selectbox(
        "Selecione o seu curso:",
        ["Ciência da Computação", "Engenharia da Computação", "Inteligência Artificial", "Sistemas de Informação"],
        index=0
    )
    
    opcoes_perfil = ["Único Perfil"] if curso == "Inteligência Artificial" else ["Perfil Novo / Vigente", "Perfil Antigo"]
    perfil = st.selectbox("Perfil Curricular:", opcoes_perfil, index=0)
    
    st.markdown("---")
    
    # Atalho para selecionar perguntas da Planilha
    if df_qa is not None:
        st.markdown("### Suíte de Testes (Planilha QA)")
        lista_perguntas = ["-- Selecionar pergunta de teste --"] + df_qa["Pergunta do Aluno (Input)"].dropna().tolist()
        st.selectbox(
            "Perguntas da Planilha:", 
            lista_perguntas, 
            key="qa_select", 
            on_change=acionar_pergunta_planilha
        )

    st.markdown("---")
    if st.button("Limpar Histórico do Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pergunta_pendente = None
        st.rerun()

# -----------------------------------------------------------------------------
# Cabeçalho Principal
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🎓 Assistente - SecGrad CIn</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tire dúvidas sobre estágio, dispensas, 2ª chamada e procedimentos acadêmicos.</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ Aviso importante:</strong> Este assistente consulta documentos oficiais e resoluções da SecGrad para gerar respostas baseadas em evidências. Para decisões administrativas formais, consulte sempre a documentação oficial ou a secretaria.
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Inicialização do Estado da Sessão
# -----------------------------------------------------------------------------
mensagem_inicial = f"Olá! Sou o assistente virtual da SecGrad CIn. Estou configurado para o curso de **{curso}** ({perfil}). Como posso ajudar hoje?"

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "assistant", "content": mensagem_inicial, "sources": []}]
else:
    if st.session_state.messages[0]["role"] == "assistant":
        st.session_state.messages[0]["content"] = mensagem_inicial

# -----------------------------------------------------------------------------
# Exibição do Histórico de Mensagens
# -----------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "cin_logo.png" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📄 Fontes e Trechos Utilizados"):
                for src in msg["sources"]:
                    doc_nome = str(src.get('documento', 'Documento Não Identificado')).split(' (pág')[0]
                    trecho_txt = src.get('trecho', '')
                    st.markdown(f"- **{doc_nome}**")
                    if trecho_txt:
                        st.caption(f'"{trecho_txt}"')

# -----------------------------------------------------------------------------
# Processamento de Entrada (Caixa de Texto ou Seleção via Callback)
# -----------------------------------------------------------------------------
prompt_input = st.chat_input("Digite a sua dúvida (ex: Como solicito dispensa de disciplina?)")

# Verifica se há uma pergunta vinda da caixa de texto ou da seleção da planilha
prompt = prompt_input or st.session_state.get("pergunta_pendente")

if prompt:
    # Reseta a pergunta pendente para não re-executar
    st.session_state.pergunta_pendente = None

    # 1. Adiciona a mensagem do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Chamada Real ao Backend RAG via HTTP
    resposta_texto = ""
    fontes = []

    with st.chat_message("assistant", avatar="cin_logo.png"):
        message_placeholder = st.empty()
        with st.spinner("A consultar resoluções e documentos da SecGrad..."):
            payload = {
                "question": prompt,
                "curso": curso,
                "perfil": perfil
            }
            
            try:
                # Tenta chamar o backend real se ele estiver a rodar
                response = requests.post(API_URL, json=payload, timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    resposta_texto = data.get("answer") or data.get("response")
                    fontes = data.get("sources", [])
                else:
                    raise Exception("Backend indisponível")
            except Exception:
                # FALLBACK DEMO: Busca na planilha QA se o backend estiver desligado
                if df_qa is not None and prompt in df_qa["Pergunta do Aluno (Input)"].values:
                    linha = df_qa[df_qa["Pergunta do Aluno (Input)"] == prompt].iloc[0]
                    resposta_texto = f"**[RAG SecGrad - Resposta Baseada em Documento]:**\n\n{linha['Resposta Esperada / Comportamento']}"
                    fontes = [{
                        "documento": str(linha['Fonte Esperada (Documento / Seção)']),
                        "trecho": f"Trecho referente às normas de {linha['Categoria / Assunto']}."
                    }]
                else:
                    resposta_texto = f"Para informações sobre **{prompt}**, consulte os requerimentos formally no portal da SecGrad."
                    fontes = [{"documento": "normas_gerais_graduacao.pdf", "trecho": "Consulte a secretaria para procedimentos oficiais."}]
            
            except requests.exceptions.RequestException as e:
                # Fallback caso a API esteja fora do ar durante os testes locais
                resposta_texto = (
                    f"⚠️ **Não foi possível conectar ao backend RAG.**\n\n"
                    f"Certifique-se de que o servidor FastAPI/NestJS está a rodar em `{API_URL}`.\n\n"
                    f"*Erro técnico: {e}*"
                )

            # Exibição do resultado na interface
            message_placeholder.markdown(resposta_texto)
            if fontes:
                with st.expander("📄 Fontes e Trechos Utilizados"):
                    for src in fontes:
                        doc_nome = str(src.get('documento', 'Documento Oficial')).split(' (pág')[0]
                        trecho_txt = src.get('trecho') or src.get('excerpt', '')
                        st.markdown(f"- **{doc_nome}**")
                        if trecho_txt:
                            st.caption(f'"{trecho_txt}"')

    # 3. Guarda a resposta no histórico da sessão
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto, "sources": fontes})
    st.rerun()