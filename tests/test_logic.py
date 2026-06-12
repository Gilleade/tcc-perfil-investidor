# Testes automatizados da lógica do protótipo.
#
# Estes testes não avaliam a interface Streamlit.
# Eles testam apenas as funções do modelo de classificação baseado em regras.
#
# Para executar:
# python -m unittest discover -s tests -v

import unittest

from logic.preliminary_profile import calculate_preliminary_profile
from logic.financial_rules import apply_financial_compatibility
from logic.knowledge_rules import apply_knowledge_refinement
from logic.final_consolidation import consolidate_final_profile
from logic.justification import generate_justification


class TestPreliminaryProfile(unittest.TestCase):
    """
    Testa a formação do perfil preliminar com P1, P2 e P3.
    """

    def test_preliminary_conservador(self):
        result = calculate_preliminary_profile({"P1": 1, "P2": 1, "P3": 1})
        self.assertEqual(result["profile"], "Conservador")

    def test_preliminary_moderado(self):
        result = calculate_preliminary_profile({"P1": 2, "P2": 2, "P3": 2})
        self.assertEqual(result["profile"], "Moderado")

    def test_preliminary_arrojado(self):
        result = calculate_preliminary_profile({"P1": 3, "P2": 3, "P3": 3})
        self.assertEqual(result["profile"], "Arrojado")

    def test_preliminary_high_risk_with_short_horizon_not_arrojado(self):
        result = calculate_preliminary_profile({"P1": 3, "P2": 1, "P3": 3})

        self.assertEqual(result["profile"], "Moderado")
        self.assertTrue(len(result["inconsistencies"]) > 0)


class TestFinancialCompatibility(unittest.TestCase):
    """
    Testa as regras de compatibilidade financeira.
    """

    def test_financial_maintains_arrojado_without_restrictions(self):
        result = apply_financial_compatibility(
            "Arrojado",
            {"P4": 2, "P5": 3, "P6": 3},
            {}
        )

        self.assertEqual(result["profile"], "Arrojado")
        self.assertEqual(result["reduction_steps"], 0)

    def test_financial_reduces_arrojado_to_moderado_by_planned_liquidity(self):
        result = apply_financial_compatibility(
            "Arrojado",
            {"P4": 1, "P5": 3, "P6": 3},
            {"4A": 2, "4B": 3}
        )

        self.assertEqual(result["profile"], "Moderado")
        self.assertEqual(result["reduction_steps"], 1)
        
    def test_financial_keeps_arrojado_when_liquidity_is_not_relevant(self):
        result = apply_financial_compatibility(
            "Arrojado",
            {"P4": 1, "P5": 3, "P6": 3},
            {"4A": 3, "4B": 3}
        )

        self.assertEqual(result["profile"], "Arrojado")
        self.assertEqual(result["reduction_steps"], 0)

    def test_financial_reduces_arrojado_to_conservador_by_fragility(self):
        result = apply_financial_compatibility(
            "Arrojado",
            {"P4": 1, "P5": 1, "P6": 1},
            {}
        )

        self.assertEqual(result["profile"], "Conservador")
        self.assertEqual(result["reduction_steps"], 2)


class TestKnowledgeRefinement(unittest.TestCase):
    """
    Testa o refinamento por conhecimento e experiência.
    """

    def test_knowledge_maintains_arrojado_with_high_knowledge(self):
        result = apply_knowledge_refinement(
            "Arrojado",
            {"P7": 3, "P8": 3, "P9": 3},
            {"7A": 3, "7B": 3, "8A": 3, "8B": 3}
        )

        self.assertEqual(result["profile"], "Arrojado")
        self.assertEqual(result["reduction_steps"], 0)

    def test_knowledge_reduces_arrojado_to_moderado_with_intermediate_knowledge(self):
        result = apply_knowledge_refinement(
            "Arrojado",
            {"P7": 2, "P8": 2, "P9": 2},
            {"7A": 2, "8A": 2, "8B": 2}
        )

        self.assertEqual(result["profile"], "Moderado")
        self.assertEqual(result["reduction_steps"], 1)

    def test_knowledge_keeps_moderado_with_intermediate_knowledge(self):
        result = apply_knowledge_refinement(
            "Moderado",
            {"P7": 2, "P8": 2, "P9": 2},
            {"7A": 2, "8A": 2, "8B": 2}
        )

        self.assertEqual(result["profile"], "Moderado")
        self.assertEqual(result["reduction_steps"], 0)

    def test_knowledge_does_not_raise_conservador(self):
        result = apply_knowledge_refinement(
            "Conservador",
            {"P7": 3, "P8": 3, "P9": 3},
            {"7A": 3, "7B": 3, "8A": 3, "8B": 3}
        )

        self.assertEqual(result["profile"], "Conservador")
        self.assertEqual(result["reduction_steps"], 0)


