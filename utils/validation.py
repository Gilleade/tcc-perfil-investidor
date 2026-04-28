# Importa as perguntas principais cadastradas no sistema.
from data.questions import get_all_questions

# Importa função para buscar dados de uma subpergunta pelo id.
from data.subquestions import get_subquestion_by_id


def validate_required_answers(answers, subanswers, active_subquestion_ids):
    """
    Valida se todas as perguntas obrigatórias foram respondidas.

    Parâmetros:
    - answers: dicionário com respostas das perguntas principais.
      Exemplo: {"P1": 2, "P2": 1}

    - subanswers: dicionário com respostas das subperguntas condicionais.
      Exemplo: {"4A": 1, "4B": 2}

    - active_subquestion_ids: lista com os ids das subperguntas que estão ativas.
      Exemplo: ["4A", "4B", "7A"]

    Retorno:
    Um dicionário contendo:
    - is_valid: True ou False;
    - missing_questions: lista de perguntas principais pendentes;
    - missing_subquestions: lista de subperguntas pendentes.
    """

    # Lista que armazenará perguntas principais sem resposta.
    missing_questions = []

    # Lista que armazenará subperguntas ativas sem resposta.
    missing_subquestions = []

    # ---------------------------------------------------------------
    # Validação das perguntas principais
    # ---------------------------------------------------------------
    #
    # Todas as 9 perguntas principais são obrigatórias.
    # Por isso, percorremos todas as perguntas cadastradas em questions.py.

    for question in get_all_questions():
        question_id = question["id"]

        # Se o id da pergunta não estiver no dicionário de respostas,
        # significa que ela ainda não foi respondida.
        if question_id not in answers or answers.get(question_id) is None:
            missing_questions.append(
                {
                    "id": question_id,
                    "text": question["text"],
                    "block": question["block"],
                }
            )

    # ---------------------------------------------------------------
    # Validação das subperguntas condicionais
    # ---------------------------------------------------------------
    #
    # As subperguntas só são obrigatórias quando estão ativas.
    # Por isso, validamos apenas os ids recebidos em active_subquestion_ids.

    for subquestion_id in active_subquestion_ids:
        if subquestion_id not in subanswers or subanswers.get(subquestion_id) is None:
            subquestion = get_subquestion_by_id(subquestion_id)

            # Se a subpergunta for encontrada no cadastro, usamos seus dados.
            if subquestion is not None:
                missing_subquestions.append(
                    {
                        "id": subquestion_id,
                        "text": subquestion["text"],
                        "parent_question_id": subquestion["parent_question_id"],
                    }
                )

            # Caso não seja encontrada, registramos uma pendência técnica.
            # Isso ajuda a identificar erro de cadastro no futuro.
            else:
                missing_subquestions.append(
                    {
                        "id": subquestion_id,
                        "text": "Subpergunta não encontrada no cadastro.",
                        "parent_question_id": None,
                    }
                )

    # A validação só é considerada correta se não houver nenhuma pendência.
    is_valid = len(missing_questions) == 0 and len(missing_subquestions) == 0

    return {
        "is_valid": is_valid,
        "missing_questions": missing_questions,
        "missing_subquestions": missing_subquestions,
    }