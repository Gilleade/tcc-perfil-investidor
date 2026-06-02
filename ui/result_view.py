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


def _render_decision_line(item):
    """
    Renderiza uma linha simples de decisão.

    A linha mostra:
    - pergunta ou evento;
    - resposta;
    - efeito na árvore.

    O objetivo é explicar a decisão em linguagem visual,
    sem parecer uma tabela técnica.
    """

    pergunta_evento = item.get("pergunta_evento", "")
    resposta = item.get("resposta", "")
    efeito = item.get("efeito", "")

    st.markdown(
        f"""
        <div class="decision-line">
            <div class="decision-question">{pergunta_evento}</div>
            <div class="decision-answer">Resposta: <strong>{resposta}</strong></div>
            <div class="decision-effect">{efeito}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_stage_card(title, description, items, footer_label=None, footer_value=None):
    """
    Renderiza um card visual para uma etapa da classificação.

    Cada card representa uma parte da árvore:
    - perfil preliminar;
    - situação financeira;
    - conhecimento e experiência;
    - resultado final.
    """

    st.markdown(
        f"""
        <div class="decision-card">
            <h4>{title}</h4>
            <p class="decision-card-description">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in items:
        _render_decision_line(item)

    if footer_label and footer_value:
        st.markdown(
            f"""
            <div class="decision-card-footer">
                {footer_label}: <strong>{footer_value}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_decision_path_cards(classification_result):
    """
    Exibe a formação da classificação em quatro blocos visuais.

    Essa visualização substitui a tabela e o fluxograma técnico,
    mostrando o percurso lógico da árvore de decisão de forma
    mais simples e intuitiva.
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

    st.subheader("Como a classificação foi formada")

    st.write(
        "A classificação foi construída em etapas. Primeiro, o sistema identifica "
        "uma orientação inicial de perfil. Depois, verifica se a situação financeira "
        "limita essa classificação. Por fim, considera conhecimento e experiência "
        "para confirmar ou ajustar o resultado."
    )

    objectives_items = [
        item for item in _get_trace_items_by_stage(decision_trace, "Objetivos")
        if item.get("id") in ["P1", "P2", "2A", "P3"]
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
            "pergunta_evento": "Perfil preliminar",
            "resposta": preliminary_profile,
            "efeito": "Resultado inicial obtido a partir dos objetivos, horizonte temporal e tolerância ao risco.",
        },
        {
            "pergunta_evento": "Limite prudencial financeiro",
            "resposta": financial_limit,
            "efeito": "Perfil máximo considerado compatível com a situação financeira informada.",
        },
        {
            "pergunta_evento": "Após conhecimento e experiência",
            "resposta": knowledge_profile,
            "efeito": "Resultado após verificar se o conhecimento e a experiência sustentam a classificação.",
        },
    ]

    _render_stage_card(
        title="1. Perfil preliminar",
        description="Esta etapa analisa finalidade do investimento, horizonte temporal e tolerância ao risco.",
        items=objectives_items,
        footer_label="Perfil preliminar",
        footer_value=preliminary_profile,
    )

    _render_stage_card(
        title="2. Situação financeira",
        description="Esta etapa verifica se há necessidade de liquidez, fragilidade financeira ou limite prudencial.",
        items=financial_items,
        footer_label="Perfil após compatibilidade financeira",
        footer_value=financial_profile,
    )

    _render_stage_card(
        title="3. Conhecimento e experiência",
        description="Esta etapa verifica se o conhecimento declarado e a experiência prática sustentam o perfil identificado.",
        items=knowledge_items,
        footer_label="Perfil após conhecimento e experiência",
        footer_value=knowledge_profile,
    )

    _render_stage_card(
        title="4. Resultado final",
        description="Esta etapa consolida o percurso da árvore e apresenta a classificação final.",
        items=final_items,
        footer_label="Perfil final",
        footer_value=final_profile,
    )


def _get_trace_items_by_stage(decision_trace, stage_name):
    """
    Filtra os itens do rastreamento por etapa.
    """

    return [
        item for item in decision_trace
        if item.get("etapa") == stage_name
    ]


def _derive_conclusion_label(effect):
    """
    Converte o efeito técnico em uma conclusão visual curta.

    Exemplo:
    - Tende para Arrojado
    - Tende para Moderado
    - Tende para Conservador
    - Bloqueia Arrojado
    - Reduz em 1 nível
    """

    text = (effect or "").lower()

    if "bloque" in text and "arroj" in text:
        return "Bloqueia Arrojado"

    if "reduz" in text and "2" in text:
        return "Reduz em 2 níveis"

    if "reduz" in text:
        return "Reduz em 1 nível"

    if "conservador" in text:
        return "Tende para Conservador"

    if "moderado" in text:
        return "Tende para Moderado"

    if "arrojado" in text:
        return "Tende para Arrojado"

    if "mant" in text:
        return "Mantém a classificação da etapa"

    return "Influencia a classificação nesta etapa"


def _render_tree_step(question, answer, explanation, conclusion):
    """
    Renderiza uma etapa da árvore em formato hierárquico recuado.
    """

    question = escape(question or "")
    answer = escape(answer or "")
    explanation = escape(explanation or "")
    conclusion = escape(conclusion or "")

    st.markdown(
        f"""
        <div class="tree-step">
            <div class="tree-line tree-line-1">↳ {question}</div>
            <div class="tree-line tree-line-2">↳ Resposta: <strong>{answer}</strong></div>
            <div class="tree-line tree-line-3">↳ {explanation}</div>
            <div class="tree-line tree-line-4">↳ {conclusion}</div>
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

        explanation = effect or "Essa resposta influencia a classificação nesta etapa."
        conclusion = item.get("direcao") or _derive_conclusion_label(effect)

        _render_tree_step(
            question=question,
            answer=answer,
            explanation=explanation,
            conclusion=conclusion,
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
        "Abaixo, o sistema apresenta o caminho percorrido na árvore de decisão. "
        "Cada pergunta mostra a resposta registrada, a interpretação lógica dessa escolha "
        "e o efeito que ela produziu na classificação."
    )

    objectives_items = [
        item for item in _get_trace_items_by_stage(decision_trace, "Objetivos")
        if item.get("id") in ["P1", "P2", "2A", "P3"]
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
        description="Síntese do percurso realizado ao longo da árvore de decisão.",
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