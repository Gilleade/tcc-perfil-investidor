# Importa a função que busca uma pergunta pelo identificador.
# Usaremos isso para recuperar o texto das alternativas e montar um registro lógico mais claro.
from data.questions import get_question_by_id


# Perfis finais usados no protótipo.
# Nesta etapa, eles ainda representam apenas o PERFIL PRELIMINAR.
PROFILE_CONSERVADOR = "Conservador"
PROFILE_MODERADO = "Moderado"
PROFILE_ARROJADO = "Arrojado"


# Perguntas que formam exclusivamente o perfil preliminar.
# Conforme a modelagem da Branch 3, o perfil preliminar nasce de:
# P1 = finalidade;
# P2 = horizonte temporal;
# P3 = tolerância ao risco.
PRELIMINARY_QUESTION_IDS = ["P1", "P2", "P3"]


def _get_answer_value(answers, question_id):
    """
    Busca o valor numérico da resposta de uma pergunta.

    Parâmetros:
    - answers: dicionário com respostas principais.
      Exemplo: {"P1": 2, "P2": 3, "P3": 2}

    - question_id: identificador da pergunta.
      Exemplo: "P1"

    Retorno:
    - número inteiro da alternativa escolhida: 1, 2 ou 3.

    Se a pergunta não tiver sido respondida ou tiver valor inválido,
    a função gera um erro para evitar cálculo incorreto.
    """

    if question_id not in answers:
        raise ValueError(f"A pergunta {question_id} é obrigatória para calcular o perfil preliminar.")

    value = answers.get(question_id)

    if value not in [1, 2, 3]:
        raise ValueError(f"A resposta da pergunta {question_id} deve ser 1, 2 ou 3.")

    return value


def _get_option_label(question_id, option_id):
    """
    Recupera o texto da alternativa escolhida.

    Isso não é obrigatório para o cálculo, mas ajuda a montar
    uma explicação mais rastreável.

    Exemplo:
    question_id = "P1"
    option_id = 2

    Retorna:
    "equilibrar preservação e crescimento ao longo do tempo"
    """

    question = get_question_by_id(question_id)

    if question is None:
        return "Pergunta não encontrada."

    for option in question["options"]:
        if option["id"] == option_id:
            return option["label"]

    return "Alternativa não encontrada."


def _has_strong_conservative_convergence(p1, p2, p3):
    """
    Verifica se existe convergência forte para perfil conservador.

    A modelagem consolidada definiu que o perfil conservador aparece
    quando predominam preservação, horizonte curto e baixa tolerância
    ao risco.

    Nesta função, consideramos convergência conservadora quando
    pelo menos dois elementos centrais apontam para restrição forte.

    Exemplos:
    - P1 = 1 e P2 = 1  -> finalidade de preservação + prazo curto;
    - P1 = 1 e P3 = 1  -> preservação + baixa tolerância ao risco;
    - P2 = 1 e P3 = 1  -> prazo curto + baixa tolerância ao risco.
    """

    conservative_signals = 0

    if p1 == 1:
        conservative_signals += 1

    if p2 == 1:
        conservative_signals += 1

    if p3 == 1:
        conservative_signals += 1

    return conservative_signals >= 2


def _has_arrojado_convergence(p1, p2, p3):
    """
    Verifica se existe convergência suficiente para perfil arrojado preliminar.

    A Branch 3 definiu que o perfil arrojado preliminar exige:
    - orientação para crescimento;
    - horizonte intermediário/longo ou longo;
    - alta tolerância ao risco;
    - ausência de resposta claramente restritiva no primeiro bloco.

    Por isso, não permitimos perfil arrojado preliminar quando
    qualquer uma das três respostas centrais for nível 1.
    """

    # Se qualquer critério do Bloco 1 estiver no nível 1,
    # o perfil preliminar não pode ser Arrojado.
    if p1 == 1 or p2 == 1 or p3 == 1:
        return False

    # Caso mais forte:
    # finalidade de crescimento + prazo longo + alta tolerância ao risco.
    if p1 == 3 and p2 == 3 and p3 == 3:
        return True

    # Crescimento + prazo intermediário ou longo + alta tolerância ao risco.
    if p1 == 3 and p2 in [2, 3] and p3 == 3:
        return True

    # Finalidade equilibrada ou de crescimento + prazo longo + alta tolerância ao risco.
    if p1 in [2, 3] and p2 == 3 and p3 == 3:
        return True

    return False


