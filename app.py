# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa as perguntas principais cadastradas na Etapa 4.
from data.questions import get_questions_by_block

# Importa a função que identifica quais subperguntas devem ser ativadas.
# Essa função foi criada na Etapa 5, dentro de data/subquestions.py.
from data.subquestions import get_active_subquestions


# -------------------------------------------------------------------
# Configuração geral da página
# -------------------------------------------------------------------
#
# Define título da aba do navegador, ícone e layout da aplicação.
# Esta configuração precisa aparecer antes dos demais elementos visuais do Streamlit.

st.set_page_config(
    page_title="Classificação do Perfil do Investidor",
    page_icon="📊",
    layout="centered"
)


# -------------------------------------------------------------------
# Inicialização do estado da sessão
# -------------------------------------------------------------------
#
# O Streamlit recarrega o script a cada interação do usuário.
# Por isso, usamos st.session_state para manter respostas, subrespostas
# e controles internos entre um clique e outro.

if "answers" not in st.session_state:
    # Guarda as respostas das 9 perguntas principais.
    # Exemplo: {"P1": 2, "P2": 3}
    st.session_state.answers = {}

if "subanswers" not in st.session_state:
    # Guarda as respostas das subperguntas condicionais.
    # Exemplo: {"4A": 1, "4B": 2}
    st.session_state.subanswers = {}

if "reset_counter" not in st.session_state:
    # Contador usado para recriar os campos de resposta quando limpamos o formulário.
    # Isso evita que o Streamlit mantenha marcações antigas nos st.radio.
    st.session_state.reset_counter = 0


# -------------------------------------------------------------------
# Função auxiliar para descobrir o índice selecionado
# -------------------------------------------------------------------
#
# O st.radio precisa receber um índice numérico.
# Como nossas respostas são salvas pelo id da alternativa, esta função
# converte o id salvo para o índice correspondente na lista de opções.

def get_selected_index(radio_options, current_answer_id):
    """
    Retorna o índice da alternativa previamente selecionada.

    Parâmetros:
    - radio_options: lista de opções exibidas no st.radio.
    - current_answer_id: id da alternativa salva no session_state.

    Se ainda não existir resposta, retorna 0, que representa a opção vazia.
    """

    if current_answer_id is None:
        return 0

    for index, option in enumerate(radio_options):
        if option is not None and option["id"] == current_answer_id:
            return index

    return 0


# -------------------------------------------------------------------
# Função auxiliar para exibir uma pergunta principal
# -------------------------------------------------------------------
#
# Esta função recebe uma pergunta cadastrada em data/questions.py,
# exibe suas alternativas e armazena a resposta escolhida.

def render_question(question):
    """
    Exibe uma pergunta principal na tela e armazena a resposta.

    Retorna:
    - o id da alternativa selecionada;
    - None, caso nenhuma alternativa tenha sido selecionada.
    """

    question_id = question["id"]
    question_text = question["text"]
    options = question["options"]

    # Adiciona uma opção vazia no início.
    # Isso impede que a primeira alternativa real já venha marcada automaticamente.
    radio_options = [None] + options

    # Recupera a resposta já salva, se existir.
    current_answer_id = st.session_state.answers.get(question_id)

    # Define qual alternativa deve aparecer selecionada.
    selected_index = get_selected_index(radio_options, current_answer_id)

    # Exibe a pergunta principal como alternativa única.
    selected_option = st.radio(
        label=f"{question_id} — {question_text}",
        options=radio_options,
        index=selected_index,
        format_func=lambda option: "Selecione uma alternativa" if option is None else option["label"],
        key=f"radio_{question_id}_{st.session_state.reset_counter}"
    )

    # Se o usuário selecionou uma alternativa real, salvamos o id.
    if selected_option is not None:
        st.session_state.answers[question_id] = selected_option["id"]
        selected_option_id = selected_option["id"]

    # Se o usuário voltou para a opção vazia, removemos a resposta.
    else:
        if question_id in st.session_state.answers:
            del st.session_state.answers[question_id]

        selected_option_id = None

    # Área técnica expansível.
    # Ela ajuda a verificar se a pergunta está ligada corretamente à modelagem acadêmica.
    with st.expander("Detalhes técnicos desta pergunta"):
        st.write(f"**Eixo:** {question['axis']}")
        st.write(f"**Critério:** {question['criterion']}")
        st.write(f"**Função lógica:** {question['logical_function']}")
        st.write(f"**Peso lógico:** {question['logical_weight']}")

    return selected_option_id


# -------------------------------------------------------------------
# Função auxiliar para exibir uma subpergunta condicional
# -------------------------------------------------------------------
#
# Esta função recebe uma subpergunta ativada e exibe suas alternativas.
# As respostas das subperguntas são guardadas separadamente em subanswers.

