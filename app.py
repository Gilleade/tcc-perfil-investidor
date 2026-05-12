# Importa o Streamlit, biblioteca usada para criar a interface web local.
import streamlit as st

# Importa a renderização dos blocos de perguntas.
from ui.question_blocks import render_question_block

# Importa a função de validação das respostas obrigatórias.
from utils.validation import validate_required_answers

# Importa funções de controle de sessão.
from utils.session import get_answers_signature, clear_simulation

# Importa a função que executa toda a sequência lógica da árvore.
from logic.final_consolidation import consolidate_final_profile

# Importa a função que gera a justificativa textual do resultado.
from logic.justification import generate_justification

# Importa a seção de resultado da interface.
from ui.result_view import render_result_section

# Importa elementos visuais gerais da aplicação.
from ui.layout import (
    apply_custom_styles,
    render_header,
    render_block_intro,
    render_completion_status,
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
# Cabeçalho da aplicação
# -------------------------------------------------------------------

render_header()


# -------------------------------------------------------------------
# Renderização dos blocos principais
# -------------------------------------------------------------------
#
# Esta lista será usada para controlar quais subperguntas estão ativas.

all_active_subquestion_ids = []


# Bloco 1 — Objetivos e tolerância ao risco
st.header("Bloco 1 — Objetivos e tolerância ao risco")
render_block_intro("B1")

all_active_subquestion_ids.extend(render_question_block("B1"))


# Bloco 2 — Compatibilidade financeira
st.header("Bloco 2 — Compatibilidade financeira")
render_block_intro("B2")

all_active_subquestion_ids.extend(render_question_block("B2"))


# Bloco 3 — Conhecimento e experiência
st.header("Bloco 3 — Conhecimento e experiência")
render_block_intro("B3")

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

render_completion_status(validation_result)

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