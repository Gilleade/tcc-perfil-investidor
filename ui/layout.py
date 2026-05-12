# Importa o Streamlit para renderizar elementos visuais da interface.
import streamlit as st


def apply_custom_styles():
    """
    Aplica estilos visuais simples ao protótipo.

    Estes estilos não alteram a lógica da aplicação.
    Eles apenas melhoram espaçamento, leitura e aparência geral.
    """

    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 980px;
            }

            .app-subtitle {
                color: #555;
                font-size: 1.05rem;
                line-height: 1.6;
                margin-bottom: 1rem;
            }

            .section-note {
                color: #666;
                font-size: 0.95rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            }

            .question-summary {
                color: #666;
                font-size: 0.88rem;
                margin-top: -0.4rem;
                margin-bottom: 0.6rem;
            }

            .status-box {
                border: 1px solid rgba(128, 128, 128, 0.35);
                border-radius: 12px;
                padding: 1rem 1.2rem;
                margin: 1rem 0;
                background-color: var(--secondary-background-color);
                color: var(--text-color);
            }

            div[data-testid="stRadio"] {
                margin-bottom: 0.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_header():
    """
    Exibe o cabeçalho principal da aplicação.

    O cabeçalho apresenta:
    - título;
    - descrição curta;
    - aviso de limite acadêmico do sistema.
    """

    st.title("Sistema de Apoio à Decisão para Classificação do Perfil do Investidor")

    st.markdown(
        """
        <p class="app-subtitle">
        Protótipo acadêmico desenvolvido em Python e Streamlit para classificar
        o perfil do investidor por meio de perguntas estruturadas, árvore de decisão
        e regras explícitas.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "Este sistema tem finalidade acadêmica. Ele não recomenda investimentos, "
        "não indica produtos financeiros, não consulta dados de mercado e não substitui "
        "avaliação profissional."
    )

    st.divider()


def render_block_intro(block_id):
    """
    Exibe o texto introdutório de cada bloco do questionário.

    Parâmetros:
    - block_id: identificador do bloco.
      Exemplos: "B1", "B2", "B3".
    """

    block_texts = {
        "B1": """
            <p class="section-note">
            Responda às perguntas sobre finalidade, prazo e tolerância ao risco.
            Essas respostas formam o perfil preliminar da classificação.
            </p>
        """,
        "B2": """
            <p class="section-note">
            Responda às perguntas sobre necessidade de recursos, renda e reserva financeira.
            Essas respostas verificam a compatibilidade financeira do perfil preliminar.
            </p>
        """,
        "B3": """
            <p class="section-note">
            Responda às perguntas sobre familiaridade, experiência e formação relacionada.
            Essas respostas refinam a classificação final sem elevar o perfil isoladamente.
            </p>
        """,
    }

    text = block_texts.get(block_id)

    if text:
        st.markdown(text, unsafe_allow_html=True)


def render_completion_status(validation_result):
    """
    Exibe automaticamente o andamento do preenchimento do questionário.

    Esta função substitui a necessidade de um botão "Verificar preenchimento".
    O status é atualizado conforme o usuário responde às perguntas.
    """

    st.header("Andamento do preenchimento")

    missing_questions_count = len(validation_result["missing_questions"])
    missing_subquestions_count = len(validation_result["missing_subquestions"])

    total_required = (
        len(st.session_state.answers)
        + missing_questions_count
        + len(st.session_state.subanswers)
        + missing_subquestions_count
    )

    answered_required = (
        len(st.session_state.answers)
        + len(st.session_state.subanswers)
    )

    progress_value = 0

    if total_required > 0:
        progress_value = answered_required / total_required

    st.progress(progress_value)

    st.markdown(
        f"""
        <div class="status-box">
            <strong>Status:</strong> {answered_required} de {total_required} respostas obrigatórias preenchidas.
        </div>
        """,
        unsafe_allow_html=True
    )

    if validation_result["is_valid"]:
        st.success("Questionário completo. O resultado já pode ser gerado.")
    else:
        st.info("O questionário ainda possui pendências.")

        with st.expander("Ver perguntas pendentes"):
            if validation_result["missing_questions"]:
                st.write("**Perguntas principais pendentes:**")

                for question in validation_result["missing_questions"]:
                    st.write(
                        f"- **{question['id']}** — {question['text']} "
                        f"({question['block']})"
                    )

            if validation_result["missing_subquestions"]:
                st.write("**Subperguntas condicionais pendentes:**")

                for subquestion in validation_result["missing_subquestions"]:
                    st.write(
                        f"- **{subquestion['id']}** — {subquestion['text']} "
                        f"(origem: {subquestion['parent_question_id']})"
                    )