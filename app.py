import streamlit as st

from utils.validation import validate_required_answers
from ui.result_actions import generate_and_store_result
from ui.result_view import render_result_section
from ui.questionnaire import render_questionnaire, build_active_question_flow
from ui.layout import apply_custom_styles, render_start_screen
from utils.session import (
    initialize_session_state,
    remove_inactive_subanswers,
    clear_outdated_result_if_answers_changed,
)


def main():
    """
    Executa o fluxo principal da aplicação.

    O fluxo é dividido em:
    - configuração da página;
    - inicialização da sessão;
    - tela inicial;
    - questionário;
    - validação;
    - geração do resultado;
    - exibição do perfil final e da justificativa.
    """

    st.set_page_config(
        page_title="Classificação do Perfil do Investidor",
        page_icon="📊",
        layout="centered",
    )

    apply_custom_styles()
    initialize_session_state()

    if not st.session_state.app_started:
        render_start_screen()
        return

    if not st.session_state.questionnaire_finished:
        all_active_subquestion_ids = render_questionnaire()

        remove_inactive_subanswers(all_active_subquestion_ids)
        clear_outdated_result_if_answers_changed()

        return

    _, all_active_subquestion_ids = build_active_question_flow()

    remove_inactive_subanswers(all_active_subquestion_ids)

    validation_result = validate_required_answers(
        answers=st.session_state.answers,
        subanswers=st.session_state.subanswers,
        active_subquestion_ids=all_active_subquestion_ids,
    )

    clear_outdated_result_if_answers_changed()

    if not validation_result["is_valid"]:
        st.error(
            "Não foi possível gerar o resultado porque ainda existem respostas "
            "obrigatórias pendentes."
        )
        return

    if st.session_state.classification_result is None:
        generate_and_store_result()

    render_result_section()


if __name__ == "__main__":
    main()