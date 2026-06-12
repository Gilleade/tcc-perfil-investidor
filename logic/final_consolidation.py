# Importa a função que calcula o perfil preliminar com base em P1, P2 e P3.
from logic.preliminary_profile import calculate_preliminary_profile

# Importa a função que aplica as regras financeiras com base em P4, P5, P6
# e nas subperguntas financeiras.
from logic.financial_rules import apply_financial_compatibility

# Importa a função que aplica o refinamento por conhecimento e experiência
# com base em P7, P8, P9 e subperguntas relacionadas.
from logic.knowledge_rules import apply_knowledge_refinement


def _combine_logs(*results):
    """
    Junta os registros lógicos das etapas executadas.

    Cada etapa do processamento retorna uma lista chamada "log".
    Esta função une todos esses logs em uma única lista.

    Exemplo:
    - log do perfil preliminar;
    - log da compatibilidade financeira;
    - log do refinamento por conhecimento.

    Retorno:
    - lista única com todos os registros lógicos.
    """

    combined_logs = []

    for result in results:
        combined_logs.extend(result.get("log", []))

    return combined_logs


def _combine_inconsistencies(*results):
    """
    Junta inconsistências identificadas nas etapas do processamento.

    Algumas etapas podem identificar conflitos ou pontos de atenção.
    Exemplo:
    - alta tolerância a risco com prazo curto;
    - necessidade de liquidez com ausência de reserva;
    - familiaridade alta contradita por baixa compreensão de risco.

    Retorno:
    - lista única com todas as inconsistências identificadas.
    """

    combined_inconsistencies = []

    for result in results:
        combined_inconsistencies.extend(result.get("inconsistencies", []))

    return combined_inconsistencies


def _combine_blocked_profiles(*results):
    """
    Junta perfis bloqueados por prudência nas etapas intermediárias.

    Exemplo:
    - Arrojado bloqueado por incompatibilidade financeira;
    - Arrojado bloqueado por baixa familiaridade ou experiência.

    Retorno:
    - lista sem duplicação com os perfis bloqueados.
    """

    blocked_profiles = []

    for result in results:
        for profile in result.get("blocked_profiles", []):
            if profile not in blocked_profiles:
                blocked_profiles.append(profile)

    return blocked_profiles


def _build_adjustments_summary(financial_result, knowledge_result):
    """
    Monta um resumo dos ajustes realizados depois do perfil preliminar.

    A ideia é registrar, de forma objetiva, se houve:
    - redução financeira;
    - bloqueio prudencial;
    - redução por conhecimento;
    - manutenção do perfil.

    Esta função ainda não cria a justificativa textual final.
    Ela apenas organiza os dados que serão usados na próxima etapa.
    """

    adjustments = []

    # Verifica ajuste financeiro.
    if financial_result["reduction_steps"] > 0:
        adjustments.append(
            {
                "stage": "compatibilidade_financeira",
                "type": "reducao",
                "levels": financial_result["reduction_steps"],
                "reason": financial_result["reduction_reason"],
                "from_profile": financial_result["input_profile"],
                "to_profile": financial_result["profile"],
            }
        )
    else:
        adjustments.append(
            {
                "stage": "compatibilidade_financeira",
                "type": "manutencao",
                "levels": 0,
                "reason": financial_result["reduction_reason"],
                "from_profile": financial_result["input_profile"],
                "to_profile": financial_result["profile"],
            }
        )

    # Verifica ajuste por conhecimento e experiência.
    if knowledge_result["reduction_steps"] > 0:
        adjustments.append(
            {
                "stage": "refinamento_conhecimento_experiencia",
                "type": "reducao",
                "levels": knowledge_result["reduction_steps"],
                "reason": knowledge_result["reduction_reason"],
                "from_profile": knowledge_result["input_profile"],
                "to_profile": knowledge_result["profile"],
            }
        )
    else:
        adjustments.append(
            {
                "stage": "refinamento_conhecimento_experiencia",
                "type": "manutencao",
                "levels": 0,
                "reason": knowledge_result["reduction_reason"],
                "from_profile": knowledge_result["input_profile"],
                "to_profile": knowledge_result["profile"],
            }
        )

    return adjustments


