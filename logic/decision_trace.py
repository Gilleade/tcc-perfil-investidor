"""
Módulo responsável por montar o rastreamento do caminho decisório.

O decision_trace registra, em ordem lógica, como as respostas do usuário
percorreram a árvore de decisão até chegar ao perfil final.

Esse rastreamento será usado posteriormente para:
- tabela explicativa pergunta por pergunta;
- fluxograma visual do percurso;
- explicação acadêmica da árvore de decisão.
"""

from data.questions import QUESTIONS
from data.subquestions import SUBQUESTIONS
from logic.preliminary_profile import (
    PROFILE_CONSERVADOR,
    PROFILE_MODERADO,
    PROFILE_ARROJADO,
)


PROFILE_LEVELS = {
    PROFILE_CONSERVADOR: 1,
    PROFILE_MODERADO: 2,
    PROFILE_ARROJADO: 3,
}


def _find_question(question_id):
    """
    Busca uma pergunta principal pelo ID.
    """

    for question in QUESTIONS:
        if question.get("id") == question_id:
            return question

    return None


def _find_subquestion(subquestion_id):
    """
    Busca uma subpergunta pelo ID.
    """

    for subquestion in SUBQUESTIONS:
        if subquestion.get("id") == subquestion_id:
            return subquestion

    return None


def _find_option_label(question_data, option_id):
    """
    Busca o texto da alternativa escolhida.
    """

    if not question_data:
        return str(option_id)

    for option in question_data.get("options", []):
        if option.get("id") == option_id:
            return option.get("label", str(option_id))

    return str(option_id)


def _find_option_data(question_data, option_id):
    """
    Busca os dados completos da alternativa escolhida.

    Diferente de _find_option_label, esta função retorna o dicionário
    inteiro da alternativa, permitindo acessar campos como:
    - label;
    - level;
    - id.
    """

    if not question_data:
        return None

    for option in question_data.get("options", []):
        if option.get("id") == option_id:
            return option

    return None


def _infer_direction_label(source_id, option_data):
    """
    Define a tendência visual exibida na tela de resultado.

    Essa função não altera a lógica da árvore.
    Ela apenas traduz o campo "level" da alternativa escolhida
    em uma mensagem explicativa para o usuário.
    """

    if not option_data:
        return "Influência registrada na classificação"

    level = option_data.get("level", "")

    # ------------------------------------------------------------
    # Bloco 1 — Perfil preliminar
    # ------------------------------------------------------------
    #
    # Neste bloco, as alternativas já apontam diretamente para
    # Conservador, Moderado ou Arrojado.

    if level == "conservador":
        return "Tendência: Conservador"

    if level == "moderado":
        return "Tendência: Moderado"

    if level == "arrojado":
        return "Tendência: Arrojado"

    # ------------------------------------------------------------
    # Bloco 2 — Situação financeira
    # ------------------------------------------------------------
    #
    # Aqui a leitura não é “desejo de perfil”, mas compatibilidade
    # financeira. Por isso usamos linguagem de limite prudencial.

    if level in [
        "necessidade_curto_prazo",
        "restricao_forte",
        "uso_relevante",
        "liquidez_essencial",
        "compromete_essencial",
        "reserva_insuficiente",
        "comprometeria_essenciais",
    ]:
        return "Tendência prudencial: Conservador"

    if level in [
        "moderacao",
        "uso_parcial",
        "liquidez_planejada",
        "liquidez_desejada",
        "impacto_parcial",
        "reserva_parcial",
        "prazo_curto_parcial",
        "incerteza",
    ]:
        return "Tendência prudencial: Moderado"

    if level in [
        "sem_necessidade_curto_prazo",
        "sem_restricao",
        "nao_compromete",
        "reserva_suficiente",
    ]:
        return "Não impõe limitação prudencial relevante"

    # ------------------------------------------------------------
    # Bloco 3 — Conhecimento e experiência
    # ------------------------------------------------------------
    #
    # Aqui a leitura é de sustentação ou limitação da classificação.

    if level in [
        "baixo_conhecimento",
        "baixa_experiencia",
        "sem_formacao_relacionada",
        "superficial",
        "nao_compreende_risco",
        "experiencia_episodica",
        "experiencia_simples",
    ]:
        return "Limita perfis mais altos"

    if level in [
        "conhecimento_intermediario",
        "experiencia_intermediaria",
        "contato_basico",
        "estudo_basico",
        "compreensao_parcial",
        "experiencia_moderada",
    ]:
        return "Sustenta perfil Moderado"

    if level in [
        "conhecimento_alto",
        "experiencia_alta",
        "formacao_relevante",
        "familiaridade_efetiva",
        "compreensao_adequada",
        "experiencia_continua",
        "experiencia_maior_oscilacao",
    ]:
        return "Sustenta perfis mais altos"

    return "Influência registrada na classificação"


