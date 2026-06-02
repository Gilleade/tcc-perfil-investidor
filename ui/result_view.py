# Importa o Streamlit para renderizar elementos da interface.
import streamlit as st

# Importa a função que limpa a simulação atual.
from utils.session import clear_simulation
from logic.decision_trace import build_decision_flowchart


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


def format_decision_trace_table(decision_trace):
    """
    Converte o rastreamento da decisão em uma tabela amigável.

    A tabela mostra como as respostas e eventos intermediários
    influenciaram o caminho percorrido pela árvore de decisão.
    """

    rows = []

    for item in decision_trace:
        rows.append(
            {
                "Etapa": str(item.get("etapa", "")),
                "Pergunta ou evento": str(item.get("pergunta_evento", "")),
                "Resposta": str(item.get("resposta", "")),
                "Efeito na árvore": str(item.get("efeito", "")),
                "Perfil antes": str(item.get("perfil_antes") or "-"),
                "Perfil depois": str(item.get("perfil_depois") or "-"),
                "Nível antes": str(item.get("nivel_antes") or "-"),
                "Nível depois": str(item.get("nivel_depois") or "-"),
            }
        )

    return rows


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

    decision_trace = classification_result.get("decision_trace", [])

    if decision_trace:
        st.subheader("Percurso da decisão")

        st.write(
            "A tabela abaixo apresenta como as respostas e os eventos intermediários "
            "influenciaram o caminho percorrido pela árvore de decisão até a classificação final."
        )

        trace_table = format_decision_trace_table(decision_trace)

        st.dataframe(
            trace_table,
            width="stretch",
            hide_index=True,
        )
        
        st.write("**Fluxograma do percurso decisório:**")

        decision_flowchart = build_decision_flowchart(decision_trace)

        st.graphviz_chart(
            decision_flowchart,
            width="stretch",
        )

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