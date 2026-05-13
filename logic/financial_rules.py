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


def _get_answer_value(answers, question_id):
    """
    Busca o valor numérico da resposta de uma pergunta principal.

    Parâmetros:
    - answers: dicionário com respostas principais.
      Exemplo: {"P4": 1, "P5": 2, "P6": 3}

    - question_id: identificador da pergunta.
      Exemplo: "P4"

    Retorno:
    - número inteiro da alternativa escolhida: 1, 2 ou 3.

    Se a resposta estiver ausente ou inválida, gera erro.
    """

    if question_id not in answers:
        raise ValueError(f"A pergunta {question_id} é obrigatória para aplicar a compatibilidade financeira.")

    value = answers.get(question_id)

    if value not in [1, 2, 3]:
        raise ValueError(f"A resposta da pergunta {question_id} deve ser 1, 2 ou 3.")

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
    p4 = _get_answer_value(answers, "P4")
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
        _add_event(
            strong_locks,
            "trava_forte",
            "P4",
            "Há necessidade declarada de utilizar o recurso em até 12 meses."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif p4 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P4",
            "Há possibilidade de necessidade do recurso entre 1 e 3 anos."
        )

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


def _define_reduction_steps(preliminary_profile, analysis):
    """
    Define se a compatibilidade financeira mantém ou reduz o perfil.

    Regras resumidas da Branch 3:
    - sem trava forte e sem combinação incompatível: mantém;
    - uma trava forte isolada ou duas moderações: reduz 1 nível;
    - liquidez forte + fragilidade financeira relevante: reduz 2 níveis;
    - perfil Arrojado fortemente contradito pelo bloco financeiro: reduz 2 níveis.
    """

    strong_locks = analysis["strong_locks"]
    moderations = analysis["moderations"]
    inconsistencies = analysis["inconsistencies"]

    strong_count = len(strong_locks)
    moderation_count = len(moderations)

    strong_sources = {event["source"] for event in strong_locks}

    # ---------------------------------------------------------------
    # Redução de 2 níveis
    # ---------------------------------------------------------------
    #
    # Cenários prudenciais mais fortes.
    # Eles representam combinação entre liquidez e fragilidade financeira.

    has_short_term_liquidity_lock = bool({"P4", "4A", "4B"} & strong_sources)
    has_financial_fragility_lock = bool({"P5", "5A", "P6", "6A", "6B"} & strong_sources)

    if has_short_term_liquidity_lock and has_financial_fragility_lock:
        return 2, "Combinação de trava forte de liquidez com fragilidade financeira relevante."

    if strong_count >= 3:
        return 2, "Acúmulo de múltiplas travas financeiras fortes."

    if preliminary_profile == PROFILE_ARROJADO and strong_count >= 2:
        return 2, "Perfil preliminar Arrojado contradito por múltiplas travas financeiras fortes."

    if preliminary_profile == PROFILE_ARROJADO and inconsistencies and strong_count >= 1:
        return 2, "Perfil preliminar Arrojado contradito por inconsistência financeira relevante."

    # ---------------------------------------------------------------
    # Redução de 1 nível
    # ---------------------------------------------------------------
    #
    # Cenários moderados ou com uma trava forte isolada.

    if strong_count >= 1:
        return 1, "Presença de trava financeira forte isolada."

    if moderation_count >= 2:
        return 1, "Combinação de duas ou mais moderações financeiras."

    # ---------------------------------------------------------------
    # Manutenção
    # ---------------------------------------------------------------

    return 0, "Não foram identificadas travas financeiras suficientes para reduzir o perfil."


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

    # Define quantos níveis o perfil deve ser reduzido.
    reduction_steps, reduction_reason = _define_reduction_steps(
        preliminary_profile=preliminary_profile,
        analysis=analysis,
    )

    # Aplica a redução ao perfil preliminar.
    adjusted_profile = reduce_profile(preliminary_profile, reduction_steps)

    # Recalcula a redução efetiva real.
    # Isso evita registrar redução quando o perfil já estava no piso (Conservador).
    input_index = PROFILE_ORDER.index(preliminary_profile)
    output_index = PROFILE_ORDER.index(adjusted_profile)
    effective_reduction_steps = input_index - output_index

    # Se o perfil Arrojado estiver bloqueado, garantimos que a saída
    # da compatibilidade financeira não permaneça como Arrojado.
    if PROFILE_ARROJADO in analysis["blocked_profiles"] and adjusted_profile == PROFILE_ARROJADO:
        adjusted_profile = PROFILE_MODERADO
        reduction_reason = "Perfil Arrojado bloqueado por incompatibilidade financeira."

    # Recalcula a redução efetiva real depois de todos os ajustes prudenciais.
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
    }