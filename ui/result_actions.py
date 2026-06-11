# Importa o Streamlit para renderizar elementos da interface.
import streamlit as st

# Importa a função que executa toda a sequência lógica baseada em regras.
from logic.final_consolidation import consolidate_final_profile

# Importa a função que gera a justificativa textual do resultado.
from logic.justification import generate_justification

# Importa a função que monta o rastreamento do caminho decisório.
from logic.decision_trace import build_decision_trace

# Importa a função que cria a assinatura das respostas atuais.
from utils.session import get_answers_signature


def generate_and_store_result():
    """
    Gera o resultado da classificação e salva no estado da sessão.

    Esta função não renderiza botão.
    Ela apenas executa a lógica baseada em regras, gera a justificativa
    e armazena os dados para a tela de resultado.
    """

    try:
        classification_result = consolidate_final_profile(
            answers=st.session_state.answers,
            subanswers=st.session_state.subanswers,
        )

        decision_trace = build_decision_trace(
            answers=st.session_state.answers,
            subanswers=st.session_state.subanswers,
            preliminary_profile=classification_result["preliminary_profile"],
            financial_result=classification_result["results"]["financial"],
            knowledge_result=classification_result["results"]["knowledge"],
            final_profile=classification_result["final_profile"],
        )

        classification_result["decision_trace"] = decision_trace

        justification_result = generate_justification(classification_result)

        st.session_state.classification_result = classification_result
        st.session_state.justification_result = justification_result
        st.session_state.result_signature = get_answers_signature()

    except ValueError as error:
        st.error(f"Não foi possível gerar o resultado: {error}")