def render_subquestion(subquestion):
    """
    Exibe uma subpergunta condicional e armazena a resposta.

    A subpergunta só chega até esta função se já tiver sido ativada
    pelo gatilho definido em data/subquestions.py.
    """

    subquestion_id = subquestion["id"]
    subquestion_text = subquestion["text"]
    options = subquestion["options"]

    # Opção vazia inicial para evitar marcação automática.
    radio_options = [None] + options

    # Recupera resposta anterior da subpergunta, se existir.
    current_answer_id = st.session_state.subanswers.get(subquestion_id)

    # Descobre o índice que deve aparecer selecionado.
    selected_index = get_selected_index(radio_options, current_answer_id)

    # Destaque visual para mostrar que não é pergunta principal,
    # mas sim uma pergunta complementar ativada por condição.
    st.markdown(f"**Subpergunta {subquestion_id}**")

    selected_option = st.radio(
        label=subquestion_text,
        options=radio_options,
        index=selected_index,
        format_func=lambda option: "Selecione uma alternativa" if option is None else option["label"],
        key=f"radio_sub_{subquestion_id}_{st.session_state.reset_counter}"
    )

    # Se o usuário respondeu, salvamos a subresposta.
    if selected_option is not None:
        st.session_state.subanswers[subquestion_id] = selected_option["id"]

    # Se voltou para a opção vazia, removemos a subresposta.
    else:
        if subquestion_id in st.session_state.subanswers:
            del st.session_state.subanswers[subquestion_id]

    # Detalhes técnicos da subpergunta.
    with st.expander(f"Detalhes técnicos da subpergunta {subquestion_id}"):
        st.write(f"**Pergunta de origem:** {subquestion['parent_question_id']}")
        st.write(f"**Função lógica:** {subquestion['logical_function']}")
        st.write(f"**Finalidade:** {subquestion['purpose']}")


# -------------------------------------------------------------------
# Função para exibir um bloco de perguntas
# -------------------------------------------------------------------
#
# Esta função exibe as perguntas principais de um bloco e,
# logo abaixo de cada uma, exibe as subperguntas ativadas.

def render_question_block(block_id):
    """
    Exibe todas as perguntas principais de um bloco.

    Para cada pergunta:
    1. exibe a pergunta principal;
    2. verifica se a resposta ativa subperguntas;
    3. exibe as subperguntas ativadas;
    4. retorna os ids das subperguntas ativas.
    """

    active_subquestion_ids = []

    for question in get_questions_by_block(block_id):
        # Exibe a pergunta principal e captura a alternativa escolhida.
        selected_option_id = render_question(question)

        # Se a pergunta principal foi respondida, verificamos subperguntas.
        if selected_option_id is not None:
            active_subquestions = get_active_subquestions(
                question["id"],
                selected_option_id
            )

            # Exibe cada subpergunta ativada.
            for subquestion in active_subquestions:
                active_subquestion_ids.append(subquestion["id"])
                render_subquestion(subquestion)

        st.divider()

    return active_subquestion_ids


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
    "Nesta etapa, o protótipo exibe as 9 perguntas principais e ativa subperguntas "
    "condicionais quando a resposta selecionada exige refinamento."
)

st.divider()


# -------------------------------------------------------------------
# Renderização dos blocos principais
# -------------------------------------------------------------------
#
# A lista abaixo será usada para controlar quais subperguntas estão ativas.
# Isso ajuda a limpar respostas antigas de subperguntas que deixaram de aparecer.

all_active_subquestion_ids = []


# Bloco 1 — Objetivos e tolerância ao risco
st.header("Bloco 1 — Objetivos e tolerância ao risco")

st.write(
    "Este bloco coleta informações sobre finalidade, horizonte temporal e "
    "tolerância ao risco. Posteriormente, essas respostas formarão o perfil preliminar."
)

all_active_subquestion_ids.extend(render_question_block("B1"))


# Bloco 2 — Compatibilidade financeira
st.header("Bloco 2 — Compatibilidade financeira")

st.write(
    "Este bloco coleta informações sobre necessidade futura de recursos, estabilidade "
    "de renda e reserva financeira. Posteriormente, essas respostas poderão limitar "
    "ou ajustar o perfil preliminar."
)

all_active_subquestion_ids.extend(render_question_block("B2"))


# Bloco 3 — Conhecimento e experiência
st.header("Bloco 3 — Conhecimento e experiência")

st.write(
    "Este bloco coleta informações sobre familiaridade, experiência prática e formação "
    "relacionada. Posteriormente, essas respostas serão usadas no refinamento do perfil."
)

all_active_subquestion_ids.extend(render_question_block("B3"))


# -------------------------------------------------------------------
# Limpeza automática de subrespostas inativas
# -------------------------------------------------------------------
#
# Se o usuário mudar uma resposta principal, uma subpergunta pode deixar de aparecer.
# Nesse caso, a resposta antiga da subpergunta não deve continuar armazenada.

for subquestion_id in list(st.session_state.subanswers.keys()):
    if subquestion_id not in all_active_subquestion_ids:
        del st.session_state.subanswers[subquestion_id]


# -------------------------------------------------------------------
# Visualização temporária das respostas
# -------------------------------------------------------------------
#
# Esta seção é apenas para desenvolvimento.
# Ela ajuda a conferir se as respostas principais e condicionais estão sendo salvas.

st.header("Respostas registradas até o momento")

st.subheader("Perguntas principais")

if st.session_state.answers:
    st.write(st.session_state.answers)
else:
    st.write("Nenhuma resposta principal registrada ainda.")

st.subheader("Subperguntas condicionais")

if st.session_state.subanswers:
    st.write(st.session_state.subanswers)
else:
    st.write("Nenhuma subpergunta condicional registrada ainda.")


# -------------------------------------------------------------------
# Botão temporário de limpeza
# -------------------------------------------------------------------
#
# Este botão limpa respostas principais, subrespostas e campos visuais.
# Ele será reaproveitado futuramente como base da função "Nova simulação".

if st.button("Limpar respostas"):
    # Limpa respostas principais.
    st.session_state.answers = {}

    # Limpa respostas das subperguntas.
    st.session_state.subanswers = {}

    # Incrementa o contador para recriar os campos radio.
    st.session_state.reset_counter += 1

    # Remove chaves antigas dos radios principais e condicionais.
    for key in list(st.session_state.keys()):
        if key.startswith("radio_"):
            del st.session_state[key]

    # Recarrega a aplicação já com os campos limpos.
    st.rerun()