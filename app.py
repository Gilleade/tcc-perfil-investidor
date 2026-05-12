# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa a função de validação das respostas obrigatórias.
from utils.validation import validate_required_answers

# Importa a seção de geração do resultado.
from ui.result_actions import render_result_generation

# Importa a seção de resultado da interface.
from ui.result_view import render_result_section

# Importa a montagem completa dos blocos do questionário.
from ui.questionnaire import render_questionnaire

# Importa elementos visuais gerais da aplicação.
from ui.layout import (
    apply_custom_styles,
    render_header,
    render_completion_status,
)

# Importa o Streamlit para acessar o estado da sessão.
from utils.session import (
    initialize_session_state,
    get_answers_signature,
)

# Importa painel técnico e botão de limpeza.
from ui.debug_panel import (
    render_registered_answers_panel,
    render_clear_answers_button,
)


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


apply_custom_styles()

initialize_session_state()


# -------------------------------------------------------------------
# Cabeçalho da aplicação
# -------------------------------------------------------------------

render_header()


# -------------------------------------------------------------------
# Renderização do questionário
# -------------------------------------------------------------------

all_active_subquestion_ids = render_questionnaire()


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

render_completion_status(validation_result)

# -------------------------------------------------------------------
# Geração do resultado
# -------------------------------------------------------------------

render_result_generation(validation_result)


# -------------------------------------------------------------------
# Exibição do resultado
# -------------------------------------------------------------------

render_result_section()


# -------------------------------------------------------------------
# Painel técnico de respostas
# -------------------------------------------------------------------

render_registered_answers_panel()


# -------------------------------------------------------------------
# Botão de limpeza da simulação
# -------------------------------------------------------------------

render_clear_answers_button()