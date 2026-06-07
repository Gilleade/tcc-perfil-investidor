QUESTIONS = [
    {
        "id": "P1",
        "block": "Bloco 1 — Objetivos e tolerância ao risco",
        "block_id": "B1",
        "axis": "Objetivos",
        "criterion": "Finalidade do investimento",
        "logical_function": "Formação do perfil preliminar",
        "logical_weight": "Nuclear",
        "text": "Qual é o principal objetivo deste investimento?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "formar reserva, preservar recursos ou manter disponibilidade",
                "level": "conservador",
            },
            {
                "id": 2,
                "label": "equilibrar preservação e crescimento ao longo do tempo",
                "level": "moderado",
            },
            {
                "id": 3,
                "label": "buscar crescimento patrimonial, aceitando maior oscilação",
                "level": "arrojado",
            },
        ],
    },
    {
        "id": "P2",
        "block": "Bloco 1 — Objetivos e tolerância ao risco",
        "block_id": "B1",
        "axis": "Objetivos",
        "criterion": "Horizonte temporal",
        "logical_function": "Formação do perfil preliminar",
        "logical_weight": "Nuclear",
        "text": "Por quanto tempo você pretende manter esse investimento aplicado?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "até 1 ano",
                "level": "conservador",
            },
            {
                "id": 2,
                "label": "acima de 1 ano até 5 anos",
                "level": "moderado",
            },
            {
                "id": 3,
                "label": "acima de 5 anos",
                "level": "arrojado",
            },
        ],
    },
    {
        "id": "P3",
        "block": "Bloco 1 — Objetivos e tolerância ao risco",
        "block_id": "B1",
        "axis": "Objetivos",
        "criterion": "Tolerância ao risco",
        "logical_function": "Formação do perfil preliminar",
        "logical_weight": "Nuclear",
        "text": "Como você reage à possibilidade de oscilações ou perdas temporárias no valor do investimento?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "prefiro evitar oscilações e perdas, mesmo com retorno menor",
                "level": "conservador",
            },
            {
                "id": 2,
                "label": "aceito oscilações moderadas em busca de retorno maior no longo prazo",
                "level": "moderado",
            },
            {
                "id": 3,
                "label": "aceito oscilações elevadas e perdas temporárias em busca de retorno maior",
                "level": "arrojado",
            },
        ],
    },
    {
        "id": "P4",
        "block": "Bloco 2 — Compatibilidade financeira",
        "block_id": "B2",
        "axis": "Situação financeira",
        "criterion": "Necessidade futura de recursos",
        "logical_function": "Limite prudencial de compatibilidade financeira",
        "logical_weight": "Limite prudencial",
        "text": "Esse valor pode ser necessário no curto prazo para cobrir despesas, compromissos ou emergências?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "sim",
                "level": "necessidade_curto_prazo",
            },
            {
                "id": 2,
                "label": "não",
                "level": "sem_necessidade_curto_prazo",
            },
        ],
    },
    {
        "id": "P5",
        "block": "Bloco 2 — Compatibilidade financeira",
        "block_id": "B2",
        "axis": "Situação financeira",
        "criterion": "Estabilidade de renda / entrada regular",
        "logical_function": "Compatibilidade financeira",
        "logical_weight": "Moderação",
        "text": "Como você classificaria sua renda ou entrada regular de recursos?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "minha renda é instável ou com pouca folga financeira",
                "level": "restricao_forte",
            },
            {
                "id": 2,
                "label": "minha renda é relativamente estável, com alguma folga",
                "level": "moderacao",
            },
            {
                "id": 3,
                "label": "minha renda é estável e tenho folga financeira consistente",
                "level": "sem_restricao",
            },
        ],
    },
    {
        "id": "P6",
        "block": "Bloco 2 — Compatibilidade financeira",
        "block_id": "B2",
        "axis": "Situação financeira",
        "criterion": "Reserva financeira / robustez patrimonial",
        "logical_function": "Compatibilidade financeira",
        "logical_weight": "Trava/moderação",
        "text": "Você possui reserva financeira ou patrimônio que permita suportar oscilações sem comprometer seu orçamento essencial?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "não possuo reserva suficiente para suportar oscilações",
                "level": "restricao_forte",
            },
            {
                "id": 2,
                "label": "possuo reserva parcial, mas com limites",
                "level": "moderacao",
            },
            {
                "id": 3,
                "label": "possuo reserva suficiente para suportar oscilações sem comprometer o essencial",
                "level": "sem_restricao",
            },
        ],
    },
    {
        "id": "P7",
        "block": "Bloco 3 — Conhecimento e experiência",
        "block_id": "B3",
        "axis": "Conhecimento e experiência",
        "criterion": "Familiaridade com investimentos",
        "logical_function": "Refinamento por conhecimento",
        "logical_weight": "Refinamento principal",
        "text": "Com quais tipos de investimentos você já teve contato ou sobre os quais possui familiaridade?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "tenho pouca ou nenhuma familiaridade além de alternativas muito simples",
                "level": "baixo_conhecimento",
            },
            {
                "id": 2,
                "label": "tenho familiaridade com algumas opções de investimento e seus riscos básicos",
                "level": "conhecimento_intermediario",
            },
            {
                "id": 3,
                "label": "tenho familiaridade também com produtos de maior oscilação e seus riscos",
                "level": "conhecimento_alto",
            },
        ],
    },
    {
        "id": "P8",
        "block": "Bloco 3 — Conhecimento e experiência",
        "block_id": "B3",
        "axis": "Conhecimento e experiência",
        "criterion": "Experiência prática com investimentos",
        "logical_function": "Refinamento por experiência",
        "logical_weight": "Refinamento principal",
        "text": "Com que frequência e há quanto tempo você realiza investimentos?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "não invisto ou invisto há pouco tempo e raramente",
                "level": "baixa_experiencia",
            },
            {
                "id": 2,
                "label": "invisto há algum tempo, com alguma regularidade",
                "level": "experiencia_intermediaria",
            },
            {
                "id": 3,
                "label": "invisto há mais tempo e com frequência consistente",
                "level": "experiencia_alta",
            },
        ],
    },
    {
        "id": "P9",
        "block": "Bloco 3 — Conhecimento e experiência",
        "block_id": "B3",
        "axis": "Conhecimento e experiência",
        "criterion": "Formação ou experiência profissional relacionada",
        "logical_function": "Confirmação complementar",
        "logical_weight": "Confirmação",
        "text": "Você possui formação ou experiência profissional relacionada a finanças, investimentos ou áreas próximas?",
        "type": "single_choice",
        "options": [
            {
                "id": 1,
                "label": "não possuo",
                "level": "sem_formacao_relacionada",
            },
            {
                "id": 2,
                "label": "possuo contato indireto ou básico",
                "level": "contato_basico",
            },
            {
                "id": 3,
                "label": "possuo formação ou experiência direta e relevante",
                "level": "formacao_relevante",
            },
        ],
    },
]


def get_all_questions():
    """Retorna todas as perguntas principais cadastradas."""
    return QUESTIONS


def get_questions_by_block(block_id):
    """Retorna as perguntas principais de um bloco específico."""
    return [
        question
        for question in QUESTIONS
        if question["block_id"] == block_id
    ]


def get_question_by_id(question_id):
    """Busca uma pergunta principal pelo identificador."""
    for question in QUESTIONS:
        if question["id"] == question_id:
            return question

    return None