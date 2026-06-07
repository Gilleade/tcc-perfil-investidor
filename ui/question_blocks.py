# Importa o Streamlit para renderizar perguntas e elementos visuais.
import streamlit as st

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
    # Usamos apenas alternativas reais, sem incluir
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

    # Se nenhuma alternativa estiver marcada, remove a resposta.
    else:
        if question_id in st.session_state.answers:
            del st.session_state.answers[question_id]

        selected_option_id = None

    return selected_option_id


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
