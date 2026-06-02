TEST_CASES = [
    {
        "code": "T01",
        "description": "Conservador claro",
        "answers": {
            "P1": 1, "P2": 1, "P3": 1,
            "P4": 1, "P5": 3, "P6": 3,
            "P7": 1, "P8": 1, "P9": 1,
        },
        "subanswers": {
            "2A": 1,
            "4A": 1,
            "4B": 1,
        },
        "expected": {
            "preliminary": "Conservador",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "caso-base conservador"
    },

    {
        "code": "T02",
        "description": "Moderado claro",
        "answers": {
            "P1": 2, "P2": 2, "P3": 2,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 2, "P8": 2, "P9": 2,
        },
        "subanswers": {
            "2A": 2,
            "7A": 2,
            "8A": 2,
            "8B": 2,
        },
        "expected": {
            "preliminary": "Moderado",
            "financial": "Moderado",
            "final": "Moderado",
        },
        "validate": "caso-base moderado"
    },

    {
        "code": "T03",
        "description": "Arrojado claro",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        },
        "subanswers": {
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Arrojado",
            "final": "Arrojado",
        },
        "validate": "caso-base arrojado"
    },

    {
        "code": "T04",
        "description": "Arrojado preliminar reduzido para Moderado",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 1, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        },
        "subanswers": {
            "4A": 2, "4B": 2,
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Moderado",
            "final": "Moderado",
        },
        "validate": "redução de 1 nível por compatibilidade financeira"
    },

    {
        "code": "T05",
        "description": "Arrojado preliminar reduzido para Conservador",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 1, "P5": 1, "P6": 1,
            "P7": 3, "P8": 3, "P9": 3,
        },
        "subanswers": {
            "4A": 1, "4B": 1,
            "5A": 1,
            "6A": 1, "6B": 1,
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "redução de 2 níveis por fragilidade financeira"
    },

    {
        "code": "T06",
        "description": "Moderado preliminar reduzido para Conservador",
        "answers": {
            "P1": 2, "P2": 2, "P3": 2,
            "P4": 1, "P5": 3, "P6": 3,
            "P7": 2, "P8": 2, "P9": 2,
        },
        "subanswers": {
            "2A": 2,
            "4A": 1, "4B": 1,
            "7A": 2,
            "8A": 2, "8B": 2,
        },
        "expected": {
            "preliminary": "Moderado",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "redução de moderado para conservador"
    },

    {
        "code": "T07",
        "description": "Alta tolerância ao risco com necessidade essencial de liquidez",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 1, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        },
        "subanswers": {
            "4A": 1, "4B": 1,
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "conflito entre risco alto e liquidez curta"
    },

    {
        "code": "T08",
        "description": "Longo prazo com ausência de reserva financeira suficiente",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 2, "P6": 1,
            "P7": 3, "P8": 3, "P9": 2,
        },
        "subanswers": {
            "6A": 1, "6B": 1,
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "redução por baixa robustez financeira"
    },

    {
        "code": "T09",
        "description": "Busca de crescimento, mas baixo conhecimento/experiência",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 1, "P8": 1, "P9": 1,
        },
        "subanswers": {},
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Arrojado",
            "final": "Conservador",
        },
        "validate": "redução por incompatibilidade no eixo cognitivo/experiencial"
    },

    {
        "code": "T10",
        "description": "Ativação de subquestões condicionais",
        "answers": {
            "P1": 2, "P2": 2, "P3": 2,
            "P4": 1, "P5": 1, "P6": 2,
            "P7": 3, "P8": 2, "P9": 2,
        },
        "subanswers": {
            "2A": 2,
            "4A": 2, "4B": 2,
            "5A": 1,
            "6A": 2, "6B": 2,
            "7A": 3, "7B": 3,
            "8A": 2, "8B": 2,
        },
        "expected": {
            "preliminary": "Moderado",
            "financial": "Conservador",
            "final": "Conservador",
        },
        "validate": "ativação correta de múltiplas subquestões"
    },

    {
        "code": "T11",
        "description": "Inconsistência entre finalidade, prazo e risco",
        "answers": {
            "P1": 1, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 2,
        },
        "subanswers": {
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        },
        "expected": {
            "preliminary": "Moderado",
            "financial": "Moderado",
            "final": "Moderado",
        },
        "validate": "tratamento prudencial de inconsistência"
    },

    {
        "code": "T12",
        "description": "Validação da justificativa textual",
        "answers": {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 2, "P8": 2, "P9": 2,
        },
        "subanswers": {
            "7A": 2,
            "8A": 2, "8B": 2,
        },
        "expected": {
            "preliminary": "Arrojado",
            "financial": "Arrojado",
            "final": "Moderado",
        },
        "validate": "justificativa com percurso completo"
    },
]