def _profile_level(profile):
    """
    Retorna o nível ordinal do perfil.
    """

    if profile is None:
        return None

    return PROFILE_LEVELS.get(profile)


def _add_trace_item(
    trace,
    item_id,
    etapa,
    pergunta_evento,
    resposta,
    bloco,
    efeito,
    perfil_antes=None,
    perfil_depois=None,
    direcao=None,
):
    """
    Adiciona uma linha ao rastreamento da decisão.
    """

    trace.append(
        {
            "id": item_id,
            "etapa": etapa,
            "pergunta_evento": pergunta_evento,
            "resposta": resposta,
            "bloco": bloco,
            "efeito": efeito,
            "perfil_antes": perfil_antes,
            "perfil_depois": perfil_depois,
            "nivel_antes": _profile_level(perfil_antes),
            "nivel_depois": _profile_level(perfil_depois),
            "direcao": direcao,
        }
    )


def _add_question_trace(trace, question_id, answers, etapa, efeito):
    """
    Adiciona ao rastreamento uma pergunta principal respondida.
    """

    if question_id not in answers:
        return

    question_data = _find_question(question_id)
    answer_id = answers.get(question_id)
    
    option_data = _find_option_data(question_data, answer_id)
    direction_label = _infer_direction_label(question_id, option_data)

    _add_trace_item(
        trace=trace,
        item_id=question_id,
        etapa=etapa,
        pergunta_evento=question_data.get("text") if question_data else question_id,
        resposta=_find_option_label(question_data, answer_id),
        bloco=question_data.get("block") if question_data else "",
        efeito=efeito,
        direcao=direction_label,
    )


def _add_subquestion_trace(trace, subquestion_id, subanswers, etapa, efeito):
    """
    Adiciona ao rastreamento uma subpergunta respondida.
    """

    if subquestion_id not in subanswers:
        return

    subquestion_data = _find_subquestion(subquestion_id)
    answer_id = subanswers.get(subquestion_id)

    option_data = _find_option_data(subquestion_data, answer_id)
    direction_label = _infer_direction_label(subquestion_id, option_data)

    _add_trace_item(
        trace=trace,
        item_id=subquestion_id,
        etapa=etapa,
        pergunta_evento=subquestion_data.get("text") if subquestion_data else subquestion_id,
        resposta=_find_option_label(subquestion_data, answer_id),
        bloco=subquestion_data.get("block") if subquestion_data else "",
        efeito=efeito,
        direcao=direction_label,
    )


