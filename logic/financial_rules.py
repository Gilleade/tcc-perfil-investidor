# Importa os nomes oficiais dos perfis usados no protótipo.
# Eles foram definidos no arquivo de perfil preliminar.
from logic.preliminary_profile import (
    PROFILE_CONSERVADOR,
    PROFILE_MODERADO,
    PROFILE_ARROJADO,
)


# Ordem dos perfis do menor para o maior nível de exposição.
#
# Essa lista será usada para reduzir o perfil de forma controlada.
# Exemplo:
# Arrojado reduzido 1 nível -> Moderado
# Arrojado reduzido 2 níveis -> Conservador
# Moderado reduzido 1 nível -> Conservador
PROFILE_ORDER = [
    PROFILE_CONSERVADOR,
    PROFILE_MODERADO,
    PROFILE_ARROJADO,
]

PROFILE_LEVELS = {
    PROFILE_CONSERVADOR: 1,
    PROFILE_MODERADO: 2,
    PROFILE_ARROJADO: 3,
}

LEVEL_TO_PROFILE = {
    1: PROFILE_CONSERVADOR,
    2: PROFILE_MODERADO,
    3: PROFILE_ARROJADO,
}


def _get_answer_value(answers, question_id, allowed_values=None):
    """
    Busca o valor numérico da resposta de uma pergunta principal.

    Parâmetros:
    - answers: dicionário com respostas principais.
      Exemplo: {"P4": 1, "P5": 2, "P6": 3}

    - question_id: identificador da pergunta.
      Exemplo: "P4"

    - allowed_values: lista opcional de alternativas válidas.
      Exemplo: [1, 2] para perguntas Sim/Não.

    Retorno:
    - número inteiro da alternativa escolhida.

    Se a resposta estiver ausente ou inválida, gera erro.
    """

    if question_id not in answers:
        raise ValueError(
            f"A pergunta {question_id} é obrigatória para aplicar a compatibilidade financeira."
        )

    value = answers.get(question_id)

    if allowed_values is None:
        allowed_values = [1, 2, 3]

    if value not in allowed_values:
        raise ValueError(
            f"A resposta da pergunta {question_id} deve estar entre {allowed_values}."
        )

    return value


def _get_subanswer_value(subanswers, subquestion_id):
    """
    Busca uma resposta de subpergunta condicional.

    Parâmetros:
    - subanswers: dicionário com respostas das subperguntas.
      Exemplo: {"4A": 1, "4B": 2}

    - subquestion_id: identificador da subpergunta.
      Exemplo: "4A"

    Retorno:
    - número da alternativa escolhida;
    - None, se a subpergunta não foi ativada ou não foi respondida.

    Observação:
    As subperguntas já foram validadas na Etapa 8.
    Portanto, aqui apenas lemos o valor quando ele existir.
    """

    return subanswers.get(subquestion_id)


def reduce_profile(profile, levels=1):
    """
    Reduz o perfil em um ou mais níveis.

    Parâmetros:
    - profile: perfil atual.
      Exemplo: "Arrojado"

    - levels: quantidade de níveis de redução.
      Exemplo: 1 ou 2

    Retorno:
    - perfil reduzido.

    Exemplos:
    - Arrojado + redução 1 -> Moderado
    - Arrojado + redução 2 -> Conservador
    - Moderado + redução 1 -> Conservador
    - Conservador + redução 1 -> Conservador
    """

    if profile not in PROFILE_ORDER:
        raise ValueError(f"Perfil inválido: {profile}")

    current_index = PROFILE_ORDER.index(profile)

    # Garante que o índice nunca fique abaixo de 0.
    new_index = max(0, current_index - levels)

    return PROFILE_ORDER[new_index]


def _add_event(events, event_type, source, message):
    """
    Adiciona um evento lógico à lista de eventos financeiros.

    Essa estrutura ajuda a registrar por que o perfil foi mantido,
    reduzido ou bloqueado.

    Parâmetros:
    - events: lista que receberá o evento.
    - event_type: tipo do evento, como "trava_forte" ou "moderacao".
    - source: origem do evento, como "P4", "4A" ou "6B".
    - message: explicação textual do evento.
    """

    events.append(
        {
            "type": event_type,
            "source": source,
            "message": message,
        }
    )


