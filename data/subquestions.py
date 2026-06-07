# Subperguntas condicionais do protótipo.
#
# As subperguntas são exibidas apenas quando a resposta de uma pergunta
# principal atende ao gatilho definido em trigger_option_ids.

SUBQUESTIONS = [
    {
        "id": "4A",
        "parent_question_id": "P4",
        "text": "A necessidade prevista comprometerá uma parte relevante do valor investido?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "sim, comprometerá parte relevante do valor", "level": "uso_relevante"},
            {"id": 2, "label": "não, será apenas uma parte pequena", "level": "uso_parcial"},
            {"id": 3, "label": "não, não comprometerá parte relevante do valor", "level": "uso_nao_relevante"},
        ],
        "trigger_option_ids": [1],
        "logical_function": "Refinar trava financeira",
        "purpose": "Distinguir uso relevante, uso parcial e uso não relevante do valor",
        "auto_activate": True,
    },
    {
        "id": "4B",
        "parent_question_id": "P4",
        "text": "O uso futuro do recurso está relacionado a despesas essenciais, compromisso já previsto ou apenas conveniência eventual?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "despesas essenciais", "level": "liquidez_essencial"},
            {"id": 2, "label": "compromisso já previsto", "level": "liquidez_planejada"},
            {"id": 3, "label": "conveniência eventual", "level": "liquidez_desejada"},
        ],
        "trigger_option_ids": [1],
        "logical_function": "Refinar necessidade de liquidez",
        "purpose": "Separar necessidade essencial, compromisso planejado e conveniência eventual",
        "auto_activate": True,
    },
    {
        "id": "5A",
        "parent_question_id": "P5",
        "text": "Uma perda temporária ou imobilização maior desse recurso comprometeria seu orçamento essencial?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "sim, comprometeria meu orçamento essencial", "level": "compromete_essencial"},
            {"id": 2, "label": "afetaria parcialmente, mas sem comprometer o essencial", "level": "impacto_parcial"},
            {"id": 3, "label": "não comprometeria meu orçamento essencial", "level": "nao_compromete"},
        ],
        "trigger_option_ids": [1],
        "logical_function": "Refinar compatibilidade financeira",
        "purpose": "Distinguir restrição prudencial forte de impacto parcial ou sem impacto relevante",
        "auto_activate": True,
    },
    {
        "id": "6A",
        "parent_question_id": "P6",
        "text": "Sua reserva atual seria suficiente para lidar com imprevistos sem depender desse investimento no curto prazo?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "não, dependeria desse investimento", "level": "reserva_insuficiente"},
            {"id": 2, "label": "parcialmente, mas com limitações", "level": "reserva_parcial"},
            {"id": 3, "label": "sim, seria suficiente", "level": "reserva_suficiente"},
        ],
        "trigger_option_ids": [1, 2],
        "logical_function": "Confirmar robustez financeira",
        "purpose": "Diferenciar ausência de reserva, reserva parcial e reserva suficiente",
        "auto_activate": True,
    },
    {
        "id": "6B",
        "parent_question_id": "P6",
        "text": "Uma oscilação relevante nesse valor comprometeria despesas essenciais ou apenas reduziria sua margem de conforto?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "comprometeria despesas essenciais", "level": "restricao_forte"},
            {"id": 2, "label": "reduziria minha margem de conforto", "level": "moderacao"},
            {"id": 3, "label": "não geraria impacto relevante", "level": "sem_restricao"},
        ],
        "trigger_option_ids": [1, 2],
        "logical_function": "Refinar restrição financeira",
        "purpose": "Distinguir restrição forte, moderação e ausência de restrição relevante",
        "auto_activate": True,
    },
    {
        "id": "7A",
        "parent_question_id": "P7",
        "text": "Sua familiaridade decorre de experiência prática, estudo próprio ou apenas conhecimento superficial?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "apenas conhecimento superficial", "level": "superficial"},
            {"id": 2, "label": "estudo próprio ou acompanhamento básico", "level": "estudo_basico"},
            {"id": 3, "label": "experiência prática ou estudo consistente", "level": "familiaridade_efetiva"},
        ],
        "trigger_option_ids": [2, 3],
        "logical_function": "Refinar familiaridade declarada",
        "purpose": "Separar familiaridade efetiva de conhecimento superficial ou básico",
        "auto_activate": True,
    },
    {
        "id": "7B",
        "parent_question_id": "P7",
        "text": "Você se considera capaz de compreender as diferenças de risco entre alternativas mais estáveis e alternativas de maior oscilação?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "não me considero capaz", "level": "nao_compreende_risco"},
            {"id": 2, "label": "compreendo parcialmente", "level": "compreensao_parcial"},
            {"id": 3, "label": "sim, compreendo essas diferenças", "level": "compreensao_adequada"},
        ],
        "trigger_option_ids": [3],
        "logical_function": "Confirmar familiaridade alta",
        "purpose": "Verificar se a familiaridade alta é acompanhada de compreensão dos riscos",
        "auto_activate": True,
    },
    {
        "id": "8A",
        "parent_question_id": "P8",
        "text": "Sua experiência foi contínua e deliberada, ou apenas episódica?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "foi apenas episódica", "level": "experiencia_episodica"},
            {"id": 2, "label": "foi moderadamente regular", "level": "experiencia_moderada"},
            {"id": 3, "label": "foi contínua e deliberada", "level": "experiencia_continua"},
        ],
        "trigger_option_ids": [2, 3],
        "logical_function": "Refinar experiência prática",
        "purpose": "Distinguir experiência episódica, moderada e contínua",
        "auto_activate": True,
    },
    {
        "id": "8B",
        "parent_question_id": "P8",
        "text": "Essa experiência incluiu apenas alternativas mais simples ou também alternativas de maior oscilação?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "apenas alternativas mais simples", "level": "experiencia_simples"},
            {"id": 2, "label": "algumas alternativas com oscilação moderada", "level": "experiencia_intermediaria"},
            {"id": 3, "label": "também alternativas de maior oscilação", "level": "experiencia_maior_oscilacao"},
        ],
        "trigger_option_ids": [2, 3],
        "logical_function": "Confirmar experiência compatível",
        "purpose": "Verificar se a experiência prática sustenta perfis de maior exposição",
        "auto_activate": True,
    },
]


def get_all_subquestions():
    """Retorna todas as subperguntas cadastradas."""
    return SUBQUESTIONS


def get_subquestions_by_parent(parent_question_id):
    """Retorna as subperguntas vinculadas a uma pergunta principal."""
    return [
        subquestion
        for subquestion in SUBQUESTIONS
        if subquestion["parent_question_id"] == parent_question_id
    ]


def should_activate_subquestion(subquestion, selected_option_id):
    """Verifica se uma subpergunta deve ser ativada pela resposta selecionada."""
    if not subquestion.get("auto_activate", True):
        return False

    return selected_option_id in subquestion.get("trigger_option_ids", [])


def get_active_subquestions(parent_question_id, selected_option_id):
    """Retorna as subperguntas ativas para uma pergunta e resposta selecionada."""
    related_subquestions = get_subquestions_by_parent(parent_question_id)

    return [
        subquestion
        for subquestion in related_subquestions
        if should_activate_subquestion(subquestion, selected_option_id)
    ]


def get_subquestion_by_id(subquestion_id):
    """Busca uma subpergunta pelo identificador."""
    for subquestion in SUBQUESTIONS:
        if subquestion["id"] == subquestion_id:
            return subquestion

    return None