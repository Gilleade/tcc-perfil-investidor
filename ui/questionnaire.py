# Importa o Streamlit para renderizar elementos visuais.
import streamlit as st

# Importa o texto introdutório de cada bloco.
from ui.layout import render_block_intro

# Importa a renderização das perguntas e subperguntas.
from ui.question_blocks import render_question_block


def render_questionnaire():
    """
    Renderiza todos os blocos do questionário.

    Esta função exibe:
    - Bloco 1: objetivos e tolerância ao risco;
    - Bloco 2: compatibilidade financeira;
    - Bloco 3: conhecimento e experiência.

    Retorno:
    - lista com os ids das subperguntas condicionais ativas.

    Essa lista é usada depois para:
    - validar apenas subperguntas ativadas;
    - remover respostas antigas de subperguntas que deixaram de aparecer.
    """

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

    return all_active_subquestion_ids