def build_decision_trace(
    answers,
    subanswers,
    preliminary_profile,
    financial_result,
    knowledge_result,
    final_profile,
):
    """
    Monta o rastreamento completo da árvore de decisão.

    Parâmetros:
    - answers: respostas das perguntas principais.
    - subanswers: respostas das subperguntas condicionais.
    - preliminary_profile: perfil gerado no bloco preliminar.
    - financial_result: resultado da compatibilidade financeira.
    - knowledge_result: resultado do refinamento por conhecimento.
    - final_profile: perfil final consolidado.

    Retorno:
    - lista de dicionários, cada um representando um passo do caminho decisório.
    """

    trace = []

    # ------------------------------------------------------------
    # Bloco 1 — Objetivos do investidor
    # ------------------------------------------------------------

    _add_question_trace(
        trace,
        "P1",
        answers,
        "Objetivos",
        "Contribui para identificar a finalidade principal do investimento.",
    )

    _add_question_trace(
        trace,
        "P2",
        answers,
        "Objetivos",
        "Contribui para identificar o horizonte temporal planejado.",
    )

    _add_subquestion_trace(
        trace,
        "2A",
        subanswers,
        "Objetivos",
        "Refina a interpretação do horizonte temporal informado.",
    )

    _add_question_trace(
        trace,
        "P3",
        answers,
        "Objetivos",
        "Contribui para identificar a tolerância declarada ao risco.",
    )

    _add_trace_item(
        trace=trace,
        item_id="perfil_preliminar",
        etapa="Objetivos",
        pergunta_evento="Perfil preliminar",
        resposta=preliminary_profile,
        bloco="Bloco 1 — Perfil preliminar",
        efeito="As respostas iniciais foram combinadas para formar a orientação inicial de perfil.",
        perfil_antes=None,
        perfil_depois=preliminary_profile,
    )

    # ------------------------------------------------------------
    # Bloco 2 — Situação financeira
    # ------------------------------------------------------------

    _add_question_trace(
        trace,
        "P4",
        answers,
        "Situação financeira",
        "Verifica se o valor pode ser necessário no curto prazo.",
    )

    _add_subquestion_trace(
        trace,
        "4A",
        subanswers,
        "Situação financeira",
        "Refina o impacto da necessidade futura sobre o valor investido.",
    )

    _add_subquestion_trace(
        trace,
        "4B",
        subanswers,
        "Situação financeira",
        "Refina o tipo de uso futuro do recurso.",
    )

    _add_question_trace(
        trace,
        "P5",
        answers,
        "Situação financeira",
        "Verifica a estabilidade de renda e a folga financeira.",
    )

    _add_subquestion_trace(
        trace,
        "5A",
        subanswers,
        "Situação financeira",
        "Refina o impacto de perdas ou imobilização sobre o orçamento.",
    )

    _add_question_trace(
        trace,
        "P6",
        answers,
        "Situação financeira",
        "Verifica a existência e suficiência da reserva financeira.",
    )

    _add_subquestion_trace(
        trace,
        "6A",
        subanswers,
        "Situação financeira",
        "Refina a suficiência da reserva para imprevistos.",
    )

    _add_subquestion_trace(
        trace,
        "6B",
        subanswers,
        "Situação financeira",
        "Refina o impacto de oscilações sobre despesas essenciais.",
    )

    financial_limit_profile = financial_result.get("financial_limit_profile")
    financial_profile = financial_result.get("profile")

    _add_trace_item(
        trace=trace,
        item_id="limite_financeiro",
        etapa="Situação financeira",
        pergunta_evento="Limite prudencial financeiro",
        resposta=financial_limit_profile,
        bloco="Bloco 2 — Compatibilidade financeira",
        efeito=financial_result.get(
            "reduction_reason",
            "A situação financeira foi analisada para definir o perfil máximo compatível.",
        ),
        perfil_antes=preliminary_profile,
        perfil_depois=financial_limit_profile,
    )

    _add_trace_item(
        trace=trace,
        item_id="perfil_apos_financas",
        etapa="Situação financeira",
        pergunta_evento="Perfil após compatibilidade financeira",
        resposta=financial_profile,
        bloco="Bloco 2 — Compatibilidade financeira",
        efeito="O perfil preliminar foi comparado ao limite financeiro e ajustado quando necessário.",
        perfil_antes=preliminary_profile,
        perfil_depois=financial_profile,
    )

    # ------------------------------------------------------------
    # Bloco 3 — Conhecimento e experiência
    # ------------------------------------------------------------

    _add_question_trace(
        trace,
        "P7",
        answers,
        "Conhecimento e experiência",
        "Verifica a familiaridade declarada com investimentos.",
    )

    _add_subquestion_trace(
        trace,
        "7A",
        subanswers,
        "Conhecimento e experiência",
        "Refina a origem da familiaridade declarada.",
    )

    _add_subquestion_trace(
        trace,
        "7B",
        subanswers,
        "Conhecimento e experiência",
        "Refina a compreensão sobre diferenças de risco.",
    )

    _add_question_trace(
        trace,
        "P8",
        answers,
        "Conhecimento e experiência",
        "Verifica a experiência prática com investimentos.",
    )

    _add_subquestion_trace(
        trace,
        "8A",
        subanswers,
        "Conhecimento e experiência",
        "Refina a frequência e consistência da experiência prática.",
    )

    _add_subquestion_trace(
        trace,
        "8B",
        subanswers,
        "Conhecimento e experiência",
        "Refina o tipo de investimento com o qual o usuário teve experiência.",
    )

    _add_question_trace(
        trace,
        "P9",
        answers,
        "Conhecimento e experiência",
        "Verifica formação ou experiência relacionada a finanças ou investimentos.",
    )

    knowledge_profile = knowledge_result.get("profile")

    _add_trace_item(
        trace=trace,
        item_id="perfil_apos_conhecimento",
        etapa="Conhecimento e experiência",
        pergunta_evento="Perfil após refinamento por conhecimento e experiência",
        resposta=knowledge_profile,
        bloco="Bloco 3 — Conhecimento e experiência",
        efeito=knowledge_result.get(
            "reduction_reason",
            "O conhecimento e a experiência foram analisados para confirmar ou ajustar a classificação.",
        ),
        perfil_antes=financial_profile,
        perfil_depois=knowledge_profile,
    )

    # ------------------------------------------------------------
    # Resultado final
    # ------------------------------------------------------------

    _add_trace_item(
        trace=trace,
        item_id="resultado_final",
        etapa="Resultado",
        pergunta_evento="Perfil final",
        resposta=final_profile,
        bloco="Resultado final",
        efeito="Resultado consolidado após a análise dos objetivos, da situação financeira e do conhecimento/experiência.",
        perfil_antes=knowledge_profile,
        perfil_depois=final_profile,
    )

    return trace

