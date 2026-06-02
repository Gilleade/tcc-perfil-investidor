# Testes automatizados do fluxo da interface Streamlit.
#
# Estes testes usam AppTest, ferramenta oficial do Streamlit para testar
# aplicações sem abrir o navegador.
#
# Eles não testam layout visual com screenshot.
# Eles testam se o app abre, se recebe respostas, se gera resultado,
# se limpa a simulação e se descarta resultado antigo quando respostas mudam.
#
# Para executar:
# python -m pytest tests/test_app_flow.py -v
#
# Para executar todos os testes do projeto:
# python -m pytest -v

from pathlib import Path

from streamlit.testing.v1 import AppTest


# Caminho absoluto até o app.py.
# Como este arquivo está dentro de tests/, usamos parents[1]
# para voltar para a raiz do projeto.
APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def make_app(answers=None, subanswers=None):
    """
    Cria uma instância testável do app Streamlit.

    Parâmetros:
    - answers: respostas das perguntas principais.
    - subanswers: respostas das subperguntas condicionais.

    A função injeta as respostas diretamente no st.session_state
    antes da primeira execução do app.

    Isso evita precisar clicar manualmente em todos os radios nos testes.
    """

    at = AppTest.from_file(str(APP_PATH))

    # Define o estado inicial da sessão antes do app rodar.
    at.session_state["answers"] = answers or {}
    at.session_state["subanswers"] = subanswers or {}
    at.session_state["reset_counter"] = 0
    at.session_state["classification_result"] = None
    at.session_state["justification_result"] = None
    at.session_state["result_signature"] = None
    
    at.session_state["app_started"] = True
    at.session_state["current_flow_index"] = 0
    at.session_state["questionnaire_finished"] = bool(answers)

    # Executa o app com esse estado inicial.
    at.run(timeout=10)

    return at


def click_button(at, label):
    """
    Clica em um botão pelo texto do botão.

    Isso evita depender da posição do botão na tela.
    Se a ordem dos botões mudar, o teste continua funcionando.
    """

    for button in at.button:
        if button.label == label:
            button.click().run(timeout=10)
            return at

    available_buttons = [button.label for button in at.button]

    raise AssertionError(
        f"Botão '{label}' não encontrado. Botões disponíveis: {available_buttons}"
    )


def get_rendered_text(at):
    """
    Junta textos renderizados pelo Streamlit em uma única string.

    Isso ajuda a verificar se determinada informação apareceu na tela,
    sem depender exatamente do tipo de elemento visual.
    """

    text_parts = []

    element_groups = [
        at.title,
        at.header,
        at.subheader,
        at.markdown,
        at.info,
        at.warning,
        at.success,
        at.error,
    ]

    for group in element_groups:
        for element in group:
            value = getattr(element, "value", "")
            text_parts.append(str(value))

    return "\n".join(text_parts)


def generate_result(at):
    """
    Gera o resultado no fluxo atual.

    Na versão sequencial, não existe mais botão "Gerar resultado".
    Quando questionnaire_finished está True e as respostas são válidas,
    o app gera o resultado automaticamente.
    """

    at.session_state["questionnaire_finished"] = True
    at.run(timeout=10)
    return at


def arrojado_answers():
    """
    Cenário com perfil final Arrojado.

    Bloco 1: objetivo, prazo e risco indicam perfil alto.
    Bloco 2: sem restrições financeiras.
    Bloco 3: conhecimento e experiência altos.
    """

    answers = {
        "P1": 3,
        "P2": 3,
        "P3": 3,
        "P4": 2,
        "P5": 3,
        "P6": 3,
        "P7": 3,
        "P8": 3,
        "P9": 3,
    }

    subanswers = {
        "7A": 3,
        "7B": 3,
        "8A": 3,
        "8B": 3,
    }

    return answers, subanswers


def moderado_answers():
    """
    Cenário com perfil final Moderado.

    Bloco 1: respostas intermediárias.
    Bloco 2: sem travas financeiras.
    Bloco 3: conhecimento intermediário suficiente para manter Moderado.
    """

    answers = {
        "P1": 2,
        "P2": 2,
        "P3": 2,
        "P4": 2,
        "P5": 3,
        "P6": 3,
        "P7": 2,
        "P8": 2,
        "P9": 2,
    }

    subanswers = {
        "2A": 2,
        "7A": 2,
        "8A": 2,
        "8B": 2,
    }

    return answers, subanswers


def conservador_by_financial_locks_answers():
    """
    Cenário em que o perfil preliminar é Arrojado,
    mas travas financeiras reduzem o resultado para Conservador.
    """

    answers = {
        "P1": 3,
        "P2": 3,
        "P3": 3,
        "P4": 1,
        "P5": 1,
        "P6": 1,
        "P7": 3,
        "P8": 3,
        "P9": 3,
    }

    subanswers = {
        "4A": 1,
        "4B": 1,
        "5A": 1,
        "6A": 1,
        "6B": 1,
        "7A": 3,
        "7B": 3,
        "8A": 3,
        "8B": 3,
    }

    return answers, subanswers


