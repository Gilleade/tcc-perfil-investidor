# Importa os nomes oficiais dos perfis usados no protótipo.
from logic.preliminary_profile import (
    PROFILE_CONSERVADOR,
    PROFILE_MODERADO,
    PROFILE_ARROJADO,
)


# Ordem dos perfis do menor para o maior nível.
#
# Esta ordem será usada para reduzir o perfil quando conhecimento
# e experiência forem insuficientes para sustentar o perfil atual.
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
      Exemplo: {"P7": 2, "P8": 1, "P9": 3}

    - question_id: identificador da pergunta.
      Exemplo: "P7"

    Retorno:
    - número inteiro da alternativa escolhida: 1, 2 ou 3.

    Se a resposta estiver ausente ou inválida, gera erro.
    """

    if question_id not in answers:
        raise ValueError(f"A pergunta {question_id} é obrigatória para aplicar o refinamento por conhecimento.")

    value = answers.get(question_id)

    if value not in [1, 2, 3]:
        raise ValueError(f"A resposta da pergunta {question_id} deve ser 1, 2 ou 3.")

    return value


def _get_subanswer_value(subanswers, subquestion_id):
    """
    Busca uma resposta de subpergunta condicional.

    Parâmetros:
    - subanswers: dicionário com respostas das subperguntas.
      Exemplo: {"7A": 3, "7B": 2}

    - subquestion_id: identificador da subpergunta.
      Exemplo: "7A"

    Retorno:
    - número da alternativa escolhida;
    - None, se a subpergunta não foi ativada ou não foi respondida.

    Observação:
    As subperguntas já foram validadas antes.
    Aqui apenas lemos o valor quando ele existir.
    """

    return subanswers.get(subquestion_id)


def _reduce_profile(profile, levels=1):
    """
    Reduz o perfil em um ou mais níveis.

    Exemplos:
    - Arrojado reduzido 1 nível -> Moderado
    - Arrojado reduzido 2 níveis -> Conservador
    - Moderado reduzido 1 nível -> Conservador
    - Conservador reduzido 1 nível -> Conservador

    Esta função não eleva perfil.
    """

    if profile not in PROFILE_ORDER:
        raise ValueError(f"Perfil inválido: {profile}")

    current_index = PROFILE_ORDER.index(profile)
    new_index = max(0, current_index - levels)

    return PROFILE_ORDER[new_index]


def _add_event(events, event_type, source, message):
    """
    Adiciona um evento lógico à lista de eventos de conhecimento.

    Esse registro será útil depois para montar a justificativa textual.
    """

    events.append(
        {
            "type": event_type,
            "source": source,
            "message": message,
        }
    )


def _analyze_knowledge_answers(answers, subanswers):
    """
    Analisa P7, P8, P9 e subperguntas de conhecimento/experiência.

    Retorno:
    Um dicionário com:
    - limitations: limitações fortes;
    - moderations: sinais intermediários;
    - confirmations: sinais positivos;
    - inconsistencies: conflitos ou pontos de atenção;
    - blocked_profiles: perfis bloqueados por prudência.

    Esta função ainda não reduz o perfil.
    Ela apenas identifica os sinais do eixo de conhecimento.
    """

    # Respostas principais do Bloco 3.
    p7 = _get_answer_value(answers, "P7")
    p8 = _get_answer_value(answers, "P8")
    p9 = _get_answer_value(answers, "P9")

    # Respostas de subperguntas relacionadas a conhecimento e experiência.
    sub_7a = _get_subanswer_value(subanswers, "7A")
    sub_7b = _get_subanswer_value(subanswers, "7B")
    sub_8a = _get_subanswer_value(subanswers, "8A")
    sub_8b = _get_subanswer_value(subanswers, "8B")

    limitations = []
    moderations = []
    confirmations = []
    inconsistencies = []
    blocked_profiles = []

    # ---------------------------------------------------------------
    # P7 — Familiaridade com investimentos
    # ---------------------------------------------------------------
    #
    # P7 = 1 indica baixa familiaridade.
    # Isso é uma limitação forte, principalmente para perfis mais altos.

    if p7 == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "P7",
            "Foi declarada pouca ou nenhuma familiaridade com investimentos além de alternativas simples."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif p7 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P7",
            "Foi declarada familiaridade intermediária com algumas opções de investimento e riscos básicos."
        )

    elif p7 == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "P7",
            "Foi declarada familiaridade com produtos de maior oscilação e seus riscos."
        )

    # Subpergunta 7A — origem da familiaridade.
    if sub_7a == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "7A",
            "A familiaridade declarada foi caracterizada como conhecimento superficial."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_7a == 2:
        _add_event(
            moderations,
            "moderacao",
            "7A",
            "A familiaridade decorre de estudo próprio ou acompanhamento básico."
        )

    elif sub_7a == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "7A",
            "A familiaridade decorre de experiência prática ou estudo consistente."
        )

    # Subpergunta 7B — compreensão de diferenças de risco.
    if sub_7b == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "7B",
            "O usuário não se considera capaz de compreender diferenças de risco entre alternativas estáveis e alternativas de maior oscilação."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_7b == 2:
        _add_event(
            moderations,
            "moderacao",
            "7B",
            "O usuário declarou compreender parcialmente as diferenças de risco."
        )

    elif sub_7b == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "7B",
            "O usuário declarou compreender adequadamente as diferenças de risco."
        )

    # ---------------------------------------------------------------
    # P8 — Experiência prática com investimentos
    # ---------------------------------------------------------------
    #
    # P8 = 1 indica baixa experiência prática.
    # Isso limita principalmente perfis mais altos.

    if p8 == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "P8",
            "Foi declarada ausência de experiência ou experiência recente e rara com investimentos."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif p8 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P8",
            "Foi declarada experiência intermediária, com alguma regularidade."
        )

    elif p8 == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "P8",
            "Foi declarada experiência prática mais longa e frequente com investimentos."
        )

    # Subpergunta 8A — continuidade da experiência.
    if sub_8a == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "8A",
            "A experiência foi caracterizada como episódica."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_8a == 2:
        _add_event(
            moderations,
            "moderacao",
            "8A",
            "A experiência foi caracterizada como moderadamente regular."
        )

    elif sub_8a == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "8A",
            "A experiência foi caracterizada como contínua e deliberada."
        )

    # Subpergunta 8B — tipo de alternativa já experimentada.
    if sub_8b == 1:
        _add_event(
            limitations,
            "limitacao_forte",
            "8B",
            "A experiência incluiu apenas alternativas mais simples."
        )

        if PROFILE_ARROJADO not in blocked_profiles:
            blocked_profiles.append(PROFILE_ARROJADO)

    elif sub_8b == 2:
        _add_event(
            moderations,
            "moderacao",
            "8B",
            "A experiência incluiu algumas alternativas com oscilação moderada."
        )

    elif sub_8b == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "8B",
            "A experiência incluiu alternativas de maior oscilação."
        )

    # ---------------------------------------------------------------
    # P9 — Formação ou experiência profissional relacionada
    # ---------------------------------------------------------------
    #
    # P9 é complementar.
    # Ele pode confirmar conhecimento, mas não deve elevar perfil sozinho.

    if p9 == 1:
        _add_event(
            moderations,
            "moderacao",
            "P9",
            "Não foi declarada formação ou experiência profissional relacionada."
        )

    elif p9 == 2:
        _add_event(
            moderations,
            "moderacao",
            "P9",
            "Foi declarado contato indireto ou básico com finanças, investimentos ou áreas próximas."
        )

    elif p9 == 3:
        _add_event(
            confirmations,
            "confirmacao",
            "P9",
            "Foi declarada formação ou experiência direta e relevante relacionada a finanças, investimentos ou áreas próximas."
        )

    # ---------------------------------------------------------------
    # Inconsistências do eixo de conhecimento
    # ---------------------------------------------------------------
    #
    # Aqui registramos conflitos ou pontos que exigem cautela.

    if p7 == 3 and sub_7b == 1:
        inconsistencies.append(
            "Foi declarada familiaridade alta, mas a subpergunta indicou incapacidade de compreender diferenças de risco."
        )

    if p8 == 3 and sub_8a == 1:
        inconsistencies.append(
            "Foi declarada experiência alta, mas a subpergunta indicou experiência apenas episódica."
        )

    if p8 == 3 and sub_8b == 1:
        inconsistencies.append(
            "Foi declarada experiência alta, mas restrita a alternativas simples."
        )

    if p9 == 3 and p7 == 1 and p8 == 1:
        inconsistencies.append(
            "Foi declarada formação ou experiência relacionada, mas com baixa familiaridade e baixa experiência prática informadas."
        )

    return {
        "limitations": limitations,
        "moderations": moderations,
        "confirmations": confirmations,
        "inconsistencies": inconsistencies,
        "blocked_profiles": blocked_profiles,
    }


def _define_knowledge_reduction_steps(current_profile, analysis):
    """
    Define se o perfil será mantido ou reduzido pelo eixo de conhecimento.

    Regras adotadas:
    - conhecimento/experiência não eleva perfil;
    - limitações fortes podem reduzir perfil;
    - múltiplas limitações fortes podem reduzir dois níveis;
    - perfil Arrojado exige confirmação mais robusta de conhecimento e experiência;
    - perfil Moderado pode ser mantido com conhecimento intermediário adequado.
    """

    limitations = analysis["limitations"]
    moderations = analysis["moderations"]
    inconsistencies = analysis["inconsistencies"]

    limitation_count = len(limitations)
    moderation_count = len(moderations)

    limitation_sources = {event["source"] for event in limitations}

    has_low_familiarity = bool({"P7", "7A", "7B"} & limitation_sources)
    has_low_experience = bool({"P8", "8A", "8B"} & limitation_sources)

    # ---------------------------------------------------------------
    # Redução de 2 níveis
    # ---------------------------------------------------------------
    #
    # A redução de dois níveis é reservada para situações fortes,
    # principalmente quando o perfil atual é Arrojado e há baixa
    # familiaridade combinada com baixa experiência prática.

    if current_profile == PROFILE_ARROJADO and has_low_familiarity and has_low_experience:
        return 2, "Perfil Arrojado incompatível com baixa familiaridade e baixa experiência prática."

    if current_profile == PROFILE_ARROJADO and limitation_count >= 3:
        return 2, "Perfil Arrojado contradito por múltiplas limitações fortes de conhecimento e experiência."

    # ---------------------------------------------------------------
    # Redução de 1 nível
    # ---------------------------------------------------------------
    #
    # Uma limitação forte reduz o perfil em um nível.
    # Exemplo: baixa familiaridade, baixa experiência ou compreensão inadequada de risco.

    if limitation_count >= 1:
        return 1, "Presença de limitação forte no eixo de conhecimento e experiência."

    # Para perfil Arrojado, múltiplas moderações indicam que o conhecimento
    # e a experiência não confirmam suficientemente o perfil alto.
    #
    # Porém, para perfil Moderado, conhecimento intermediário é compatível
    # e não deve reduzir automaticamente para Conservador.

    if current_profile == PROFILE_ARROJADO and moderation_count >= 2:
        return 1, "Perfil Arrojado exige maior confirmação de conhecimento e experiência."

    if inconsistencies and current_profile == PROFILE_ARROJADO:
        return 1, "Inconsistência relevante no eixo de conhecimento para perfil Arrojado."

    # ---------------------------------------------------------------
    # Manutenção
    # ---------------------------------------------------------------

    return 0, "Conhecimento e experiência suficientes para manter o perfil atual."


def apply_knowledge_refinement(current_profile, answers, subanswers):
    """
    Aplica o refinamento por conhecimento e experiência.

    Parâmetros:
    - current_profile: perfil vindo da compatibilidade financeira.
      Exemplo: "Moderado"

    - answers: respostas das perguntas principais.
      Deve conter P7, P8 e P9.

    - subanswers: respostas das subperguntas condicionais.
      Pode conter 7A, 7B, 8A e 8B.

    Retorno:
    Um dicionário com:
    - perfil de entrada;
    - perfil após refinamento;
    - quantidade de níveis reduzidos;
    - limitações;
    - moderações;
    - confirmações;
    - perfis bloqueados;
    - inconsistências;
    - registro lógico.
    """

    if current_profile not in PROFILE_ORDER:
        raise ValueError(f"Perfil atual inválido: {current_profile}")

    # Analisa respostas do eixo de conhecimento/experiência.
    analysis = _analyze_knowledge_answers(answers, subanswers)

    # Define quantos níveis o perfil deve ser reduzido.
    reduction_steps, reduction_reason = _define_knowledge_reduction_steps(
        current_profile=current_profile,
        analysis=analysis,
    )

    # Aplica a redução.
    refined_profile = _reduce_profile(current_profile, reduction_steps)

    # Recalcula a redução efetiva real.
    # Isso evita registrar redução quando o perfil já estava no piso.
    input_index = PROFILE_ORDER.index(current_profile)
    output_index = PROFILE_ORDER.index(refined_profile)
    effective_reduction_steps = input_index - output_index

    # Se o perfil Arrojado estiver bloqueado, garantimos que o resultado
    # deste bloco não permaneça como Arrojado.
    if PROFILE_ARROJADO in analysis["blocked_profiles"] and refined_profile == PROFILE_ARROJADO:
        refined_profile = PROFILE_MODERADO
        reduction_reason = "Perfil Arrojado bloqueado por limitação de conhecimento ou experiência."

    # Recalcula a redução efetiva real depois de todos os ajustes prudenciais.
    input_index = PROFILE_ORDER.index(current_profile)
    output_index = PROFILE_ORDER.index(refined_profile)
    effective_reduction_steps = input_index - output_index

    # Monta log lógico para justificativa futura.
    logical_log = []

    if effective_reduction_steps == 0:
        logical_log.append(
            "O refinamento por conhecimento e experiência manteve o perfil atual. "
            "Mesmo com eventuais limitações registradas, não houve redução efetiva do perfil nesta etapa."
        )
    elif effective_reduction_steps == 1:
        logical_log.append(
            f"O refinamento por conhecimento e experiência reduziu o perfil em 1 nível. Motivo: {reduction_reason}"
        )
    else:
        logical_log.append(
            f"O refinamento por conhecimento e experiência reduziu o perfil em 2 níveis. Motivo: {reduction_reason}"
        )

    # Só registramos bloqueio prudencial de perfil alto quando o perfil de entrada era Arrojado.
    # Assim evitamos mensagens confusas quando o perfil já era Moderado ou Conservador.
    if current_profile == PROFILE_ARROJADO and analysis["blocked_profiles"]:
        logical_log.append(
            "Houve bloqueio prudencial de perfil alto em razão de limitações de conhecimento ou experiência."
        )

    if analysis["inconsistencies"]:
        logical_log.append(
            "Foram identificadas inconsistências no eixo de conhecimento e experiência."
        )

    return {
        "stage": "refinamento_conhecimento_experiencia",
        "input_profile": current_profile,
        "profile": refined_profile,
        "reduction_steps": effective_reduction_steps,
        "reduction_reason": reduction_reason,
        "limitations": analysis["limitations"],
        "moderations": analysis["moderations"],
        "confirmations": analysis["confirmations"],
        "blocked_profiles": analysis["blocked_profiles"],
        "inconsistencies": analysis["inconsistencies"],
        "log": logical_log,
    }