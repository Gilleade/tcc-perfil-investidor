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
                max-width: 760px;
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
            
            .decision-card {
                margin-top: 1.4rem;
                padding: 1.1rem 1.2rem;
                border-radius: 0.8rem;
                border: 1px solid rgba(128, 128, 128, 0.25);
                background: rgba(128, 128, 128, 0.08);
            }

            .decision-card h4 {
                margin: 0 0 0.4rem 0;
            }

            .decision-card-description {
                margin: 0;
                opacity: 0.85;
                line-height: 1.5;
            }

            .decision-line {
                margin: 0.7rem 0;
                padding: 0.85rem 1rem;
                border-radius: 0.7rem;
                border-left: 4px solid rgba(128, 128, 128, 0.45);
                background: rgba(128, 128, 128, 0.05);
            }

            .decision-question {
                font-weight: 600;
                margin-bottom: 0.25rem;
            }

            .decision-answer {
                font-size: 0.95rem;
                margin-bottom: 0.25rem;
            }

            .decision-effect {
                font-size: 0.9rem;
                opacity: 0.82;
                line-height: 1.45;
            }

            .decision-card-footer {
                margin-top: 0.8rem;
                padding: 0.85rem 1rem;
                border-radius: 0.7rem;
                background: rgba(128, 128, 128, 0.12);
                font-size: 1rem;
            }
            
            .tree-block {
                margin-top: 1.4rem;
                padding: 1.05rem 1.15rem;
                border-radius: 0.85rem;
                border: 1px solid rgba(128, 128, 128, 0.22);
                background: rgba(128, 128, 128, 0.08);
            }

            .tree-block-title {
                font-size: 1.08rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .tree-block-description {
                opacity: 0.84;
                line-height: 1.5;
            }

            .tree-step {
                margin: 0.9rem 0;
                padding: 0.9rem 1rem;
                border-radius: 0.8rem;
                border: 1px solid rgba(128, 128, 128, 0.16);
                background: rgba(128, 128, 128, 0.04);
            }

            .tree-line {
                line-height: 1.55;
                padding: 0.08rem 0;
            }

            .tree-line-1 {
                font-weight: 600;
                margin-left: 0rem;
            }

            .tree-line-2 {
                margin-left: 1.2rem;
            }

            .tree-line-3 {
                margin-left: 2.4rem;
                opacity: 0.86;
            }

            .tree-block-footer {
                margin-top: 0.85rem;
                padding: 0.8rem 1rem;
                border-radius: 0.75rem;
                background: rgba(128, 128, 128, 0.12);
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_start_screen():
    """
    Exibe a tela inicial minimalista do protótipo.

    Essa tela aparece apenas no primeiro acesso.
    Depois que o usuário inicia a simulação, novas simulações voltam
    diretamente para a primeira pergunta.
    """

    st.title("Sistema de Apoio à Decisão para Classificação do Perfil do Investidor")

    st.markdown(
        """
        <p class="app-subtitle">
        Responda algumas perguntas sobre seus objetivos, sua situação financeira
        e seu conhecimento sobre investimentos para visualizar uma classificação
        estimada do seu perfil.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "Este protótipo tem finalidade acadêmica e classificatória. "
        "Ele não recomenda investimentos e não substitui avaliação profissional."
    )

    if st.button("Começar", type="primary", width="stretch"):
        st.session_state.app_started = True
        st.session_state.current_flow_index = 0
        st.session_state.questionnaire_finished = False
        st.rerun()