def test_app_opens_without_error():
    """
    Verifica se o app abre sem lançar exceções
    e se os títulos principais aparecem.
    """

    at = make_app()

    assert not at.exception

    rendered_text = get_rendered_text(at)

    assert "Objetivos e tolerância ao risco" in rendered_text
    assert "Geração do resultado" not in rendered_text


def test_generate_arrojado_result():
    """
    Verifica o fluxo de geração de resultado Arrojado.
    """

    answers, subanswers = arrojado_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    result = at.session_state["classification_result"]

    assert result is not None
    assert result["preliminary_profile"] == "Arrojado"
    assert result["financial_profile"] == "Arrojado"
    assert result["final_profile"] == "Arrojado"
    
    assert "decision_trace" in result
    assert result["decision_trace"]
    assert result["decision_trace"][-1]["id"] == "resultado_final"

    rendered_text = get_rendered_text(at)

    assert "Resultado da classificação" in rendered_text
    assert "Perfil final: Arrojado" in rendered_text
    assert "Percurso da decisão" in rendered_text
    assert "Fluxograma do percurso decisório" in rendered_text


def test_generate_moderado_result():
    """
    Verifica o fluxo de geração de resultado Moderado.
    """

    answers, subanswers = moderado_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    result = at.session_state["classification_result"]

    assert result is not None
    assert result["preliminary_profile"] == "Moderado"
    assert result["financial_profile"] == "Moderado"
    assert result["final_profile"] == "Moderado"

    rendered_text = get_rendered_text(at)

    assert "Resultado da classificação" in rendered_text
    assert "Perfil final: Moderado" in rendered_text


def test_generate_conservador_by_financial_locks_result():
    """
    Verifica o fluxo em que o perfil preliminar Arrojado
    é reduzido para Conservador por travas financeiras.
    """

    answers, subanswers = conservador_by_financial_locks_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    result = at.session_state["classification_result"]

    assert result is not None
    assert result["preliminary_profile"] == "Arrojado"
    assert result["financial_profile"] == "Conservador"
    assert result["final_profile"] == "Conservador"

    rendered_text = get_rendered_text(at)

    assert "Resultado da classificação" in rendered_text
    assert "Perfil final: Conservador" in rendered_text


def test_new_simulation_clears_result_and_answers():
    """
    Verifica se o botão Nova simulação limpa respostas e resultado.
    """

    answers, subanswers = arrojado_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    assert at.session_state["classification_result"] is not None
    assert at.session_state["justification_result"] is not None

    at = click_button(at, "Nova simulação")

    assert at.session_state["answers"] == {}
    assert at.session_state["subanswers"] == {}
    assert at.session_state["classification_result"] is None
    assert at.session_state["justification_result"] is None
    assert at.session_state["result_signature"] is None


def test_new_simulation_button_clears_state():
    """
    Verifica se o botão Nova simulação limpa respostas e resultado.
    """

    answers, subanswers = moderado_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    assert at.session_state["classification_result"] is not None

    at = click_button(at, "Nova simulação")

    assert at.session_state["answers"] == {}
    assert at.session_state["subanswers"] == {}
    assert at.session_state["classification_result"] is None
    assert at.session_state["justification_result"] is None
    assert at.session_state["result_signature"] is None


def test_result_is_regenerated_when_answers_change_after_generation():
    """
    Verifica se o resultado é atualizado quando as respostas mudam
    depois de uma classificação já gerada.

    Na versão sequencial atual, se o questionário já está finalizado
    e as respostas continuam válidas, o app remove o resultado antigo
    e gera uma nova classificação automaticamente.
    """

    answers, subanswers = arrojado_answers()

    at = make_app(answers=answers, subanswers=subanswers)
    at = generate_result(at)

    assert at.session_state["classification_result"] is not None
    assert at.session_state["justification_result"] is not None
    assert at.session_state["result_signature"] is not None

    old_signature = at.session_state["result_signature"]

    # Simula alteração de uma resposta principal depois do resultado gerado.
    updated_answers = dict(at.session_state["answers"])
    updated_answers["P1"] = 2
    at.session_state["answers"] = updated_answers

    at.session_state["reset_counter"] = at.session_state["reset_counter"] + 1

    at.run(timeout=10)

    assert at.session_state["classification_result"] is not None
    assert at.session_state["justification_result"] is not None
    assert at.session_state["result_signature"] is not None
    assert at.session_state["result_signature"] != old_signature