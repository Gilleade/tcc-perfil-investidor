# Lista principal de subperguntas condicionais do protótipo.
#
# As subperguntas não aparecem sempre.
# Elas aparecem apenas quando uma resposta de uma pergunta principal ativa um gatilho.
#
# Exemplo:
# - Se o usuário responder P4 com alternativa 1 ou 2,
#   as subperguntas 4A e 4B poderão ser exibidas.
#
# Nesta etapa, este arquivo apenas CADASTRA as subperguntas.
# A exibição no Streamlit será feita em uma etapa posterior.

SUBQUESTIONS = [
    {
        # Identificador único da subpergunta.
        # O padrão segue a modelagem: 4A, 4B, 5A etc.
        "id": "1A",

        # Pergunta principal de origem.
        # Esta subpergunta deriva da P1.
        "parent_question_id": "P1",

        # Texto da subpergunta que poderá aparecer ao usuário.
        "text": "O objetivo principal é preservar, equilibrar ou expandir o valor ao longo do tempo?",

        # Tipo de pergunta.
        # Neste protótipo, as subperguntas também serão de alternativa única.
        "type": "single_choice",

        # Lista de alternativas da subpergunta.
        "options": [
            {"id": 1, "label": "preservar o valor ou manter disponibilidade", "level": "preservacao"},
            {"id": 2, "label": "equilibrar preservação e crescimento", "level": "equilibrio"},
            {"id": 3, "label": "expandir o valor aceitando maior oscilação", "level": "expansao"},
        ],

        # Alternativas da pergunta principal que ativam esta subpergunta.
        #
        # A Branch 4 registrou a 1A como opcional, apenas em caso de ambiguidade futura.
        # Como ainda não temos uma regra automática de ambiguidade para P1, deixamos sem gatilho automático.
        # Assim, ela fica cadastrada, mas não será exibida automaticamente nesta primeira implementação.
        "trigger_option_ids": [],

        # Função lógica da subpergunta dentro da árvore.
        "logical_function": "Registrar inconsistência",

        # Explica para que a subpergunta serve.
        "purpose": "Registrar ambiguidade quando a finalidade declarada precisar de esclarecimento adicional",

        # Indica se a subpergunta está ativa automaticamente nesta versão.
        "auto_activate": False,
    },
    {
        "id": "4A",
        "parent_question_id": "P4",
        "text": "A necessidade prevista comprometerá uma parte relevante do valor investido?",
        "type": "single_choice",
        "options": [
            {"id": 1, "label": "sim, comprometerá parte relevante do valor", "level": "uso_relevante"},
            {"id": 2, "label": "não, será apenas uma parte pequena", "level": "uso_parcial"},
            {"id": 3, "label": "não sei informar com segurança", "level": "incerteza"},
        ],

        # A subpergunta 4A aparece quando P4 recebe resposta 1.
        # P4 = necessidade possível do valor no curto prazo.
        "trigger_option_ids": [1],
        "logical_function": "Refinar trava financeira",
        "purpose": "Distinguir trava forte de moderação",
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

        # A subpergunta 4B também aparece quando P4 recebe resposta 1.
        "trigger_option_ids": [1],
        "logical_function": "Registrar inconsistência e reduzir incerteza",
        "purpose": "Separar liquidez realmente necessária de liquidez apenas desejada",
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

        # A subpergunta 5A aparece apenas quando P5 recebe resposta 1.
        # P5 = renda instável ou com pouca folga.
        "trigger_option_ids": [1],
        "logical_function": "Refinar compatibilidade financeira",
        "purpose": "Converter renda instável em moderação ou trava prudencial",
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

        # A subpergunta 6A aparece quando P6 recebe resposta 1 ou 2.
        # P6 = reserva financeira ou robustez patrimonial.
        "trigger_option_ids": [1, 2],
        "logical_function": "Confirmar robustez financeira",
        "purpose": "Diferenciar ausência de reserva de reserva apenas parcial",
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

        # A subpergunta 6B também aparece quando P6 recebe resposta 1 ou 2.
        "trigger_option_ids": [1, 2],
        "logical_function": "Refinar restrição financeira",
        "purpose": "Distinguir restrição forte de moderação simples",
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

        # A subpergunta 7A aparece quando P7 recebe resposta 2 ou 3.
        # P7 = familiaridade com investimentos.
        "trigger_option_ids": [2, 3],
        "logical_function": "Reduzir incerteza",
        "purpose": "Separar familiaridade efetiva de conhecimento superficial",
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

        # A subpergunta 7B aparece apenas quando P7 recebe resposta 3.
        # Ela confirma a autodeclaração de familiaridade alta.
        "trigger_option_ids": [3],
        "logical_function": "Confirmar familiaridade alta",
        "purpose": "Validar se a autodeclaração de familiaridade alta é coerente",
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

        # A subpergunta 8A aparece quando P8 recebe resposta 2 ou 3.
        # P8 = experiência prática com investimentos.
        "trigger_option_ids": [2, 3],
        "logical_function": "Refinar experiência prática",
        "purpose": "Distinguir experiência regular de contato esporádico",
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

        # A subpergunta 8B também aparece quando P8 recebe resposta 2 ou 3.
        "trigger_option_ids": [2, 3],
        "logical_function": "Confirmar experiência compatível",
        "purpose": "Verificar compatibilidade da experiência com perfil mais alto",
        "auto_activate": True,
    },
]


