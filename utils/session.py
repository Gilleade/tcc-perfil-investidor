# Importa o Streamlit para acessar o estado da sessão.
import streamlit as st

def initialize_session_state():
    """
    Inicializa as chaves necessárias no estado da sessão.

    O Streamlit recarrega o script a cada interação.
    Por isso, usamos st.session_state para preservar:
    - respostas principais;
    - respostas condicionais;
    - contador de limpeza;
    - resultado consolidado;
    - justificativa textual;
    - assinatura das respostas usadas no resultado.

    A função só cria cada chave se ela ainda não existir.
    Isso evita sobrescrever respostas já preenchidas pelo usuário.
    """

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
        # Isso evita mostrar resultado antigo depois que o usuário altera respostas.
        st.session_state.result_signature = None


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