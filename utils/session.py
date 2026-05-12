# Importa o Streamlit para acessar o estado da sessão.
import streamlit as st


def get_answers_signature():
    """
    Cria uma assinatura simples das respostas atuais.

    Essa assinatura é usada para saber se o usuário alterou alguma resposta
    depois de gerar o resultado.

    Se as respostas mudarem, o resultado antigo é descartado para evitar
    inconsistência entre formulário e classificação exibida.

    Retorno:
    - string representando as respostas principais e condicionais atuais.
    """

    main_answers = sorted(st.session_state.answers.items())
    conditional_answers = sorted(st.session_state.subanswers.items())

    return repr((main_answers, conditional_answers))


def clear_simulation():
    """
    Limpa a simulação atual.

    Esta função remove:
    - respostas principais;
    - respostas condicionais;
    - resultado consolidado;
    - justificativa textual;
    - assinatura do resultado;
    - seleção visual dos campos radio.

    Depois de chamar esta função, a tela deve ser recarregada com st.rerun().
    """

    st.session_state.answers = {}
    st.session_state.subanswers = {}
    st.session_state.classification_result = None
    st.session_state.justification_result = None
    st.session_state.result_signature = None

    # Incrementa o contador para recriar os campos de seleção.
    st.session_state.reset_counter += 1

    # Remove chaves antigas dos radios principais e condicionais.
    for key in list(st.session_state.keys()):
        if key.startswith("radio_"):
            del st.session_state[key]