def get_all_subquestions():
    """
    Retorna todas as subperguntas cadastradas.

    Esta função será útil quando quisermos verificar, testar
    ou listar todas as subperguntas do sistema.
    """
    return SUBQUESTIONS


def get_subquestions_by_parent(parent_question_id):
    """
    Retorna todas as subperguntas ligadas a uma pergunta principal.

    Exemplo:
    get_subquestions_by_parent("P4")

    Isso retorna as subperguntas derivadas da P4, como 4A e 4B.
    """
    return [
        subquestion
        for subquestion in SUBQUESTIONS
        if subquestion["parent_question_id"] == parent_question_id
    ]


def should_activate_subquestion(subquestion, selected_option_id):
    """
    Verifica se uma subpergunta deve ser ativada.

    Parâmetros:
    - subquestion: a subpergunta cadastrada.
    - selected_option_id: a alternativa escolhida na pergunta principal.

    Exemplo:
    Se a subpergunta 4A tem trigger_option_ids = [1, 2],
    ela será ativada quando o usuário responder P4 com alternativa 1 ou 2.
    """

    # Se a subpergunta não tem ativação automática,
    # ela não será exibida nesta etapa.
    if not subquestion.get("auto_activate", True):
        return False

    # Pega a lista de alternativas que ativam essa subpergunta.
    trigger_option_ids = subquestion.get("trigger_option_ids", [])

    # Retorna True se a alternativa escolhida estiver na lista de gatilhos.
    return selected_option_id in trigger_option_ids


def get_active_subquestions(parent_question_id, selected_option_id):
    """
    Retorna apenas as subperguntas que devem aparecer
    depois de uma pergunta principal.

    Exemplo:
    get_active_subquestions("P4", 1)

    Isso deve retornar as subperguntas 4A e 4B,
    porque ambas são ativadas pelas respostas 1 ou 2 da P4.
    """

    # Primeiro, buscamos todas as subperguntas ligadas à pergunta principal.
    related_subquestions = get_subquestions_by_parent(parent_question_id)

    # Depois, filtramos apenas as que devem ser ativadas
    # pela alternativa escolhida pelo usuário.
    return [
        subquestion
        for subquestion in related_subquestions
        if should_activate_subquestion(subquestion, selected_option_id)
    ]


def get_subquestion_by_id(subquestion_id):
    """
    Busca uma subpergunta específica pelo seu identificador.

    Exemplo:
    get_subquestion_by_id("7A")
    """

    for subquestion in SUBQUESTIONS:
        if subquestion["id"] == subquestion_id:
            return subquestion

    return None