def _analyze_financial_answers(answers, subanswers):
    """
    Analisa P4, P5, P6 e subperguntas financeiras.

    Retorno:
    Um dicionário com:
    - strong_locks: travas fortes encontradas;
    - moderations: moderações encontradas;
    - inconsistencies: inconsistências ou pontos de atenção;
    - blocked_profiles: perfis bloqueados por prudência.

    Esta função não reduz o perfil diretamente.
    Ela apenas identifica sinais financeiros.
    """

    # Respostas principais do Bloco 2.
    p4 = _get_answer_value(answers, "P4", allowed_values=[1, 2])
    p5 = _get_answer_value(answers, "P5")
    p6 = _get_answer_value(answers, "P6")

    # Respostas de subperguntas financeiras.
    sub_4a = _get_subanswer_value(subanswers, "4A")
    sub_4b = _get_subanswer_value(subanswers, "4B")
    sub_5a = _get_subanswer_value(subanswers, "5A")
    sub_6a = _get_subanswer_value(subanswers, "6A")
    sub_6b = _get_subanswer_value(subanswers, "6B")

    strong_locks = []
    moderations = []
    inconsistencies = []
    blocked_profiles = []

    # ---------------------------------------------------------------
    # P4 — Necessidade futura de recursos
    # ---------------------------------------------------------------
    #
    # P4 = 1 indica necessidade do recurso em até 12 meses.
    # Esse é um sinal prudencial forte, especialmente se a maior parte
    # do valor será usada ou se o uso está ligado a despesa essencial.

    if p4 == 1:
        # Se o usuário pode precisar do valor no curto prazo,
        # mas possui renda estável e reserva suficiente,
        # a situação financeira limita o perfil máximo a Moderado,
        # em vez de reduzir diretamente para Conservador.
        if p5 == 3 and p6 == 3:
            _add_event(
                moderations,
                "moderacao",
                "P4",
                "Há possibilidade de necessidade do valor no curto prazo, mas a renda estável e a reserva suficiente permitem limitar o perfil a Moderado."
            )

            if PROFILE_ARROJADO not in blocked_profiles:
                blocked_profiles.append(PROFILE_ARROJADO)

        else:
            _add_event(
                strong_locks,
                "trava_forte",
                "P4",
                "Há possibilidade de necessidade do valor no curto prazo sem robustez financeira suficiente."
            )

            if PROFILE_ARROJADO not in blocked_profiles:
                blocked_profiles.append(PROFILE_ARROJADO)

    # Subpergunta 4A: uso relevante da maior parte do valor.
    if sub_4a == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "4A",
            "A necessidade futura comprometerá parte relevante do valor investido."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_4a in [2, 3]:
        _add_event(
            moderations,
            "moderacao",
            "4A",
            "A necessidade futura não foi caracterizada como totalmente livre de restrição."
        )

    # Subpergunta 4B: tipo de uso futuro do recurso.
    if sub_4b == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "4B",
            "O uso futuro do recurso está associado a despesas essenciais."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_4b == 2:
        _add_event(
            moderations,
            "moderacao",
            "4B",
            "O uso futuro do recurso está associado a compromisso já previsto."
        )

    elif sub_4b == 3:
        _add_event(
            moderations,
            "moderacao",
            "4B",
            "O uso futuro foi indicado como conveniência eventual, gerando apenas moderação leve."
        )

    # ---------------------------------------------------------------
    # P5 — Estabilidade de renda
    # ---------------------------------------------------------------
    #
    # P5 = 1 indica renda instável ou pouca folga financeira.
    # Pela modelagem, isso pode gerar moderação ou trava forte
    # quando a subpergunta aponta comprometimento do orçamento essencial.

    if p5 == 1:
        _add_event(
            moderations,
            "moderacao",
            "P5",
            "A renda foi declarada como instável ou com pouca folga financeira."
        )

    elif p5 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P5",
            "A renda foi declarada como relativamente estável, mas apenas com alguma folga."
        )

    # Subpergunta 5A: impacto no orçamento essencial.
    if sub_5a == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "5A",
            "Uma perda temporária ou imobilização do recurso comprometeria o orçamento essencial."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_5a == 2:
        _add_event(
            moderations,
            "moderacao",
            "5A",
            "Uma perda temporária afetaria parcialmente o orçamento, sem comprometer o essencial."
        )

    elif sub_5a == 3:
        # P5 já registra moderação quando renda = 1.
        # Aqui apenas registramos observação positiva, sem remover a moderação original.
        pass

    # ---------------------------------------------------------------
    # P6 — Reserva financeira / robustez patrimonial
    # ---------------------------------------------------------------
    #
    # P6 = 1 indica ausência de reserva suficiente.
    # A Branch 3 definiu isso como trava forte para perfil alto.
    #
    # P6 = 2 indica reserva parcial, funcionando como moderação.

    if p6 == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "P6",
            "Não há reserva financeira suficiente para suportar oscilações."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif p6 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P6",
            "Há reserva parcial, mas com limitações."
        )

    # Subpergunta 6A: dependência do investimento para imprevistos.
    if sub_6a == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "6A",
            "A reserva atual não seria suficiente para lidar com imprevistos sem depender do investimento."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_6a == 2:
        _add_event(
            moderations,
            "moderacao",
            "6A",
            "A reserva seria apenas parcialmente suficiente para lidar com imprevistos."
        )

    # Subpergunta 6B: impacto de oscilação relevante.
    if sub_6b == 1:
        _add_event(
            strong_locks,
            "trava_forte",
            "6B",
            "Uma oscilação relevante comprometeria despesas essenciais."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_6b == 2:
        _add_event(
            moderations,
            "moderacao",
            "6B",
            "Uma oscilação relevante reduziria a margem de conforto."
        )

    # ---------------------------------------------------------------
    # Inconsistências financeiras combinadas
    # ---------------------------------------------------------------
    #
    # Algumas combinações merecem registro porque indicam conflito forte
    # entre liquidez, renda e reserva.

    if p4 == 1 and p6 == 1:
        inconsistencies.append(
            "Necessidade de uso do recurso em até 12 meses combinada com ausência de reserva suficiente."
        )

    if p4 == 1 and p5 == 1 and p6 in [1, 2]:
        inconsistencies.append(
            "Necessidade de liquidez, renda instável e reserva insuficiente ou parcial indicam fragilidade financeira relevante."
        )

    if sub_4b == 1 and sub_6b == 1:
        inconsistencies.append(
            "Uso essencial do recurso combinado com possibilidade de comprometimento de despesas essenciais em caso de oscilação."
        )

    return {
        "strong_locks": strong_locks,
        "moderations": moderations,
        "inconsistencies": inconsistencies,
        "blocked_profiles": blocked_profiles,
    }


def _define_financial_limit_profile(answers, subanswers, analysis):
    """
    Define o perfil máximo compatível com a situação financeira.

    Essa função representa o limite prudencial financeiro.

    Em vez de decidir o perfil final diretamente, ela define até qual
    perfil a situação financeira permite chegar.

    Exemplos:
    - Limite Arrojado: sem restrição financeira relevante.
    - Limite Moderado: há restrição financeira moderada.
    - Limite Conservador: há fragilidade financeira relevante.
    """

    p4 = _get_answer_value(answers, "P4", allowed_values=[1, 2])
    p5 = _get_answer_value(answers, "P5")
    p6 = _get_answer_value(answers, "P6")

    sub_4a = _get_subanswer_value(subanswers, "4A")
    sub_4b = _get_subanswer_value(subanswers, "4B")
    sub_5a = _get_subanswer_value(subanswers, "5A")
    sub_6a = _get_subanswer_value(subanswers, "6A")
    sub_6b = _get_subanswer_value(subanswers, "6B")

    strong_locks = analysis["strong_locks"]
    moderations = analysis["moderations"]

    strong_count = len(strong_locks)
    moderation_count = len(moderations)

    # ---------------------------------------------------------------
    # Limite Conservador
    # ---------------------------------------------------------------
    #
    # O perfil máximo passa a ser Conservador quando a situação financeira
    # indica dependência relevante do recurso, ausência de reserva suficiente
    # ou possibilidade de comprometimento de despesas essenciais.

    if sub_4a == 1 or sub_4b == 1:
        return (
            PROFILE_CONSERVADOR,
            "Necessidade do valor no curto prazo associada a uso relevante ou despesa essencial."
        )

    if p4 == 1 and (p5 == 1 or p6 == 1):
        return (
            PROFILE_CONSERVADOR,
            "Possibilidade de necessidade do valor no curto prazo combinada com fragilidade de renda ou reserva."
        )

    if sub_5a == 1:
        return (
            PROFILE_CONSERVADOR,
            "Possível perda temporária ou imobilização do recurso comprometeria o orçamento essencial."
        )

    if p6 == 1 and (sub_6a == 1 or sub_6b == 1):
        return (
            PROFILE_CONSERVADOR,
            "Ausência de reserva suficiente combinada com dependência do investimento ou comprometimento de despesas essenciais."
        )

    if strong_count >= 3:
        return (
            PROFILE_CONSERVADOR,
            "Acúmulo de múltiplas travas financeiras fortes."
        )

    # ---------------------------------------------------------------
    # Limite Moderado
    # ---------------------------------------------------------------
    #
    # O perfil máximo passa a ser Moderado quando há restrições financeiras
    # relevantes, mas não suficientes para caracterizar fragilidade severa.

    if p4 == 1:
        return (
            PROFILE_MODERADO,
            "Possibilidade de necessidade do valor no curto prazo, com condição financeira suficiente para evitar classificação conservadora."
        )

    if p5 == 2 or p6 == 2:
        return (
            PROFILE_MODERADO,
            "Renda ou reserva financeira parcialmente adequada, exigindo limitação prudencial do perfil."
        )

    if moderation_count >= 2:
        return (
            PROFILE_MODERADO,
            "Combinação de duas ou mais moderações financeiras."
        )

    if strong_count >= 1:
        return (
            PROFILE_MODERADO,
            "Presença de restrição financeira pontual."
        )

    # ---------------------------------------------------------------
    # Sem limitação financeira relevante
    # ---------------------------------------------------------------

    return (
        PROFILE_ARROJADO,
        "Não foram identificadas restrições financeiras suficientes para limitar o perfil."
    )


def apply_financial_compatibility(preliminary_profile, answers, subanswers):
    """
    Aplica a compatibilidade financeira ao perfil preliminar.

    Parâmetros:
    - preliminary_profile: perfil gerado pelo Bloco 1.
      Exemplo: "Arrojado"

    - answers: respostas das perguntas principais.
      Deve conter P4, P5 e P6.

    - subanswers: respostas das subperguntas condicionais.
      Pode conter 4A, 4B, 5A, 6A e 6B.

    Retorno:
    Um dicionário com:
    - perfil de entrada;
    - perfil após compatibilidade financeira;
    - quantidade de níveis reduzidos;
    - travas fortes;
    - moderações;
    - perfis bloqueados;
    - inconsistências;
    - registro lógico.
    """

    if preliminary_profile not in PROFILE_ORDER:
        raise ValueError(f"Perfil preliminar inválido: {preliminary_profile}")

    # Analisa as respostas financeiras e identifica sinais.
    analysis = _analyze_financial_answers(answers, subanswers)

    # Define o perfil máximo compatível com a situação financeira.
    financial_limit_profile, reduction_reason = _define_financial_limit_profile(
        answers=answers,
        subanswers=subanswers,
        analysis=analysis,
    )

    # Aplica o limite prudencial:
    # o perfil após finanças nunca pode ser maior que o limite financeiro.
    preliminary_level = PROFILE_LEVELS[preliminary_profile]
    financial_limit_level = PROFILE_LEVELS[financial_limit_profile]

    adjusted_level = min(preliminary_level, financial_limit_level)
    adjusted_profile = LEVEL_TO_PROFILE[adjusted_level]

    # Recalcula a redução efetiva real.
    # Isso evita registrar redução quando o perfil já estava no piso (Conservador).
    input_index = PROFILE_ORDER.index(preliminary_profile)
    output_index = PROFILE_ORDER.index(adjusted_profile)
    effective_reduction_steps = input_index - output_index

    # Monta registro lógico para uso futuro na justificativa textual.
    logical_log = []

    if effective_reduction_steps == 0:
        logical_log.append(
            "A compatibilidade financeira manteve o perfil preliminar. "
            "Mesmo com eventuais restrições registradas, não houve redução efetiva do perfil final desta etapa."
        )
    elif effective_reduction_steps == 1:
        logical_log.append(
            f"A compatibilidade financeira reduziu o perfil em 1 nível. Motivo: {reduction_reason}"
        )
    else:
        logical_log.append(
            f"A compatibilidade financeira reduziu o perfil em 2 níveis. Motivo: {reduction_reason}"
        )

    if analysis["blocked_profiles"]:
        logical_log.append(
            "Houve bloqueio prudencial de perfil alto em razão de restrições financeiras identificadas."
        )

    if analysis["inconsistencies"]:
        logical_log.append(
            "Foram identificadas inconsistências financeiras relevantes para a justificativa final."
        )

    return {
        "stage": "compatibilidade_financeira",
        "input_profile": preliminary_profile,
        "profile": adjusted_profile,
        "reduction_steps": effective_reduction_steps,
        "reduction_reason": reduction_reason,
        "strong_locks": analysis["strong_locks"],
        "moderations": analysis["moderations"],
        "blocked_profiles": analysis["blocked_profiles"],
        "inconsistencies": analysis["inconsistencies"],
        "log": logical_log,
        "financial_limit_profile": financial_limit_profile,
        "financial_limit_level": financial_limit_level,
        "input_profile_level": preliminary_level,
        "output_profile_level": adjusted_level,
    }