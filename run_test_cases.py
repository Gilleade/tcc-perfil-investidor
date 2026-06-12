import json
from pathlib import Path

from logic.final_consolidation import consolidate_final_profile
from logic.justification import generate_justification
from tests.test_cases import TEST_CASES


OUTPUT_DIR = Path("test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

JSON_PATH = OUTPUT_DIR / "test_cases_results.json"
MD_PATH = OUTPUT_DIR / "test_cases_results.md"


def compare_case(case, consolidated):
    expected = case["expected"]

    prelim_ok = consolidated["preliminary_profile"] == expected["preliminary"]
    fin_ok = consolidated["financial_profile"] == expected["financial"]
    final_ok = consolidated["final_profile"] == expected["final"]

    return {
        "preliminary_ok": prelim_ok,
        "financial_ok": fin_ok,
        "final_ok": final_ok,
        "all_ok": prelim_ok and fin_ok and final_ok,
    }


def build_console_block(case, consolidated, justification, comparison):
    return [
        f"=== {case['code']} — {case['description']} ===",
        f"Validação principal: {case['validate']}",
        f"Esperado: preliminar={case['expected']['preliminary']}, "
        f"financeiro={case['expected']['financial']}, "
        f"final={case['expected']['final']}",
        f"Obtido:   preliminar={consolidated['preliminary_profile']}, "
        f"financeiro={consolidated['financial_profile']}, "
        f"final={consolidated['final_profile']}",
        f"Status: {'OK' if comparison['all_ok'] else 'DIVERGÊNCIA'}",
        "Resumo da justificativa:",
        justification["summary"],
        "Inconsistências registradas:",
        json.dumps(consolidated.get("inconsistencies", []), ensure_ascii=False),
        "Perfis bloqueados:",
        json.dumps(consolidated.get("blocked_profiles", []), ensure_ascii=False),
        "Ajustes:",
        json.dumps(consolidated.get("adjustments", []), ensure_ascii=False, indent=2),
        "Justificativa completa:",
        justification["full_text"],
        "",
    ]


def build_markdown_report(results):
    lines = ["# Resultados do Teste de Casos", ""]
    for item in results:
        case = item["case"]
        consolidated = item["consolidated"]
        justification = item["justification"]
        comparison = item["comparison"]

        lines.append(f"## {case['code']} — {case['description']}")
        lines.append("")
        lines.append(f"- **Validação principal:** {case['validate']}")
        lines.append(
            f"- **Esperado:** preliminar={case['expected']['preliminary']}, "
            f"financeiro={case['expected']['financial']}, "
            f"final={case['expected']['final']}"
        )
        lines.append(
            f"- **Obtido:** preliminar={consolidated['preliminary_profile']}, "
            f"financeiro={consolidated['financial_profile']}, "
            f"final={consolidated['final_profile']}"
        )
        lines.append(f"- **Status:** {'OK' if comparison['all_ok'] else 'DIVERGÊNCIA'}")
        lines.append("")
        lines.append("### Justificativa")
        lines.append("")
        lines.append(justification["full_text"])
        lines.append("")
        lines.append("### Inconsistências")
        lines.append("")
        inconsistencies = consolidated.get("inconsistencies", [])
        if inconsistencies:
            for inc in inconsistencies:
                lines.append(f"- {inc}")
        else:
            lines.append("- Nenhuma.")
        lines.append("")
    return "\n".join(lines)


def main():
    all_results = []

    print("\n===== EXECUÇÃO AUTOMÁTICA Do TESTE DE CASOS =====\n")

    for case in TEST_CASES:
        consolidated = consolidate_final_profile(case["answers"], case["subanswers"])
        justification = generate_justification(consolidated)
        comparison = compare_case(case, consolidated)

        result_item = {
            "case": case,
            "consolidated": consolidated,
            "justification": justification,
            "comparison": comparison,
        }
        all_results.append(result_item)

        for line in build_console_block(case, consolidated, justification, comparison):
            print(line)

    json_ready = []
    for item in all_results:
        json_ready.append({
            "case": item["case"],
            "consolidated": item["consolidated"],
            "justification": item["justification"],
            "comparison": item["comparison"],
        })

    JSON_PATH.write_text(
        json.dumps(json_ready, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    MD_PATH.write_text(
        build_markdown_report(all_results),
        encoding="utf-8"
    )

    total = len(all_results)
    ok = sum(1 for item in all_results if item["comparison"]["all_ok"])
    fail = total - ok

    print("\n===== RESUMO FINAL =====")
    print(f"Total de casos: {total}")
    print(f"Casos OK: {ok}")
    print(f"Casos com divergência: {fail}")
    print(f"Arquivo JSON: {JSON_PATH}")
    print(f"Arquivo Markdown: {MD_PATH}")


if __name__ == "__main__":
    main()