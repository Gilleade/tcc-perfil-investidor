# Importa o Streamlit para renderizar elementos da interface.
import streamlit as st

# Importa a função que limpa a simulação atual.
from utils.session import clear_simulation

from html import escape


def render_profile_badge(profile):
    """
    Exibe o perfil final com destaque visual.

    A lógica de classificação não está aqui.
    Esta função apenas melhora a apresentação do resultado.
    """

    if profile == "Conservador":
        st.info("Perfil final: Conservador")
    elif profile == "Moderado":
        st.success("Perfil final: Moderado")
    elif profile == "Arrojado":
        st.warning("Perfil final: Arrojado")
    else:
        st.write(f"Perfil final: {profile}")


def render_adjustments(adjustments):
    """
    Exibe os ajustes realizados após o perfil preliminar.

    Os ajustes vêm da consolidação final e mostram se houve manutenção
    ou redução por compatibilidade financeira e por conhecimento/experiência.
    """

    if not adjustments:
        st.write("Nenhum ajuste registrado.")
        return

    for adjustment in adjustments:
        stage = adjustment["stage"]
        adjustment_type = adjustment["type"]
        levels = adjustment["levels"]
        reason = adjustment["reason"]
        from_profile = adjustment["from_profile"]
        to_profile = adjustment["to_profile"]

        if adjustment_type == "reducao":
            level_text = "1 nível" if levels == 1 else f"{levels} níveis"

            st.write(
                f"- **{stage}**: reduziu de **{from_profile}** para **{to_profile}** "
                f"({level_text}). Motivo: {reason}"
            )
        else:
            st.write(
                f"- **{stage}**: manteve **{to_profile}**. Motivo: {reason}"
            )


def _get_trace_items_by_stage(decision_trace, stage_name):
    """
    Filtra os itens do rastreamento por etapa.

    Exemplo de etapas:
    - Objetivos
    - Situação financeira
    - Conhecimento e experiência
    - Resultado
    """

    return [
        item for item in decision_trace
        if item.get("etapa") == stage_name
    ]


