# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa a função que busca perguntas por bloco.
# Essa função foi criada na Etapa 4, dentro do arquivo data/questions.py.
from data.questions import get_questions_by_block


# Configuração geral da página no navegador.
# Essa configuração deve ficar no início do app Streamlit.
st.set_page_config(
    page_title="Classificação do Perfil do Investidor",
    page_icon="📊",
    layout="centered"
)


# -------------------------------------------------------------------
# Inicialização do estado da sessão
# -------------------------------------------------------------------
#
# O Streamlit executa o script novamente a cada interação do usuário.
# Por isso, usamos st.session_state para guardar informações entre interações.
#
# Aqui criamos um dicionário chamado "answers" para armazenar as respostas.
# Exemplo futuro:
# st.session_state.answers["P1"] = 2
#
# Isso significa que a pergunta P1 recebeu a alternativa de id 2.

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Contador usado para recriar os campos de resposta quando limpamos o formulário.
# Isso força o Streamlit a gerar novos st.radio sem reaproveitar seleções antigas.
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# -------------------------------------------------------------------
# Função auxiliar para exibir uma pergunta principal
# -------------------------------------------------------------------
#
# Esta função recebe uma pergunta cadastrada em data/questions.py
# e cria um campo de resposta do tipo radio no Streamlit.

def render_question(question):
    """
    Exibe uma pergunta principal na tela e armazena a resposta escolhida.

    Parâmetro:
    - question: dicionário com os dados da pergunta.

    O dicionário da pergunta contém:
    - id;
    - texto;
    - alternativas;
    - critério;
    - eixo;
    - função lógica.
    """

    question_id = question["id"]
    question_text = question["text"]
    options = question["options"]

    # Cria uma lista com uma opção vazia inicial.
    # Isso evita que o Streamlit já deixe a primeira alternativa marcada automaticamente.
    radio_options = [None] + options

    # Recupera resposta anterior, se existir.
    # Isso permite que a resposta continue marcada se a tela recarregar.
    current_answer_id = st.session_state.answers.get(question_id)

    # Define qual opção deve aparecer selecionada.
    # Se ainda não houver resposta, a opção selecionada será None.
    selected_index = 0

    if current_answer_id is not None:
        for index, option in enumerate(radio_options):
            if option is not None and option["id"] == current_answer_id:
                selected_index = index
                break

    # Exibe a pergunta na tela.
    selected_option = st.radio(
        label=f"{question_id} — {question_text}",
        options=radio_options,
        index=selected_index,
        format_func=lambda option: "Selecione uma alternativa" if option is None else option["label"],
        key=f"radio_{question_id}_{st.session_state.reset_counter}"
    )

    # Se o usuário selecionou uma alternativa real, armazenamos o id da resposta.
    if selected_option is not None:
        st.session_state.answers[question_id] = selected_option["id"]

    # Se o usuário voltou para a opção vazia, removemos a resposta armazenada.
    else:
        if question_id in st.session_state.answers:
            del st.session_state.answers[question_id]

    # Exibe uma pequena informação técnica para fins de desenvolvimento.
    # Essa informação ajuda a conferir se a pergunta está ligada ao eixo correto.
    with st.expander("Detalhes técnicos desta pergunta"):
        st.write(f"**Eixo:** {question['axis']}")
        st.write(f"**Critério:** {question['criterion']}")
        st.write(f"**Função lógica:** {question['logical_function']}")
        st.write(f"**Peso lógico:** {question['logical_weight']}")

    st.divider()


# -------------------------------------------------------------------
# Cabeçalho da aplicação
# -------------------------------------------------------------------

st.title("Sistema de Apoio à Decisão para Classificação do Perfil do Investidor")

st.write(
    "Este protótipo tem finalidade acadêmica e foi desenvolvido para apoiar a "
    "classificação do perfil do investidor com base em critérios estruturados."
)

st.warning(
    "Atenção: este sistema não recomenda investimentos, não indica produtos "
    "financeiros, não consulta dados de mercado e não substitui avaliação profissional."
)

st.info(
    "Nesta etapa, o protótipo apenas exibe as 9 perguntas principais e captura "
    "as respostas. O cálculo do perfil será implementado nas próximas etapas."
)

st.divider()


# -------------------------------------------------------------------
# Bloco 1 — Objetivos e tolerância ao risco
# -------------------------------------------------------------------
#
# Neste bloco entram as perguntas P1, P2 e P3.
# Elas formarão futuramente o perfil preliminar.

st.header("Bloco 1 — Objetivos e tolerância ao risco")

st.write(
    "Este bloco coleta informações sobre finalidade, horizonte temporal e "
    "tolerância ao risco. Posteriormente, essas respostas formarão o perfil preliminar."
)

for question in get_questions_by_block("B1"):
    render_question(question)


# -------------------------------------------------------------------
# Bloco 2 — Compatibilidade financeira
# -------------------------------------------------------------------
#
# Neste bloco entram as perguntas P4, P5 e P6.
# Elas serão usadas futuramente para verificar travas, reduções e compatibilidade financeira.

st.header("Bloco 2 — Compatibilidade financeira")

st.write(
    "Este bloco coleta informações sobre necessidade futura de recursos, estabilidade "
    "de renda e reserva financeira. Posteriormente, essas respostas poderão limitar "
    "ou ajustar o perfil preliminar."
)

for question in get_questions_by_block("B2"):
    render_question(question)


# -------------------------------------------------------------------
# Bloco 3 — Conhecimento e experiência
# -------------------------------------------------------------------
#
# Neste bloco entram as perguntas P7, P8 e P9.
# Elas serão usadas futuramente para confirmar ou reduzir a classificação final.

st.header("Bloco 3 — Conhecimento e experiência")

st.write(
    "Este bloco coleta informações sobre familiaridade, experiência prática e formação "
    "relacionada. Posteriormente, essas respostas serão usadas no refinamento do perfil."
)

for question in get_questions_by_block("B3"):
    render_question(question)


# -------------------------------------------------------------------
# Visualização temporária das respostas
# -------------------------------------------------------------------
#
# Esta seção é apenas para desenvolvimento.
# Ela mostra quais respostas já foram armazenadas no session_state.
# Em uma versão final mais limpa, isso poderá ser removido ou escondido.

st.header("Respostas registradas até o momento")

if st.session_state.answers:
    st.write(st.session_state.answers)
else:
    st.write("Nenhuma resposta registrada ainda.")


# -------------------------------------------------------------------
# Botão temporário de limpeza
# -------------------------------------------------------------------
#
# Este botão limpa todas as respostas registradas e recria os campos de seleção.
if st.button("Limpar respostas"):
    # Limpa o dicionário principal de respostas.
    st.session_state.answers = {}

    # Aumenta o contador para forçar o Streamlit a criar novos st.radio.
    st.session_state.reset_counter += 1

    # Remove chaves antigas dos radios, apenas para manter a sessão limpa.
    for key in list(st.session_state.keys()):
        if key.startswith("radio_"):
            del st.session_state[key]

    # Recarrega a aplicação.
    st.rerun()