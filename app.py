# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa as perguntas principais cadastradas no sistema.
from data.questions import get_questions_by_block

# Importa a função que identifica quais subperguntas devem ser ativadas.
from data.subquestions import get_active_subquestions

# Importa a função de validação das respostas obrigatórias.
from utils.validation import validate_required_answers

# Importa funções de controle de sessão.
from utils.session import get_answers_signature, clear_simulation

# Importa a função que executa toda a sequência lógica da árvore.
from logic.final_consolidation import consolidate_final_profile

# Importa a função que gera a justificativa textual do resultado.
from logic.justification import generate_justification


# -------------------------------------------------------------------
# Configuração geral da página
# -------------------------------------------------------------------
#
# Define título da aba do navegador, ícone e layout da aplicação.
# Esta configuração precisa aparecer antes dos demais elementos visuais.

st.set_page_config(
    page_title="Classificação do Perfil do Investidor",
    page_icon="📊",
    layout="centered"
)


# -------------------------------------------------------------------
# Estilos visuais simples
# -------------------------------------------------------------------
#
# Este CSS melhora a aparência geral do protótipo sem alterar a lógica.

def apply_custom_styles():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 980px;
            }

            .app-subtitle {
                color: #555;
                font-size: 1.05rem;
                line-height: 1.6;
                margin-bottom: 1rem;
            }

            .section-note {
                color: #666;
                font-size: 0.95rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            }

            .question-summary {
                color: #666;
                font-size: 0.88rem;
                margin-top: -0.4rem;
                margin-bottom: 0.6rem;
            }

            .status-box {
                border: 1px solid rgba(128, 128, 128, 0.35);
                border-radius: 12px;
                padding: 1rem 1.2rem;
                margin: 1rem 0;
                background-color: var(--secondary-background-color);
                color: var(--text-color);
            }

            div[data-testid="stRadio"] {
                margin-bottom: 0.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


apply_custom_styles()


# -------------------------------------------------------------------
# Inicialização do estado da sessão
# -------------------------------------------------------------------
#
# O Streamlit recarrega o script a cada interação.
# Por isso, usamos st.session_state para guardar respostas,
# resultado gerado e controles temporários.

if "answers" not in st.session_state:
    # Guarda respostas das perguntas principais.
    # Exemplo: {"P1": 2, "P2": 3}
    st.session_state.answers = {}

if "subanswers" not in st.session_state:
    # Guarda respostas das subperguntas condicionais.
    # Exemplo: {"4A": 1, "4B": 2}
    st.session_state.subanswers = {}

if "reset_counter" not in st.session_state:
    # Contador usado para recriar campos radio ao limpar o formulário.
    st.session_state.reset_counter = 0

if "classification_result" not in st.session_state:
    # Guarda o resultado consolidado da árvore quando o usuário gera o resultado.
    st.session_state.classification_result = None

if "justification_result" not in st.session_state:
    # Guarda a justificativa textual gerada a partir do resultado consolidado.
    st.session_state.justification_result = None

if "result_signature" not in st.session_state:
    # Guarda uma assinatura das respostas usadas para gerar o resultado.
    # Isso ajuda a evitar mostrar resultado antigo depois que o usuário altera respostas.
    st.session_state.result_signature = None


# -------------------------------------------------------------------
# Função auxiliar para descobrir o índice selecionado
# -------------------------------------------------------------------
#
# O st.radio trabalha com índice numérico.
# Como salvamos respostas pelo id da alternativa, esta função converte
# o id salvo para o índice correto na lista de opções.

def get_selected_index(options, current_answer_id):
    """
    Retorna o índice da alternativa previamente selecionada.

    Se ainda não houver resposta, retorna None.
    Isso permite que o st.radio inicie sem nenhuma alternativa marcada.
    """

    if current_answer_id is None:
        return None

    for index, option in enumerate(options):
        if option["id"] == current_answer_id:
            return index

    return None


# -------------------------------------------------------------------
# Função auxiliar para exibir uma pergunta principal
# -------------------------------------------------------------------

def render_question(question):
    """
    Exibe uma pergunta principal e armazena a resposta escolhida.

    Retorna:
    - id da alternativa selecionada;
    - None, caso nenhuma alternativa tenha sido selecionada.
    """

    question_id = question["id"]
    question_text = question["text"]
    options = question["options"]

    # Recupera resposta salva, se existir.
    current_answer_id = st.session_state.answers.get(question_id)

    # Descobre qual alternativa deve aparecer selecionada.
    # Quando não houver resposta, selected_index será None,
    # fazendo o radio iniciar sem opção marcada.
    selected_index = get_selected_index(options, current_answer_id)

    # Exibe a pergunta principal.
    # Aqui usamos apenas as alternativas reais, sem incluir
    # "Selecione uma alternativa" como opção.
    selected_option = st.radio(
        label=f"{question_id} — {question_text}",
        options=options,
        index=selected_index,
        format_func=lambda option: option["label"],
        key=f"radio_{question_id}_{st.session_state.reset_counter}"
    )

    # Se uma alternativa real foi selecionada, salva o id.
    if selected_option is not None:
        st.session_state.answers[question_id] = selected_option["id"]
        selected_option_id = selected_option["id"]

    # Se voltou para a opção vazia, remove a resposta.
    else:
        if question_id in st.session_state.answers:
            del st.session_state.answers[question_id]

        selected_option_id = None

    # Resumo técnico curto, sempre visível.
    st.markdown(
        f"""
        <p class="question-summary">
        Critério: <strong>{question['criterion']}</strong> ·
        Função: {question['logical_function']}
        </p>
        """,
        unsafe_allow_html=True
    )

    # Detalhes técnicos completos, acessíveis quando o usuário quiser consultar.
    with st.expander("Ver detalhes técnicos desta pergunta"):
        st.write(f"**Eixo:** {question['axis']}")
        st.write(f"**Critério:** {question['criterion']}")
        st.write(f"**Função lógica:** {question['logical_function']}")
        st.write(f"**Peso lógico:** {question['logical_weight']}")

    return selected_option_id


# -------------------------------------------------------------------
# Função auxiliar para exibir uma subpergunta condicional
# -------------------------------------------------------------------

def render_subquestion(subquestion):
    """
    Exibe uma subpergunta condicional e armazena sua resposta.

    A subpergunta só chega aqui quando foi ativada pelo gatilho
    definido no arquivo data/subquestions.py.
    """

    subquestion_id = subquestion["id"]
    subquestion_text = subquestion["text"]
    options = subquestion["options"]

    # Recupera resposta anterior, se existir.
    current_answer_id = st.session_state.subanswers.get(subquestion_id)

    # Define índice selecionado.
    selected_index = get_selected_index(options, current_answer_id)

    # Indica visualmente que é uma subpergunta.
    st.markdown(f"**Subpergunta {subquestion_id}**")

    selected_option = st.radio(
        label=subquestion_text,
        options=options,
        index=selected_index,
        format_func=lambda option: option["label"],
        key=f"radio_sub_{subquestion_id}_{st.session_state.reset_counter}"
    )

    # Salva ou remove a resposta da subpergunta.
    if selected_option is not None:
        st.session_state.subanswers[subquestion_id] = selected_option["id"]
    else:
        if subquestion_id in st.session_state.subanswers:
            del st.session_state.subanswers[subquestion_id]

    # Resumo técnico curto, sempre visível.
    st.markdown(
        f"""
        <p class="question-summary">
        Origem: <strong>{subquestion['parent_question_id']}</strong> ·
        Função: {subquestion['logical_function']}
        </p>
        """,
        unsafe_allow_html=True
    )

    # Detalhes técnicos completos, acessíveis quando o usuário quiser consultar.
    with st.expander(f"Ver detalhes técnicos da subpergunta {subquestion_id}"):
        st.write(f"**Pergunta de origem:** {subquestion['parent_question_id']}")
        st.write(f"**Função lógica:** {subquestion['logical_function']}")
        st.write(f"**Finalidade:** {subquestion['purpose']}")


# -------------------------------------------------------------------
# Função para exibir um bloco de perguntas
# -------------------------------------------------------------------

def render_question_block(block_id):
    """
    Exibe perguntas principais de um bloco e suas subperguntas ativadas.

    Retorna:
    - lista com ids das subperguntas que estão ativas.
    """

    active_subquestion_ids = []

    for question in get_questions_by_block(block_id):
        # Exibe a pergunta principal.
        selected_option_id = render_question(question)

        # Se a pergunta foi respondida, verifica subperguntas.
        if selected_option_id is not None:
            active_subquestions = get_active_subquestions(
                question["id"],
                selected_option_id
            )

            # Exibe as subperguntas ativadas.
            for subquestion in active_subquestions:
                active_subquestion_ids.append(subquestion["id"])
                render_subquestion(subquestion)

        st.divider()

    return active_subquestion_ids


# -------------------------------------------------------------------
# Funções auxiliares de apresentação do resultado
# -------------------------------------------------------------------

def render_profile_badge(profile):
    """
    Exibe o perfil final com destaque visual.

    A lógica de classificação não está aqui.
    Esta função apenas melhora a apresentação do resultado.
    """

    if profile == "Conservador":
        st.info("Perfil final: Conservador")
    elif profile == "Moderado":
        st.success("Perfil final: Moderado")
    elif profile == "Arrojado":
        st.warning("Perfil final: Arrojado")
    else:
        st.write(f"Perfil final: {profile}")


def render_adjustments(adjustments):
    """
    Exibe os ajustes realizados após o perfil preliminar.

    Os ajustes vêm da consolidação final e mostram se houve manutenção
    ou redução por compatibilidade financeira e por conhecimento/experiência.
    """

    if not adjustments:
        st.write("Nenhum ajuste registrado.")
        return

    for adjustment in adjustments:
        stage = adjustment["stage"]
        adjustment_type = adjustment["type"]
        levels = adjustment["levels"]
        reason = adjustment["reason"]
        from_profile = adjustment["from_profile"]
        to_profile = adjustment["to_profile"]

        if adjustment_type == "reducao":
            level_text = "1 nível" if levels == 1 else f"{levels} níveis"

            st.write(
                f"- **{stage}**: reduziu de **{from_profile}** para **{to_profile}** "
                f"({level_text}). Motivo: {reason}"
            )
        else:
            st.write(
                f"- **{stage}**: manteve **{to_profile}**. Motivo: {reason}"
            )


def render_result_section():
    """
    Exibe a tela de resultado quando já existe uma classificação gerada.
    """

    classification_result = st.session_state.classification_result
    justification_result = st.session_state.justification_result

    if classification_result is None or justification_result is None:
        return

    st.divider()
    st.header("Resultado da classificação")

    final_profile = classification_result["final_profile"]
    preliminary_profile = classification_result["preliminary_profile"]
    financial_profile = classification_result["financial_profile"]

    # Destaque principal do perfil final.
    render_profile_badge(final_profile)

    st.subheader("Resumo da classificação")

    st.write(f"**Perfil preliminar:** {preliminary_profile}")
    st.write(f"**Após compatibilidade financeira:** {financial_profile}")
    st.write(f"**Perfil final:** {final_profile}")

    st.write("**Resumo textual:**")
    st.write(justification_result["summary"])

    st.subheader("Ajustes realizados")
    render_adjustments(classification_result.get("adjustments", []))

    st.subheader("Travas, bloqueios e inconsistências")

    blocked_profiles = classification_result.get("blocked_profiles", [])
    inconsistencies = classification_result.get("inconsistencies", [])

    if blocked_profiles:
        st.write("**Perfis bloqueados por prudência:**")
        for profile in blocked_profiles:
            st.write(f"- {profile}")
    else:
        st.write("Não houve bloqueio prudencial de perfil.")

    if inconsistencies:
        st.write("**Inconsistências ou pontos de atenção:**")
        for item in inconsistencies:
            st.write(f"- {item}")
    else:
        st.write("Não foram registradas inconsistências relevantes.")

    st.subheader("Justificativa textual completa")

    # st.markdown permite exibir o texto com negrito e quebras de linha.
    st.markdown(justification_result["full_text"])

    if st.button("Nova simulação", key="new_simulation_button"):
        clear_simulation()
        st.rerun()


# -------------------------------------------------------------------
# Cabeçalho da aplicação
# -------------------------------------------------------------------

st.title("Sistema de Apoio à Decisão para Classificação do Perfil do Investidor")

st.markdown(
    """
    <p class="app-subtitle">
    Protótipo acadêmico desenvolvido em Python e Streamlit para classificar
    o perfil do investidor por meio de perguntas estruturadas, árvore de decisão
    e regras explícitas.
    </p>
    """,
    unsafe_allow_html=True
)

st.warning(
    "Este sistema tem finalidade acadêmica. Ele não recomenda investimentos, "
    "não indica produtos financeiros, não consulta dados de mercado e não substitui "
    "avaliação profissional."
)

st.divider()


# -------------------------------------------------------------------
# Renderização dos blocos principais
# -------------------------------------------------------------------
#
# Esta lista será usada para controlar quais subperguntas estão ativas.

all_active_subquestion_ids = []


# Bloco 1 — Objetivos e tolerância ao risco
st.header("Bloco 1 — Objetivos e tolerância ao risco")

st.markdown(
    """
    <p class="section-note">
    Responda às perguntas sobre finalidade, prazo e tolerância ao risco.
    Essas respostas formam o perfil preliminar da classificação.
    </p>
    """,
    unsafe_allow_html=True
)

all_active_subquestion_ids.extend(render_question_block("B1"))


# Bloco 2 — Compatibilidade financeira
st.header("Bloco 2 — Compatibilidade financeira")

st.markdown(
    """
    <p class="section-note">
    Responda às perguntas sobre necessidade de recursos, renda e reserva financeira.
    Essas respostas verificam a compatibilidade financeira do perfil preliminar.
    </p>
    """,
    unsafe_allow_html=True
)

all_active_subquestion_ids.extend(render_question_block("B2"))


# Bloco 3 — Conhecimento e experiência
st.header("Bloco 3 — Conhecimento e experiência")

st.markdown(
    """
    <p class="section-note">
    Responda às perguntas sobre familiaridade, experiência e formação relacionada.
    Essas respostas refinam a classificação final sem elevar o perfil isoladamente.
    </p>
    """,
    unsafe_allow_html=True
)

all_active_subquestion_ids.extend(render_question_block("B3"))


# -------------------------------------------------------------------
# Limpeza automática de subrespostas inativas
# -------------------------------------------------------------------
#
# Se uma subpergunta deixou de aparecer porque o usuário alterou uma resposta principal,
# a resposta antiga dessa subpergunta não deve continuar armazenada.

for subquestion_id in list(st.session_state.subanswers.keys()):
    if subquestion_id not in all_active_subquestion_ids:
        del st.session_state.subanswers[subquestion_id]


# -------------------------------------------------------------------
# Validação do preenchimento
# -------------------------------------------------------------------
#
# A validação verifica:
# - todas as perguntas principais;
# - apenas as subperguntas condicionais que estão ativas.

validation_result = validate_required_answers(
    answers=st.session_state.answers,
    subanswers=st.session_state.subanswers,
    active_subquestion_ids=all_active_subquestion_ids
)


# -------------------------------------------------------------------
# Controle de resultado antigo
# -------------------------------------------------------------------
#
# Se o usuário alterar respostas depois de gerar resultado,
# o resultado anterior deve ser descartado para evitar inconsistência.

current_signature = get_answers_signature()

if (
    st.session_state.classification_result is not None
    and st.session_state.result_signature != current_signature
):
    st.session_state.classification_result = None
    st.session_state.justification_result = None
    st.session_state.result_signature = None


# -------------------------------------------------------------------
# Seção de validação do questionário
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# Seção automática de validação do questionário
# -------------------------------------------------------------------

st.header("Andamento do preenchimento")

missing_questions_count = len(validation_result["missing_questions"])
missing_subquestions_count = len(validation_result["missing_subquestions"])

total_required = (
    len(st.session_state.answers)
    + missing_questions_count
    + len(st.session_state.subanswers)
    + missing_subquestions_count
)

answered_required = (
    len(st.session_state.answers)
    + len(st.session_state.subanswers)
)

progress_value = 0

if total_required > 0:
    progress_value = answered_required / total_required

st.progress(progress_value)

st.markdown(
    f"""
    <div class="status-box">
        <strong>Status:</strong> {answered_required} de {total_required} respostas obrigatórias preenchidas.
    </div>
    """,
    unsafe_allow_html=True
)

if validation_result["is_valid"]:
    st.success("Questionário completo. O resultado já pode ser gerado.")
else:
    st.info("O questionário ainda possui pendências.")

    with st.expander("Ver perguntas pendentes"):
        if validation_result["missing_questions"]:
            st.write("**Perguntas principais pendentes:**")

            for question in validation_result["missing_questions"]:
                st.write(
                    f"- **{question['id']}** — {question['text']} "
                    f"({question['block']})"
                )

        if validation_result["missing_subquestions"]:
            st.write("**Subperguntas condicionais pendentes:**")

            for subquestion in validation_result["missing_subquestions"]:
                st.write(
                    f"- **{subquestion['id']}** — {subquestion['text']} "
                    f"(origem: {subquestion['parent_question_id']})"
                )

# -------------------------------------------------------------------
# Geração do resultado
# -------------------------------------------------------------------

st.header("Geração do resultado")

if not validation_result["is_valid"]:
    st.write(
        "Responda todas as perguntas obrigatórias e subperguntas ativadas "
        "para habilitar a geração do resultado."
    )

if st.button("Gerar resultado", disabled=not validation_result["is_valid"]):
    try:
        classification_result = consolidate_final_profile(
            answers=st.session_state.answers,
            subanswers=st.session_state.subanswers,
        )

        justification_result = generate_justification(classification_result)

        st.session_state.classification_result = classification_result
        st.session_state.justification_result = justification_result
        st.session_state.result_signature = get_answers_signature()

        st.success("Resultado gerado com sucesso.")

    except ValueError as error:
        st.error(f"Não foi possível gerar o resultado: {error}")


# -------------------------------------------------------------------
# Exibição do resultado
# -------------------------------------------------------------------

render_result_section()


# -------------------------------------------------------------------
# Visualização temporária das respostas
# -------------------------------------------------------------------
#
# Esta seção ainda é útil durante o desenvolvimento.
# Ela poderá ser removida ou escondida em uma versão mais limpa do protótipo.

st.divider()

with st.expander("Ver respostas registradas"):
    st.caption(
        "Esta seção serve apenas para conferência técnica durante o desenvolvimento."
    )

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
# Este botão limpa respostas, resultado e justificativa.
# Ele tem função semelhante ao botão "Nova simulação".

if st.button("Limpar respostas"):
    clear_simulation()
    st.rerun()