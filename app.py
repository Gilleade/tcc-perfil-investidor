# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa a função de validação das respostas obrigatórias.
from utils.validation import validate_required_answers

# Importa a seção de geração do resultado.
from ui.result_actions import generate_and_store_result

# Importa a seção de resultado da interface.
from ui.result_view import render_result_section

# Importa a montagem completa dos blocos do questionário.
from ui.questionnaire import render_questionnaire, build_active_question_flow

# Importa elementos visuais gerais da aplicação.
from ui.layout import (
    apply_custom_styles,
    render_start_screen,
)

# Importa o Streamlit para acessar o estado da sessão.
from utils.session import (
    initialize_session_state,
    remove_inactive_subanswers,
    clear_outdated_result_if_answers_changed,
)


# -------------------------------------------------------------------
# Configuração geral da página
# -------------------------------------------------------------------
#
# Define título da aba do navegador, ícone e layout da aplicação.
# Esta configuração precisa aparecer antes dos demais elementos visuais.

def main():
    """
    Executa o fluxo principal da aplicação Streamlit.

    Esta função organiza:
    - configuração da página;
    - aplicação de estilos;
    - inicialização da sessão;
    - renderização do cabeçalho;
    - renderização do questionário;
    - validação;
    - geração do resultado;
    - exibição do resultado;
    - painel técnico;
    - limpeza da simulação.
    """

    st.set_page_config(
        page_title="Classificação do Perfil do Investidor",
        page_icon="📊",
        layout="centered"
    )

    apply_custom_styles()

    initialize_session_state()
    
    if not st.session_state.app_started:
        render_start_screen()
        return


        # -------------------------------------------------------------------
    # Tela do questionário ou tela de resultado
    # -------------------------------------------------------------------
    #
    # Quando o questionário ainda não foi finalizado, exibimos apenas
    # uma pergunta por vez.
    #
    # Quando o usuário clica em Finalizar, deixamos de renderizar
    # o questionário e passamos para uma tela exclusiva de resultado.

    if not st.session_state.questionnaire_finished:
        all_active_subquestion_ids = render_questionnaire()

        remove_inactive_subanswers(all_active_subquestion_ids)

        clear_outdated_result_if_answers_changed()

        return

    # Se o questionário foi finalizado, não renderizamos mais a última pergunta.
    # Apenas reconstruímos o fluxo ativo para validar as subperguntas necessárias.
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
            "Não foi possível gerar o resultado porque ainda existem respostas obrigatórias pendentes."
        )
        return

    if st.session_state.classification_result is None:
        generate_and_store_result()

    render_result_section()

if __name__ == "__main__":
    main()