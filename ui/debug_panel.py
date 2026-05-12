# Importa o Streamlit para renderizar elementos da interface.
import streamlit as st

# Importa a função que limpa respostas, resultado e estado visual da simulação.
from utils.session import clear_simulation


def render_registered_answers_panel():
    """
    Exibe um painel expansível com as respostas registradas.

    Esta área é útil para conferência técnica durante o desenvolvimento
    e para rastrear se as respostas estão sendo armazenadas corretamente.

    Ela permanece recolhida por padrão para não poluir a interface principal.
    """

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


def render_clear_answers_button():
    """
    Exibe o botão de limpeza da simulação.

    Este botão limpa:
    - respostas principais;
    - subperguntas;
    - resultado gerado;
    - justificativa textual;
    - seleção visual dos radios.

    Ele tem função semelhante ao botão “Nova simulação”,
    mas fica disponível mesmo antes de gerar resultado.
    """

    if st.button("Limpar respostas"):
        clear_simulation()
        st.rerun()