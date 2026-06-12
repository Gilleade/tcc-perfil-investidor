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
        stage = _format_adjustment_stage(adjustment["stage"])
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
    

def _format_adjustment_stage(stage):
    """
    Transforma o nome interno da etapa em texto amigável.
    """

    labels = {
        "compatibilidade_financeira": "Compatibilidade financeira",
        "refinamento_conhecimento_experiencia": "Conhecimento e experiência",
    }

    return labels.get(stage, stage)


def render_result_summary_table(classification_result):
    """
    Exibe uma síntese visual da classificação.
    """

    preliminary_profile = classification_result.get("preliminary_profile", "-")
    financial_profile = classification_result.get("financial_profile", "-")
    final_profile = classification_result.get("final_profile", "-")

    st.subheader("Resumo visual da classificação")

    st.markdown(
        f"""
        | Etapa | Resultado |
        |---|---|
        | Bloco 1 — Objetivos e tolerância ao risco | Perfil preliminar: **{preliminary_profile}** |
        | Bloco 2 — Compatibilidade financeira | Perfil após análise financeira: **{financial_profile}** |
        | Bloco 3 — Conhecimento e experiência | Perfil final: **{final_profile}** |
        """
    )


def _render_process_step(question, answer, interpretation):
    """
    Renderiza uma resposta considerada na classificação.
    """

    question = escape(question or "")
    answer = escape(answer or "")
    interpretation = escape(interpretation or "")

    st.markdown(
        f"""
        <div class="decision-line">
            <div class="decision-question">{question}</div>
            <div class="decision-answer">Resposta: <strong>{answer}</strong></div>
            <div class="decision-effect">{interpretation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_process_block(title, description, result_label, result_value, items):
    """
    Renderiza um bloco do processamento decisório.
    """

    st.markdown(
        f"""
        <div class="decision-card">
            <h4>{escape(title)}</h4>
            <p class="decision-card-description">{escape(description)}</p>
            <div class="decision-card-footer">
                {escape(result_label)}: <strong>{escape(str(result_value))}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not items:
        return

    with st.expander(f"Ver respostas consideradas em {title}"):
        for item in items:
            question = item.get("pergunta_evento", "")
            answer = item.get("resposta", "")
            effect = item.get("efeito", "")

            interpretation = item.get("direcao") or effect or (
                "Essa resposta foi considerada na etapa de classificação."
            )

            _render_process_step(
                question=question,
                answer=answer,
                interpretation=interpretation,
            )


def render_process_by_blocks(classification_result):
    """
    Exibe o processamento decisório por blocos.

    O sistema é apresentado como um modelo baseado em regras explícitas,
    organizado em etapas sucessivas de classificação.
    """

    decision_trace = classification_result.get("decision_trace", [])

    if not decision_trace:
        return

    preliminary_profile = classification_result.get("preliminary_profile", "-")
    financial_profile = classification_result.get("financial_profile", "-")
    final_profile = classification_result.get("final_profile", "-")

    st.subheader("Entenda o resultado por blocos")

    st.write(
        "A classificação foi construída em etapas. Primeiro, o sistema identificou "
        "uma orientação inicial de perfil. Depois, verificou se a situação financeira "
        "permitia manter essa classificação. Por fim, avaliou se o conhecimento e a "
        "experiência sustentavam o resultado."
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

    _render_process_block(
        title="Bloco 1 — Objetivos e tolerância ao risco",
        description=(
            "Analisa finalidade do investimento, horizonte temporal e reação a "
            "oscilações para formar a orientação inicial do perfil."
        ),
        result_label="Perfil preliminar",
        result_value=preliminary_profile,
        items=objectives_items,
    )

    _render_process_block(
        title="Bloco 2 — Compatibilidade financeira",
        description=(
            "Verifica necessidade de uso do recurso, estabilidade de renda e reserva "
            "financeira para manter ou limitar o perfil preliminar."
        ),
        result_label="Perfil após compatibilidade financeira",
        result_value=financial_profile,
        items=financial_items,
    )

    _render_process_block(
        title="Bloco 3 — Conhecimento e experiência",
        description=(
            "Avalia familiaridade, experiência prática e formação relacionada para "
            "confirmar ou refinar a classificação."
        ),
        result_label="Perfil final após refinamento",
        result_value=final_profile,
        items=knowledge_items,
    )


def render_attention_points(classification_result):
    """
    Exibe bloqueios, travas e inconsistências apenas quando forem relevantes.
    """

    blocked_profiles = classification_result.get("blocked_profiles", [])
    inconsistencies = classification_result.get("inconsistencies", [])

    if not blocked_profiles and not inconsistencies:
        st.info("Não foram identificadas inconsistências relevantes nesta simulação.")
        return

    st.subheader("Pontos de atenção identificados")

    if blocked_profiles:
        st.write("**Perfis bloqueados por prudência:**")

        for profile in blocked_profiles:
            st.write(f"- {profile}")

    if inconsistencies:
        st.write("**Inconsistências ou pontos de atenção:**")

        for item in inconsistencies:
            st.write(f"- {item}")


def render_consistency_guidance(classification_result):
    """
    Exibe orientações gerais para tornar a classificação mais consistente.

    Esta função não recomenda produtos financeiros e não sugere mudança de perfil.
    Ela apenas indica fatores que podem tornar as respostas mais alinhadas entre si.
    """

    final_profile = classification_result.get("final_profile", "-")
    total_reduction_steps = classification_result.get("total_reduction_steps", 0)
    blocked_profiles = classification_result.get("blocked_profiles", [])
    inconsistencies = classification_result.get("inconsistencies", [])

    st.subheader("Como tornar a classificação mais consistente")

    st.write(
        "Os perfis Conservador, Moderado e Arrojado não representam uma escala de melhor "
        "ou pior. Eles indicam graus diferentes de compatibilidade entre objetivos, situação "
        "financeira, tolerância ao risco e conhecimento sobre investimentos."
    )

    suggestions = []

    if total_reduction_steps > 0 or blocked_profiles:
        suggestions.append(
            "Observar quais fatores limitaram a classificação, principalmente necessidade "
            "de liquidez, reserva financeira ou conhecimento insuficiente."
        )

    if inconsistencies:
        suggestions.append(
            "Revisar respostas que indicaram conflito, como alta tolerância ao risco combinada "
            "com necessidade de uso do recurso em prazo curto."
        )

    if final_profile == "Conservador":
        suggestions.extend([
            "Manter clareza sobre prazo de uso do dinheiro e necessidade de liquidez.",
            "Fortalecer reserva financeira antes de assumir maior exposição a oscilações.",
            "Ampliar conhecimento sobre riscos antes de considerar alternativas mais voláteis.",
        ])
    elif final_profile == "Moderado":
        suggestions.extend([
            "Manter equilíbrio entre busca de crescimento, prazo e capacidade de suportar oscilações.",
            "Aprofundar conhecimento sobre riscos para tornar futuras decisões mais conscientes.",
            "Reavaliar periodicamente objetivos e necessidade de liquidez.",
        ])
    elif final_profile == "Arrojado":
        suggestions.extend([
            "Verificar se a reserva financeira e o prazo continuam compatíveis com maior exposição a oscilações.",
            "Manter atenção à diferença entre tolerar oscilações e precisar do recurso no curto prazo.",
            "Revisar a classificação sempre que houver mudança relevante de renda, reserva, objetivos ou conhecimento.",
        ])

    for suggestion in suggestions:
        st.write(f"- {suggestion}")


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

    # Destaque principal do perfil final.
    render_profile_badge(final_profile)

    st.write(
        f"Com base nas respostas fornecidas, o sistema classificou o perfil como "
        f"**{final_profile}**, considerando objetivos, situação financeira, "
        f"tolerância ao risco e conhecimento/experiência."
    )

    render_result_summary_table(classification_result)

    st.subheader("Explicação geral")
    st.write(justification_result["summary"])

    with st.expander("Ver ajustes realizados"):
        render_adjustments(classification_result.get("adjustments", []))

    render_process_by_blocks(classification_result)

    render_attention_points(classification_result)

    render_consistency_guidance(classification_result)

    with st.expander("Ver justificativa textual completa"):
        st.markdown(justification_result["full_text"])

    if st.button("Nova simulação", key="new_simulation_button"):
        clear_simulation()
        st.rerun()