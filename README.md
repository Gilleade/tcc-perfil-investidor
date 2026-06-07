# Sistema de Apoio à Decisão para Classificação do Perfil do Investidor

Protótipo acadêmico desenvolvido em Python e Streamlit para classificação do perfil do investidor a partir de perguntas estruturadas, subperguntas condicionais e regras explícitas.

O sistema classifica o usuário em um dos três perfis:

* Conservador
* Moderado
* Arrojado

A classificação é feita por meio de um fluxo lógico dividido em três blocos:

1. Objetivos e tolerância ao risco;
2. Compatibilidade financeira;
3. Conhecimento e experiência.

## Objetivo do protótipo

O objetivo do protótipo é demonstrar, de forma funcional, como critérios de classificação do perfil do investidor podem ser organizados em um Sistema de Apoio à Decisão baseado em regras explícitas.

O sistema não utiliza inteligência artificial, não recomenda investimentos, não indica produtos financeiros e não consulta dados de mercado.

## Tecnologias utilizadas

* Python
* Streamlit
* Pytest

## Estrutura do projeto

```text
tcc-perfil-investidor-main/
├── app.py
├── data/
│   ├── questions.py
│   └── subquestions.py
├── logic/
│   ├── preliminary_profile.py
│   ├── financial_rules.py
│   ├── knowledge_rules.py
│   ├── final_consolidation.py
│   ├── justification.py
│   └── decision_trace.py
├── ui/
│   ├── layout.py
│   ├── questionnaire.py
│   ├── question_blocks.py
│   ├── result_actions.py
│   └── result_view.py
├── utils/
│   ├── session.py
│   └── validation.py
├── tests/
├── run_test_cases.py
└── README.md
```

## Funcionamento geral

O protótipo apresenta perguntas principais e, quando necessário, exibe subperguntas condicionais.

As respostas são processadas em etapas:

1. cálculo do perfil preliminar;
2. aplicação das regras de compatibilidade financeira;
3. aplicação do refinamento por conhecimento e experiência;
4. consolidação do perfil final;
5. geração da justificativa textual.

A tela de resultado apresenta o perfil final, a justificativa e o percurso lógico utilizado na classificação.

## Como executar

Ative o ambiente Python utilizado no projeto e execute:

```bash
streamlit run app.py
```

## Como rodar os testes

Para executar os testes automatizados:

```bash
python -m pytest -v
```

Para executar os casos simulados usados na análise do protótipo:

```bash
python run_test_cases.py
```

## Limites do protótipo

Este sistema possui finalidade acadêmica e demonstrativa.

O protótipo não:

* recomenda ativos financeiros;
* monta carteira de investimentos;
* consulta cotações ou dados de mercado;
* substitui avaliação profissional;
* realiza suitability regulatório completo;
* utiliza inteligência artificial;
* armazena histórico de usuários;
* possui login ou banco de dados.

## Situação atual

O protótipo está estruturado para apoiar a etapa de testes e análise do TCC, permitindo verificar se as respostas simuladas geram classificações coerentes com as regras documentadas.
