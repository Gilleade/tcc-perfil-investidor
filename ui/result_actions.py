# Importa o Streamlit para renderizar elementos da interface.
import streamlit as st

# Importa a função que executa toda a sequência lógica da árvore.
from logic.final_consolidation import consolidate_final_profile

# Importa a função que gera a justificativa textual do resultado.
from logic.justification import generate_justification

# Importa a função que cria a assinatura das respostas atuais.
from utils.session import get_answers_signature


def render_result_generation(validation_result):
    """
    Exibe a seção de geração do resultado.

    Esta função:
    - informa se ainda existem pendências;
    - habilita o botão de geração apenas quando o questionário está completo;
    - consolida o perfil final;
    - gera a justificativa textual;
    - salva os resultados no estado da sessão.

    Parâmetros:
    - validation_result: resultado da validação do preenchimento.
    """

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