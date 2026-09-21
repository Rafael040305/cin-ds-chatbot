import streamlit as st
import pandas as pd
import time

# -----------------------------------------------------------------------------
# Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Assistente - SecGrad CIn",
    page_icon="cin_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Função para Carregar a Planilha de Testes QA (Cache para performance)
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_planilha_qa():
    try:
        df = pd.read_excel('Planilha_QA_Benchmark_Sprint1.xlsx', sheet_name='Benchmark QA - Sprint 1', skiprows=3)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha de testes: {e}")
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
                    st.markdown(f"- **{src['documento']}** (Pág. {src['pagina']})")
                    st.caption(f'"{src["trecho"]}"')

# -----------------------------------------------------------------------------
# Processamento de Entrada (Caixa de Texto ou Seleção via Callback)
# -----------------------------------------------------------------------------
prompt_input = st.chat_input("Digite a sua dúvida (ex: Como solicito dispensa de disciplina?)")

# Verifica se há uma pergunta vinda do caixa de texto ou da seleção da planilha
prompt = prompt_input or st.session_state.get("pergunta_pendente")

if prompt:
    # Reseta a pergunta pendente para não re-executar no próximo ciclo
    st.session_state.pergunta_pendente = None

    # 1. Adiciona a mensagem do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Busca na Planilha a resposta esperada correspondente (Simulação de RAG)
    resposta_texto = ""
    fontes = []

    if df_qa is not None and prompt in df_qa["Pergunta do Aluno (Input)"].values:
        linha = df_qa[df_qa["Pergunta do Aluno (Input)"] == prompt].iloc[0]
        resposta_texto = f"**[Resposta Mock da Planilha - Teste #{linha['ID']}]:**\n\n{linha['Resposta Esperada / Comportamento']}"
        fontes = [{
            "documento": str(linha['Fonte Esperada (Documento / Seção)']),
            "pagina": 1,
            "trecho": f"Conteúdo de referência mapeado na planilha de QA para o assunto '{linha['Categoria / Assunto']}'."
        }]
    else:
        resposta_texto = f"Para orientações sobre **{prompt}** no curso de {curso}, consulte os requerimentos padrão da SecGrad."
        fontes = [{"documento": "normas_gerais_graduacao.pdf", "pagina": 1, "trecho": "Consulte o manual do aluno para procedimentos administrativos."}]

    # 3. Exibe a resposta do assistente
    with st.chat_message("assistant", avatar="cin_logo.png"):
        message_placeholder = st.empty()
        with st.spinner("A consultar resoluções da SecGrad..."):
            time.sleep(1)
            message_placeholder.markdown(resposta_texto)
            with st.expander("📄 Fontes e Trechos Utilizados"):
                for src in fontes:
                    st.markdown(f"- **{src['documento']}** (Pág. {src['pagina']})")
                    st.caption(f'"{src["trecho"]}"')

    # 4. Guarda a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto, "sources": fontes})
    st.rerun() 