class TestFinalConsolidation(unittest.TestCase):
    """
    Testa a consolidação completa da classificação.
    """

    def test_final_arrojado_full_compatibility(self):
        answers = {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        }

        subanswers = {
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        }

        result = consolidate_final_profile(answers, subanswers)

        self.assertEqual(result["preliminary_profile"], "Arrojado")
        self.assertEqual(result["financial_profile"], "Arrojado")
        self.assertEqual(result["final_profile"], "Arrojado")

    def test_final_arrojado_reduced_to_conservador_by_financial_fragility(self):
        answers = {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 1, "P5": 1, "P6": 1,
            "P7": 3, "P8": 3, "P9": 3,
        }

        subanswers = {
            "4A": 1, "4B": 1,
            "5A": 1,
            "6A": 1, "6B": 1,
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        }

        result = consolidate_final_profile(answers, subanswers)

        self.assertEqual(result["preliminary_profile"], "Arrojado")
        self.assertEqual(result["financial_profile"], "Conservador")
        self.assertEqual(result["final_profile"], "Conservador")

    def test_final_moderado_kept_when_financial_and_knowledge_are_adequate(self):
        answers = {
            "P1": 2, "P2": 2, "P3": 2,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 2, "P8": 2, "P9": 2,
        }

        subanswers = {
            "7A": 2,
            "8A": 2, "8B": 2,
        }

        result = consolidate_final_profile(answers, subanswers)

        self.assertEqual(result["preliminary_profile"], "Moderado")
        self.assertEqual(result["financial_profile"], "Moderado")
        self.assertEqual(result["final_profile"], "Moderado")

    def test_final_conservador_not_raised_by_high_knowledge(self):
        answers = {
            "P1": 1, "P2": 1, "P3": 1,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        }

        subanswers = {
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        }

        result = consolidate_final_profile(answers, subanswers)

        self.assertEqual(result["preliminary_profile"], "Conservador")
        self.assertEqual(result["financial_profile"], "Conservador")
        self.assertEqual(result["final_profile"], "Conservador")


class TestJustification(unittest.TestCase):
    """
    Testa se a justificativa textual é gerada a partir do resultado consolidado.
    """

    def test_justification_summary_for_arrojado(self):
        answers = {
            "P1": 3, "P2": 3, "P3": 3,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 3, "P8": 3, "P9": 3,
        }

        subanswers = {
            "7A": 3, "7B": 3,
            "8A": 3, "8B": 3,
        }

        consolidated = consolidate_final_profile(answers, subanswers)
        justification = generate_justification(consolidated)

        self.assertIn("perfil final Arrojado", justification["summary"])

    def test_justification_full_text_contains_sections(self):
        answers = {
            "P1": 2, "P2": 2, "P3": 2,
            "P4": 2, "P5": 3, "P6": 3,
            "P7": 2, "P8": 2, "P9": 2,
        }

        subanswers = {
            "7A": 2,
            "8A": 2, "8B": 2,
        }

        consolidated = consolidate_final_profile(answers, subanswers)
        justification = generate_justification(consolidated)

        self.assertIn("Perfil preliminar", justification["full_text"])
        self.assertIn("Compatibilidade financeira", justification["full_text"])
        self.assertIn("Conhecimento e experiência", justification["full_text"])
        self.assertIn("Resultado final", justification["full_text"])


if __name__ == "__main__":
    unittest.main()