def _detect_preliminary_inconsistencies(p1, p2, p3):
    """
    Identifica inconsistências preliminares entre objetivo, prazo e risco.

    Essas inconsistências ainda não geram perfil final.
    Elas apenas são registradas para futura justificativa textual.

    Exemplo:
    - usuário declara alta tolerância ao risco,
      mas também declara finalidade de preservação ou prazo curto.
    """

    inconsistencies = []

    if p3 == 3 and p1 == 1:
        inconsistencies.append(
            "Alta tolerância ao risco declarada em conjunto com finalidade de preservação ou reserva."
        )

    if p3 == 3 and p2 == 1:
        inconsistencies.append(
            "Alta tolerância ao risco declarada em conjunto com horizonte temporal de até 1 ano."
        )

    if p1 == 3 and p3 == 1:
        inconsistencies.append(
            "Busca de crescimento patrimonial combinada com baixa tolerância a oscilações."
        )

    if p2 == 3 and p3 == 1:
        inconsistencies.append(
            "Horizonte temporal longo combinado com baixa tolerância a oscilações."
        )

    return inconsistencies


def calculate_preliminary_profile(answers):
    """
    Calcula o perfil preliminar com base nas perguntas P1, P2 e P3.

    Parâmetro:
    - answers: dicionário com respostas principais.
      Exemplo: {"P1": 3, "P2": 3, "P3": 3}

    Retorno:
    Um dicionário com:
    - perfil preliminar;
    - respostas consideradas;
    - critérios utilizados;
    - registro lógico;
    - inconsistências preliminares, se existirem.

    Importante:
    Este cálculo ainda NÃO representa o perfil final.
    O perfil final só será definido depois das etapas de:
    1. compatibilidade financeira;
    2. refinamento por conhecimento/experiência;
    3. consolidação final.
    """

    # Recupera as respostas obrigatórias do Bloco 1.
    p1 = _get_answer_value(answers, "P1")
    p2 = _get_answer_value(answers, "P2")
    p3 = _get_answer_value(answers, "P3")

    # Monta um resumo das respostas usadas no cálculo.
    selected_answers = {
        "P1": {
            "criterion": "Finalidade do investimento",
            "value": p1,
            "label": _get_option_label("P1", p1),
        },
        "P2": {
            "criterion": "Horizonte temporal",
            "value": p2,
            "label": _get_option_label("P2", p2),
        },
        "P3": {
            "criterion": "Tolerância ao risco",
            "value": p3,
            "label": _get_option_label("P3", p3),
        },
    }

    # Lista que guardará a explicação lógica do cálculo.
    logical_log = []

    # Lista de inconsistências preliminares.
    inconsistencies = _detect_preliminary_inconsistencies(p1, p2, p3)

    # ---------------------------------------------------------------
    # Regra 1 — Verificar convergência para perfil arrojado
    # ---------------------------------------------------------------
    #
    # O perfil Arrojado preliminar exige convergência positiva:
    # crescimento, prazo adequado e alta tolerância ao risco.
    # Se houver resposta nível 1 em qualquer item do Bloco 1,
    # o perfil preliminar não pode ser Arrojado.

    if _has_arrojado_convergence(p1, p2, p3):
        preliminary_profile = PROFILE_ARROJADO

        logical_log.append(
            "O perfil preliminar foi classificado como Arrojado porque finalidade, horizonte temporal "
            "e tolerância ao risco indicaram convergência suficiente para maior aceitação de oscilação."
        )

    # ---------------------------------------------------------------
    # Regra 2 — Verificar convergência para perfil conservador
    # ---------------------------------------------------------------
    #
    # O perfil Conservador preliminar ocorre quando pelo menos dois
    # dos três elementos centrais indicam preservação, curto prazo
    # ou baixa tolerância ao risco.

    elif _has_strong_conservative_convergence(p1, p2, p3):
        preliminary_profile = PROFILE_CONSERVADOR

        logical_log.append(
            "O perfil preliminar foi classificado como Conservador porque houve predominância de sinais "
            "ligados à preservação, horizonte curto ou baixa tolerância ao risco."
        )

    # ---------------------------------------------------------------
    # Regra 3 — Demais combinações ficam como perfil moderado
    # ---------------------------------------------------------------
    #
    # Quando não existe convergência forte para Conservador nem
    # convergência suficiente para Arrojado, a classificação preliminar
    # permanece como Moderado.

    else:
        preliminary_profile = PROFILE_MODERADO

        logical_log.append(
            "O perfil preliminar foi classificado como Moderado porque as respostas apresentaram combinação "
            "intermediária ou sem convergência suficiente para os extremos."
        )

    # Caso existam inconsistências preliminares, registramos isso.
    # Essas inconsistências poderão ser usadas depois na justificativa final.
    if inconsistencies:
        logical_log.append(
            "Foram identificadas combinações preliminares que exigem atenção nas etapas posteriores da árvore."
        )

    return {
        "stage": "perfil_preliminar",
        "profile": preliminary_profile,
        "criteria_used": [
            "Finalidade do investimento",
            "Horizonte temporal",
            "Tolerância ao risco",
        ],
        "selected_answers": selected_answers,
        "log": logical_log,
        "inconsistencies": inconsistencies,
    }