def _escape_dot_text(value):
    """
    Prepara textos para uso seguro em labels do Graphviz/DOT.

    O DOT usa aspas e barras invertidas com significado especial,
    por isso escapamos esses caracteres para evitar erro no fluxograma.
    """

    text = str(value or "")

    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')

    return text


def _shorten_text(text, max_length=90):
    """
    Reduz textos muito longos para não deixar o fluxograma ilegível.
    """

    text = str(text or "")

    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


def build_decision_flowchart(decision_trace):
    """
    Constrói uma representação DOT do percurso decisório.

    O fluxograma é gerado a partir do decision_trace, que contém
    perguntas, respostas, eventos intermediários e resultado final.

    Retorno:
    - string em formato DOT, pronta para uso em st.graphviz_chart.
    """

    lines = [
        "digraph decision_path {",
        "    rankdir=TB;",
        '    graph [fontsize=10, labelloc="t", label="Percurso da árvore de decisão"];',
        '    node [shape=box, style="rounded", fontsize=10];',
        '    edge [fontsize=9];',
    ]

    previous_node_id = None

    for index, item in enumerate(decision_trace):
        node_id = f"node_{index}"

        pergunta_evento = _shorten_text(item.get("pergunta_evento", ""))
        resposta = _shorten_text(item.get("resposta", ""))
        efeito = _shorten_text(item.get("efeito", ""))

        perfil_antes = item.get("perfil_antes")
        perfil_depois = item.get("perfil_depois")
        nivel_antes = item.get("nivel_antes")
        nivel_depois = item.get("nivel_depois")

        label_parts = [
            f"{item.get('etapa', '')}",
            f"{pergunta_evento}",
        ]

        if resposta:
            label_parts.append(f"Resposta: {resposta}")

        if perfil_antes or perfil_depois:
            label_parts.append(
                f"Perfil: {perfil_antes or '-'} → {perfil_depois or '-'}"
            )

        if nivel_antes or nivel_depois:
            label_parts.append(
                f"Nível: {nivel_antes or '-'} → {nivel_depois or '-'}"
            )

        if efeito:
            label_parts.append(f"Efeito: {efeito}")

        label = "\\n".join(_escape_dot_text(part) for part in label_parts)

        lines.append(f'    {node_id} [label="{label}"];')

        if previous_node_id is not None:
            lines.append(f"    {previous_node_id} -> {node_id};")

        previous_node_id = node_id

    lines.append("}")

    return "\n".join(lines)