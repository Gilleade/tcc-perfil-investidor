# Importa o Streamlit para renderizar elementos visuais.
import streamlit as st

# Importa perguntas principais e subperguntas.
from data.questions import get_questions_by_block
from data.subquestions import get_active_subquestions

# Importa a renderização individual de perguntas.
from ui.question_blocks import render_question, render_subquestion


BLOCK_ORDER = ["B1", "B2", "B3"]

BLOCK_TITLES = {
    "B1": "Objetivos e tolerância ao risco",
    "B2": "Compatibilidade financeira",
    "B3": "Conhecimento e experiência",
}


def build_active_question_flow():
    """
    Monta o fluxo sequencial de perguntas e subperguntas ativas.

    As perguntas principais sempre entram no fluxo.
    As subperguntas entram apenas quando a resposta da pergunta principal
    ativa seu gatilho.

    Retorno:
    - flow: lista de itens renderizáveis;
    - active_subquestion_ids: lista de subperguntas ativas.
    """

    flow = []
    active_subquestion_ids = []

    for block_id in BLOCK_ORDER:
        for question in get_questions_by_block(block_id):
            flow.append(
                {
                    "type": "question",
                    "id": question["id"],
                    "block_id": block_id,
                    "data": question,
                }
            )

            selected_option_id = st.session_state.answers.get(question["id"])

            if selected_option_id is not None:
                active_subquestions = get_active_subquestions(
                    question["id"],
                    selected_option_id,
                )

                for subquestion in active_subquestions:
                    active_subquestion_ids.append(subquestion["id"])

                    flow.append(
                        {
                            "type": "subquestion",
                            "id": subquestion["id"],
                            "block_id": block_id,
                            "data": subquestion,
                        }
                    )

    return flow, active_subquestion_ids


def is_current_item_answered(item):
    """
    Verifica se a pergunta ou subpergunta atual já foi respondida.
    """

    item_id = item["id"]

    if item["type"] == "question":
        return item_id in st.session_state.answers

    return item_id in st.session_state.subanswers


def render_navigation_buttons(current_index, total_items, current_item_answered):
    """
    Renderiza botões de navegação do fluxo sequencial.
    """

    previous_col, next_col = st.columns(2)

    with previous_col:
        if st.button(
            "Voltar",
            disabled=current_index == 0,
            width="stretch",
        ):
            st.session_state.current_flow_index = max(0, current_index - 1)
            st.session_state.questionnaire_finished = False
            st.session_state.classification_result = None
            st.session_state.justification_result = None
            st.session_state.result_signature = None
            st.rerun()

    with next_col:
        is_last_item = current_index >= total_items - 1
        button_label = "Finalizar" if is_last_item else "Próximo"

        if st.button(
            button_label,
            disabled=not current_item_answered,
            type="primary",
            width="stretch",
        ):
            if is_last_item:
                st.session_state.questionnaire_finished = True
                st.session_state.classification_result = None
                st.session_state.justification_result = None
                st.session_state.result_signature = None
            else:
                st.session_state.current_flow_index = current_index + 1

            st.rerun()


def render_questionnaire():
    """
    Renderiza o questionário em formato sequencial.

    Em vez de mostrar todos os blocos ao mesmo tempo, exibe apenas
    uma pergunta ou subpergunta por vez.

    Retorno:
    - lista com ids das subperguntas condicionais ativas.
    """

    flow, active_subquestion_ids = build_active_question_flow()

    if not flow:
        return active_subquestion_ids

    # Garante que o índice atual nunca ultrapasse o tamanho do fluxo.
    if st.session_state.current_flow_index >= len(flow):
        st.session_state.current_flow_index = len(flow) - 1

    current_index = st.session_state.current_flow_index
    current_item = flow[current_index]

    block_id = current_item["block_id"]
    block_title = BLOCK_TITLES.get(block_id, "Questionário")

    st.header(block_title)

    progress_value = (current_index + 1) / len(flow)

    st.progress(progress_value)

    st.caption(
        f"Pergunta {current_index + 1} de {len(flow)}"
    )

    st.divider()

    if current_item["type"] == "question":
        render_question(current_item["data"])
    else:
        render_subquestion(current_item["data"])

    st.divider()

    current_item_answered = is_current_item_answered(current_item)

    render_navigation_buttons(
        current_index=current_index,
        total_items=len(flow),
        current_item_answered=current_item_answered,
    )

    return active_subquestion_ids