# Sistema de Apoio à Decisão para Classificação do Perfil do Investidor

Protótipo acadêmico desenvolvido em Python e Streamlit para classificação do perfil do investidor a partir de perguntas estruturadas, subperguntas condicionais e regras explícitas de classificação.

O sistema classifica o usuário em um dos três perfis:

* Conservador;
* Moderado;
* Arrojado.

A classificação é realizada por meio de um processamento sequencial organizado em três blocos:

1. Objetivos e tolerância ao risco;
2. Compatibilidade financeira;
3. Conhecimento e experiência.

O protótipo foi desenvolvido como parte de um Trabalho de Conclusão de Curso em Sistemas de Informação, com a finalidade de demonstrar como critérios teóricos e técnicos de classificação do perfil do investidor podem ser operacionalizados em um sistema de apoio à decisão baseado em regras explícitas.

## Objetivo do protótipo

O objetivo do protótipo é demonstrar, de forma funcional, a aplicação de uma lógica de classificação do perfil do investidor a partir de critérios previamente definidos.

A solução transforma respostas fornecidas pelo usuário em uma classificação final, considerando:

* a orientação inicial indicada pelos objetivos e pela tolerância ao risco;
* a compatibilidade financeira informada;
* o conhecimento e a experiência declarados;
* os limites e refinamentos previstos nas regras de classificação;
* a justificativa textual associada ao resultado.

O sistema não realiza recomendação de investimentos, não indica produtos financeiros, não monta carteiras e não substitui avaliação profissional.

## Escopo da solução

O protótipo contempla:

* apresentação de perguntas principais organizadas por blocos;
* acionamento de subperguntas condicionais quando necessário;
* validação do preenchimento obrigatório;
* cálculo do perfil preliminar;
* aplicação da compatibilidade financeira;
* aplicação do refinamento por conhecimento e experiência;
* consolidação do perfil final;
* geração de justificativa textual;
* exibição do resultado ao usuário;
* possibilidade de iniciar uma nova simulação;
* testes automatizados e casos simulados.

O protótipo não contempla:

* login de usuários;
* banco de dados;
* armazenamento de histórico;
* integração com APIs externas;
* consulta a cotações ou dados de mercado;
* recomendação de ativos financeiros;
* suitability regulatório completo;
* uso de inteligência artificial ou aprendizagem de máquina.

## Tecnologias utilizadas

* Python;
* Streamlit;
* Pytest.

O Python foi utilizado para implementar a lógica de classificação, as validações, a consolidação do perfil final e a geração da justificativa textual. O Streamlit foi utilizado para construir a interface interativa do protótipo. O Pytest foi utilizado para apoiar a verificação automatizada da lógica implementada.

## Estrutura do projeto

```text
tcc-perfil-investidor-main/
├── app.py
├── data/
│   ├── questions.py
│   └── subquestions.py
├── logic/
│   ├── decision_trace.py
│   ├── final_consolidation.py
│   ├── financial_rules.py
│   ├── justification.py
│   ├── knowledge_rules.py
│   └── preliminary_profile.py
├── ui/
│   ├── layout.py
│   ├── question_blocks.py
│   ├── questionnaire.py
│   ├── result_actions.py
│   └── result_view.py
├── utils/
│   ├── session.py
│   └── validation.py
├── tests/
│   ├── test_app_flow.py
│   ├── test_cases.py
│   └── test_logic.py
├── environment.yml
├── requirements.txt
├── run_test_cases.py
└── README.md
```

## Organização dos módulos

### Arquivo principal

O arquivo `app.py` concentra o fluxo principal da aplicação. Ele inicializa a interface, controla o estado da sessão, apresenta o questionário, valida as respostas e aciona a geração do resultado.

### Base de perguntas

A pasta `data/` contém a estrutura de entrada do sistema:

* `questions.py`: define as perguntas principais, seus blocos, critérios e alternativas;
* `subquestions.py`: define as subperguntas condicionais, seus gatilhos e alternativas.

Esses arquivos representam a base lógica do instrumento de classificação.

### Regras de classificação

A pasta `logic/` contém os módulos responsáveis pelo processamento das respostas:

* `preliminary_profile.py`: calcula o perfil preliminar com base no Bloco 1;
* `financial_rules.py`: aplica as regras de compatibilidade financeira do Bloco 2;
* `knowledge_rules.py`: aplica o refinamento por conhecimento e experiência do Bloco 3;
* `final_consolidation.py`: consolida o perfil final a partir das etapas anteriores;
* `justification.py`: gera a justificativa textual do resultado;
* `decision_trace.py`: registra os elementos necessários para rastrear o percurso lógico da classificação.

