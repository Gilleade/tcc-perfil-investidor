# Este arquivo é responsável por gerar a justificativa textual da classificação.
#
# Ele não calcula o perfil.
# Ele recebe o resultado já consolidado pela função consolidate_final_profile()
# e transforma os registros lógicos em texto claro e rastreável.

def _format_levels(quantity):
    """
    Formata corretamente a palavra nível no singular ou plural.

    Exemplos:
    - 1 -> "1 nível"
    - 2 -> "2 níveis"
    """

    if quantity == 1:
        return "1 nível"

    return f"{quantity} níveis"


def _get_result_section(consolidated_result, section_name):
    """
    Busca uma seção interna do resultado consolidado.

    Exemplo:
    section_name = "financial"

    Retorna:
    consolidated_result["results"]["financial"]

    Se a seção não existir, retorna um dicionário vazio para evitar erro.
    """

    return consolidated_result.get("results", {}).get(section_name, {})


def _format_profile_change(input_profile, output_profile):
    """
    Formata a mudança entre um perfil de entrada e um perfil de saída.

    Exemplos:
    - Arrojado -> Moderado
    - Moderado -> Moderado
    """

    if input_profile == output_profile:
        return f"manteve o perfil {output_profile}"

    return f"alterou o perfil de {input_profile} para {output_profile}"


def _format_event_messages(events, empty_message):
    """
    Recebe uma lista de eventos lógicos e transforma em texto.

    Cada evento geralmente tem:
    - type;
    - source;
    - message.

    Exemplo de evento:
    {
        "type": "trava_forte",
        "source": "P4",
        "message": "Há necessidade declarada de utilizar o recurso no curto prazo."
    }
    """

    if not events:
        return empty_message

    messages = []

    for event in events:
        source = event.get("source", "origem não informada")
        message = event.get("message", "evento sem descrição")

        messages.append(f"- {source}: {message}")

    return "\n".join(messages)


def _build_preliminary_section(preliminary_result):
    """
    Monta a seção textual do perfil preliminar.

    Esta seção explica que o primeiro resultado nasceu das perguntas P1, P2 e P3.
    """

    profile = preliminary_result.get("profile", "não identificado")
    selected_answers = preliminary_result.get("selected_answers", {})

    lines = []

    lines.append("### 1. Perfil preliminar")
    lines.append(
        f"O perfil preliminar identificado foi **{profile}**. "
        "Essa primeira classificação considera a finalidade do investimento, "
        "o horizonte temporal e a tolerância ao risco."
    )

    if selected_answers:
        lines.append("As respostas consideradas nessa etapa foram:")

        for question_id, answer_data in selected_answers.items():
            criterion = answer_data.get("criterion", "critério não informado")
            label = answer_data.get("label", "alternativa não informada")
            lines.append(f"- {question_id} — {criterion}: {label}")

    inconsistencies = preliminary_result.get("inconsistencies", [])

    if inconsistencies:
        lines.append("Foram observados pontos de atenção no bloco preliminar:")

        for item in inconsistencies:
            lines.append(f"- {item}")

    return "\n".join(lines)


def _build_financial_section(financial_result):
    """
    Monta a seção textual da compatibilidade financeira.

    Esta seção explica se o perfil foi mantido, reduzido ou bloqueado
    por necessidade de liquidez, renda, reserva ou fragilidade financeira.
    """

    input_profile = financial_result.get("input_profile", "não identificado")
    output_profile = financial_result.get("profile", "não identificado")
    reduction_steps = financial_result.get("reduction_steps", 0)
    reduction_reason = financial_result.get("reduction_reason", "")

    strong_locks = financial_result.get("strong_locks", [])
    moderations = financial_result.get("moderations", [])
    inconsistencies = financial_result.get("inconsistencies", [])
    blocked_profiles = financial_result.get("blocked_profiles", [])

    lines = []

    lines.append("### 2. Compatibilidade financeira")

    if reduction_steps == 0:
        lines.append(
            f"A análise de compatibilidade financeira {_format_profile_change(input_profile, output_profile)}. "
            "Não foram identificadas restrições financeiras suficientes para reduzir a classificação."
        )
    else:
        lines.append(
            f"A análise de compatibilidade financeira {_format_profile_change(input_profile, output_profile)}, "
            f"com redução de {_format_levels(reduction_steps)}. Motivo: {reduction_reason}"
        )

    lines.append("Travas financeiras fortes identificadas:")
    lines.append(
        _format_event_messages(
            strong_locks,
            "Não foram identificadas travas financeiras fortes."
        )
    )

    lines.append("Moderações financeiras identificadas:")
    lines.append(
        _format_event_messages(
            moderations,
            "Não foram identificadas moderações financeiras relevantes."
        )
    )

    if blocked_profiles:
        lines.append(
            "Perfis bloqueados por prudência nesta etapa: "
            + ", ".join(blocked_profiles)
            + "."
        )

    if inconsistencies:
        lines.append("Inconsistências financeiras observadas:")

        for item in inconsistencies:
            lines.append(f"- {item}")

    return "\n".join(lines)