def _render_tree_step(question, answer, interpretation):
    """
    Renderiza uma etapa da árvore em formato hierárquico recuado.

    A estrutura apresentada ao usuário é:
    pergunta -> resposta -> interpretação da resposta.
    """

    question = escape(question or "")
    answer = escape(answer or "")
    interpretation = escape(interpretation or "")

    st.markdown(
        f"""
        <div class="tree-step">
            <div class="tree-line tree-line-1">↳ {question}</div>
            <div class="tree-line tree-line-2">↳ Resposta: <strong>{answer}</strong></div>
            <div class="tree-line tree-line-3">↳ {interpretation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_tree_block(title, description, items, footer_label=None, footer_value=None):
    """
    Renderiza um bloco da árvore percorrida.
    """

    st.markdown(
        f"""
        <div class="tree-block">
            <div class="tree-block-title">{escape(title)}</div>
            <div class="tree-block-description">{escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in items:
        question = item.get("pergunta_evento", "")
        answer = item.get("resposta", "")
        effect = item.get("efeito", "")

        interpretation = item.get("direcao") or effect or (
            "Essa resposta foi considerada na etapa de classificação."
        )

        _render_tree_step(
            question=question,
            answer=answer,
            interpretation=interpretation,
        )

    if footer_label and footer_value:
        st.markdown(
            f"""
            <div class="tree-block-footer">
                {escape(footer_label)}: <strong>{escape(str(footer_value))}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_decision_tree_path(classification_result):
    """
    Exibe a árvore percorrida em formato hierárquico.
    """

    decision_trace = classification_result.get("decision_trace", [])

    if not decision_trace:
        return

    preliminary_profile = classification_result.get("preliminary_profile", "-")
    financial_profile = classification_result.get("financial_profile", "-")
    final_profile = classification_result.get("final_profile", "-")

    financial_result = classification_result.get("results", {}).get("financial", {})
    knowledge_result = classification_result.get("results", {}).get("knowledge", {})

    financial_limit = financial_result.get("financial_limit_profile", financial_profile)
    knowledge_profile = knowledge_result.get("profile", final_profile)

    st.subheader("Como cada resposta influenciou o resultado")

    st.write(
        "Abaixo, o sistema apresenta o percurso lógico da classificação. "
        "Cada pergunta mostra a resposta registrada, a interpretação lógica dessa escolha "
        "e o efeito que ela produziu no resultado."
    )

    objectives_items = [
        item for item in _get_trace_items_by_stage(decision_trace, "Objetivos")
        if item.get("id") in ["P1", "P2", "P3"]
    ]

    financial_items = [
        item for item in _get_trace_items_by_stage(decision_trace, "Situação financeira")
        if item.get("id") in ["P4", "4A", "4B", "P5", "5A", "P6", "6A", "6B"]
    ]

    knowledge_items = [
        item for item in _get_trace_items_by_stage(decision_trace, "Conhecimento e experiência")
        if item.get("id") in ["P7", "7A", "7B", "P8", "8A", "8B", "P9"]
    ]

    final_items = [
        {
            "pergunta_evento": "Perfil preliminar identificado",
            "resposta": preliminary_profile,
            "efeito": f"O primeiro bloco da árvore gerou um perfil preliminar {preliminary_profile}.",
        },
        {
            "pergunta_evento": "Compatibilidade financeira aplicada",
            "resposta": financial_limit,
            "efeito": f"A etapa financeira definiu como limite prudencial o perfil {financial_limit}.",
        },
        {
            "pergunta_evento": "Refinamento por conhecimento e experiência",
            "resposta": knowledge_profile,
            "efeito": f"A etapa de conhecimento e experiência conduziu o resultado para {knowledge_profile}.",
        },
        {
            "pergunta_evento": "Classificação final",
            "resposta": final_profile,
            "efeito": f"O sistema consolidou o perfil final como {final_profile}.",
        },
    ]

    _render_tree_block(
        title="1. Perfil preliminar",
        description="Análise de finalidade, horizonte temporal e tolerância ao risco.",
        items=objectives_items,
        footer_label="Perfil preliminar",
        footer_value=preliminary_profile,
    )

    _render_tree_block(
        title="2. Situação financeira",
        description="Verificação de necessidade de liquidez, estabilidade e reserva financeira.",
        items=financial_items,
        footer_label="Perfil após compatibilidade financeira",
        footer_value=financial_profile,
    )

    _render_tree_block(
        title="3. Conhecimento e experiência",
        description="Verificação de familiaridade, experiência prática e formação relacionada.",
        items=knowledge_items,
        footer_label="Perfil após conhecimento e experiência",
        footer_value=knowledge_profile,
    )

    _render_tree_block(
        title="4. Consolidação do resultado final",
        description="Síntese do percurso lógico realizado até a classificação final.",
        items=final_items,
        footer_label="Perfil final",
        footer_value=final_profile,
    )


def render_result_section():
    """
    Exibe a tela de resultado quando já existe uma classificação gerada.

    Esta função depende de dois dados salvos na sessão:
    - classification_result;
    - justification_result.
    """

    classification_result = st.session_state.classification_result
    justification_result = st.session_state.justification_result

    if classification_result is None or justification_result is None:
        return

    st.divider()
    st.header("Resultado da classificação")

    final_profile = classification_result["final_profile"]
    preliminary_profile = classification_result["preliminary_profile"]
    financial_profile = classification_result["financial_profile"]

    # Destaque principal do perfil final.
    render_profile_badge(final_profile)

    st.subheader("Resumo da classificação")

    st.write(
        f"O perfil inicialmente identificado foi **{preliminary_profile}**. "
        f"Após a análise da situação financeira, a classificação passou para "
        f"**{financial_profile}**. Ao final, considerando também conhecimento "
        f"e experiência, o perfil resultante foi **{final_profile}**."
    )

    st.write(justification_result["summary"])

    st.subheader("Ajustes realizados")
    render_adjustments(classification_result.get("adjustments", []))

    render_decision_tree_path(classification_result)

    st.subheader("Travas, bloqueios e inconsistências")

    blocked_profiles = classification_result.get("blocked_profiles", [])
    inconsistencies = classification_result.get("inconsistencies", [])

    if blocked_profiles:
        st.write("**Perfis bloqueados por prudência:**")

        for profile in blocked_profiles:
            st.write(f"- {profile}")
    else:
        st.write("Não houve bloqueio prudencial de perfil.")

    if inconsistencies:
        st.write("**Inconsistências ou pontos de atenção:**")

        for item in inconsistencies:
            st.write(f"- {item}")
    else:
        st.write("Não foram registradas inconsistências relevantes.")

    st.subheader("Justificativa textual completa")

    # st.markdown permite exibir o texto com negrito e quebras de linha.
    st.markdown(justification_result["full_text"])

    if st.button("Nova simulação", key="new_simulation_button"):
        clear_simulation()
        st.rerun()