def consolidate_final_profile(answers, subanswers):
    """
    Consolida o perfil final do investidor.

    Parâmetros:
    - answers: dicionário com respostas das 9 perguntas principais.
      Exemplo:
      {
          "P1": 3,
          "P2": 3,
          "P3": 3,
          "P4": 2,
          "P5": 3,
          "P6": 3,
          "P7": 3,
          "P8": 3,
          "P9": 3
      }

    - subanswers: dicionário com respostas das subperguntas condicionais.
      Exemplo:
      {
          "7A": 3,
          "7B": 3,
          "8A": 3,
          "8B": 3
      }

    Retorno:
    Um dicionário com:
    - perfil preliminar;
    - perfil após compatibilidade financeira;
    - perfil final;
    - resultados intermediários completos;
    - logs;
    - inconsistências;
    - bloqueios;
    - resumo dos ajustes.

    Importante:
    Esta função ainda NÃO gera a justificativa textual final.
    Ela apenas organiza todos os dados necessários para isso.
    """

    # ---------------------------------------------------------------
    # Etapa 1 — Perfil preliminar
    # ---------------------------------------------------------------
    #
    # Usa apenas P1, P2 e P3.
    # Resultado possível:
    # - Conservador;
    # - Moderado;
    # - Arrojado.

    preliminary_result = calculate_preliminary_profile(answers)

    preliminary_profile = preliminary_result["profile"]

    # ---------------------------------------------------------------
    # Etapa 2 — Compatibilidade financeira
    # ---------------------------------------------------------------
    #
    # Usa o perfil preliminar e aplica P4, P5, P6
    # e subperguntas financeiras.
    #
    # Essa etapa pode:
    # - manter o perfil;
    # - reduzir 1 nível;
    # - reduzir 2 níveis;
    # - bloquear perfil alto.

    financial_result = apply_financial_compatibility(
        preliminary_profile=preliminary_profile,
        answers=answers,
        subanswers=subanswers,
    )

    financial_profile = financial_result["profile"]

    # ---------------------------------------------------------------
    # Etapa 3 — Refinamento por conhecimento e experiência
    # ---------------------------------------------------------------
    #
    # Usa o perfil que saiu da compatibilidade financeira
    # e aplica P7, P8, P9 e subperguntas relacionadas.
    #
    # Essa etapa pode:
    # - manter o perfil;
    # - reduzir o perfil;
    # - bloquear perfil alto por prudência.
    #
    # Ela nunca eleva o perfil isoladamente.

    knowledge_result = apply_knowledge_refinement(
        current_profile=financial_profile,
        answers=answers,
        subanswers=subanswers,
    )

    final_profile = knowledge_result["profile"]

    # ---------------------------------------------------------------
    # Organização dos resultados
    # ---------------------------------------------------------------
    #
    # Aqui reunimos todas as informações intermediárias em uma estrutura única.
    # Isso facilitará a próxima etapa: geração da justificativa textual.

    logs = _combine_logs(
        preliminary_result,
        financial_result,
        knowledge_result,
    )

    inconsistencies = _combine_inconsistencies(
        preliminary_result,
        financial_result,
        knowledge_result,
    )

    blocked_profiles = _combine_blocked_profiles(
        financial_result,
        knowledge_result,
    )

    adjustments = _build_adjustments_summary(
        financial_result=financial_result,
        knowledge_result=knowledge_result,
    )

    total_reduction_steps = (
        financial_result["reduction_steps"]
        + knowledge_result["reduction_steps"]
    )

    return {
        "stage": "consolidacao_final",
        "preliminary_profile": preliminary_profile,
        "financial_profile": financial_profile,
        "final_profile": final_profile,
        "total_reduction_steps": total_reduction_steps,
        "profiles": {
            "preliminary": preliminary_profile,
            "after_financial_compatibility": financial_profile,
            "final": final_profile,
        },
        "results": {
            "preliminary": preliminary_result,
            "financial": financial_result,
            "knowledge": knowledge_result,
        },
        "adjustments": adjustments,
        "logs": logs,
        "inconsistencies": inconsistencies,
        "blocked_profiles": blocked_profiles,
    }