### Interface

A pasta `ui/` contém os componentes responsáveis pela apresentação visual do protótipo:

* `layout.py`: define estilos e estrutura visual;
* `questionnaire.py`: controla a apresentação do questionário;
* `question_blocks.py`: renderiza os blocos de perguntas e subperguntas;
* `result_actions.py`: executa a classificação e salva o resultado na sessão;
* `result_view.py`: exibe o perfil final, o resumo da classificação, os pontos de atenção e a justificativa textual.

### Utilitários

A pasta `utils/` contém funções auxiliares:

* `session.py`: inicializa e limpa os dados mantidos temporariamente durante a simulação;
* `validation.py`: verifica se as perguntas obrigatórias e as subperguntas ativadas foram respondidas antes da geração do resultado.

### Testes

A pasta `tests/` contém os testes automatizados e os casos simulados utilizados para verificar o comportamento do protótipo:

* `test_logic.py`: testa funções centrais da lógica de classificação;
* `test_app_flow.py`: testa o fluxo da aplicação com apoio dos recursos de teste do Streamlit;
* `test_cases.py`: reúne casos simulados de classificação.

O arquivo `run_test_cases.py` executa os casos simulados e gera uma síntese dos resultados.

## Funcionamento geral

O funcionamento do protótipo segue uma sequência organizada em entrada, processamento e saída.

Na etapa de entrada, o usuário responde às perguntas principais e, quando necessário, às subperguntas condicionais. As subperguntas são exibidas apenas quando uma resposta anterior ativa determinado gatilho.

Na etapa de processamento, o sistema valida o preenchimento e aplica as regras de classificação. Primeiro, calcula o perfil preliminar a partir dos objetivos e da tolerância ao risco. Em seguida, verifica a compatibilidade financeira e define limites para a classificação. Depois, aplica o refinamento por conhecimento e experiência. Por fim, consolida o perfil final.

Na etapa de saída, o sistema apresenta o perfil final, um resumo da classificação, os ajustes realizados, os pontos de atenção identificados e a justificativa textual do resultado.

## Instalação do ambiente

### Opção 1 — Usando Conda

Crie o ambiente a partir do arquivo `environment.yml`:

```bash
conda env create -f environment.yml
```

Ative o ambiente:

```bash
conda activate tcc-perfil-investidor
```

### Opção 2 — Usando venv e pip

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar o protótipo

Com o ambiente ativado, execute:

```bash
streamlit run app.py
```

Após a execução, o Streamlit abrirá a aplicação no navegador. O usuário poderá iniciar a classificação, responder ao instrumento e visualizar o perfil final gerado pelo sistema.

## Como executar os testes

Para executar todos os testes automatizados:

```bash
python -m pytest -v
```

Para executar apenas os testes da lógica de classificação:

```bash
python -m pytest tests/test_logic.py -v
```

Para executar os casos simulados:

```bash
python run_test_cases.py
```

Os resultados dos casos simulados podem ser gerados na pasta `test_outputs/`. Essa pasta não é versionada, pois contém arquivos produzidos durante a execução dos testes.

## Perfis classificados

O sistema pode gerar três perfis finais:

### Conservador

Perfil associado à maior prioridade para preservação, menor exposição a oscilações ou presença de limitações relevantes nos critérios financeiros ou de conhecimento.

### Moderado

Perfil associado ao equilíbrio entre segurança e busca de crescimento, desde que a situação financeira e o conhecimento informados sustentem esse nível de exposição.

### Arrojado

Perfil associado à maior aceitação de oscilações e perdas temporárias, desde que haja compatibilidade entre objetivos, condição financeira, conhecimento e experiência.

Os perfis não representam uma escala de melhor ou pior. Eles indicam diferentes níveis de compatibilidade entre objetivos, situação financeira, tolerância ao risco e conhecimento sobre investimentos.

## Finalidade acadêmica

Este protótipo possui finalidade acadêmica e demonstrativa. Seu objetivo é apresentar a implementação de um sistema de apoio à decisão baseado em regras explícitas para classificação do perfil do investidor.

O sistema não deve ser utilizado como ferramenta profissional de recomendação financeira. A classificação gerada depende das respostas informadas pelo usuário e das regras definidas no escopo do trabalho.