def _build_knowledge_section(knowledge_result):
    """
    Monta a seção textual do refinamento por conhecimento e experiência.

    Esta seção explica se a familiaridade, a experiência prática e a formação
    foram suficientes para manter o perfil ou se exigiram redução prudencial.
    """

    input_profile = knowledge_result.get("input_profile", "não identificado")
    output_profile = knowledge_result.get("profile", "não identificado")
    reduction_steps = knowledge_result.get("reduction_steps", 0)
    reduction_reason = knowledge_result.get("reduction_reason", "")

    limitations = knowledge_result.get("limitations", [])
    moderations = knowledge_result.get("moderations", [])
    confirmations = knowledge_result.get("confirmations", [])
    inconsistencies = knowledge_result.get("inconsistencies", [])
    blocked_profiles = knowledge_result.get("blocked_profiles", [])

    lines = []

    lines.append("### 3. Conhecimento e experiência")

    if reduction_steps == 0:
        lines.append(
            f"O refinamento por conhecimento e experiência {_format_profile_change(input_profile, output_profile)}. "
            "Não foram identificadas limitações suficientes para reduzir a classificação."
        )
    else:
        lines.append(
            f"O refinamento por conhecimento e experiência {_format_profile_change(input_profile, output_profile)}, "
            f"com redução de {_format_levels(reduction_steps)}. Motivo: {reduction_reason}"
        )

    lines.append("Limitações identificadas:")
    lines.append(
        _format_event_messages(
            limitations,
            "Não foram identificadas limitações fortes de conhecimento ou experiência."
        )
    )

    lines.append("Moderações identificadas:")
    lines.append(
        _format_event_messages(
            moderations,
            "Não foram identificadas moderações relevantes no eixo de conhecimento."
        )
    )

    lines.append("Confirmações identificadas:")
    lines.append(
        _format_event_messages(
            confirmations,
            "Não foram identificados fatores adicionais de confirmação."
        )
    )

    if blocked_profiles:
        lines.append(
            "Perfis bloqueados por prudência nesta etapa: "
            + ", ".join(blocked_profiles)
            + "."
        )

    if inconsistencies:
        lines.append("Inconsistências no eixo de conhecimento e experiência:")

        for item in inconsistencies:
            lines.append(f"- {item}")

    return "\n".join(lines)


def _build_final_section(consolidated_result):
    """
    Monta a seção final da justificativa.

    Esta seção apresenta:
    - perfil preliminar;
    - perfil após compatibilidade financeira;
    - perfil final;
    - total de reduções;
    - inconsistências gerais.
    """

    preliminary_profile = consolidated_result.get("preliminary_profile", "não identificado")
    financial_profile = consolidated_result.get("financial_profile", "não identificado")
    final_profile = consolidated_result.get("final_profile", "não identificado")
    total_reduction_steps = consolidated_result.get("total_reduction_steps", 0)

    inconsistencies = consolidated_result.get("inconsistencies", [])
    blocked_profiles = consolidated_result.get("blocked_profiles", [])

    lines = []

    lines.append("### 4. Resultado final")
    lines.append(
        f"O perfil preliminar foi **{preliminary_profile}**. "
        f"Após a compatibilidade financeira, o perfil passou a **{financial_profile}**. "
        f"Após o refinamento por conhecimento e experiência, o perfil final foi **{final_profile}**."
    )

    if total_reduction_steps > 0:
        lines.append(
            f"A classificação sofreu redução total de {_format_levels(total_reduction_steps)} ao longo do processamento por regras, "
            "em razão de travas, moderações ou limitações identificadas."
        )
    else:
        lines.append(
            "A classificação não sofreu redução ao longo do processamento por regras, pois os blocos posteriores confirmaram "
            "a coerência do perfil preliminar."
        )

    if blocked_profiles:
        lines.append(
            "Durante o processamento, houve bloqueio prudencial dos seguintes perfis: "
            + ", ".join(blocked_profiles)
            + "."
        )

    if inconsistencies:
        lines.append("Pontos de atenção registrados ao longo da classificação:")

        for item in inconsistencies:
            lines.append(f"- {item}")
    else:
        lines.append("Não foram registradas inconsistências relevantes ao longo da classificação.")

    lines.append(
        "Este resultado possui finalidade acadêmica e classificatória. "
        "O sistema não recomenda investimentos, não indica produtos financeiros e não substitui avaliação profissional."
    )

    return "\n".join(lines)


def generate_justification(consolidated_result):
    """
    Gera a justificativa textual completa da classificação.

    Parâmetro:
    - consolidated_result: resultado da função consolidate_final_profile().

    Retorno:
    Um dicionário contendo:
    - summary: resumo curto;
    - preliminary_text: texto sobre o perfil preliminar;
    - financial_text: texto sobre compatibilidade financeira;
    - knowledge_text: texto sobre conhecimento e experiência;
    - final_text: texto sobre resultado final;
    - full_text: justificativa completa.
    """

    preliminary_result = _get_result_section(consolidated_result, "preliminary")
    financial_result = _get_result_section(consolidated_result, "financial")
    knowledge_result = _get_result_section(consolidated_result, "knowledge")

    preliminary_profile = consolidated_result.get("preliminary_profile", "não identificado")
    financial_profile = consolidated_result.get("financial_profile", "não identificado")
    final_profile = consolidated_result.get("final_profile", "não identificado")

    summary = (
        f"O perfil preliminar foi {preliminary_profile}, passou para {financial_profile} "
        f"após a compatibilidade financeira e resultou em perfil final {final_profile}."
    )

    preliminary_text = _build_preliminary_section(preliminary_result)
    financial_text = _build_financial_section(financial_result)
    knowledge_text = _build_knowledge_section(knowledge_result)
    final_text = _build_final_section(consolidated_result)

    full_text = "\n\n".join(
        [
            preliminary_text,
            financial_text,
            knowledge_text,
            final_text,
        ]
    )

    return {
        "summary": summary,
        "preliminary_text": preliminary_text,
        "financial_text": financial_text,
        "knowledge_text": knowledge_text,
        "final_text": final_text,
        "full_text": full_text,
    }