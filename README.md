# Sistema de Apoio à Decisão para Classificação do Perfil do Investidor

Protótipo acadêmico desenvolvido em **Python** e **Streamlit** como parte de um Trabalho de Conclusão de Curso em **Sistemas de Informação**.

O projeto implementa um sistema de apoio à decisão para **classificação do perfil do investidor**, utilizando perguntas estruturadas, subperguntas condicionais, árvore de decisão, regras explícitas e justificativa textual do resultado.

---

## Sumário

- [1. Finalidade do projeto](#1-finalidade-do-projeto)
- [2. Tema do TCC](#2-tema-do-tcc)
- [3. Objetivo do protótipo](#3-objetivo-do-protótipo)
- [4. O que o sistema faz](#4-o-que-o-sistema-faz)
- [5. O que o sistema não faz](#5-o-que-o-sistema-não-faz)
- [6. Perfis classificados](#6-perfis-classificados)
- [7. Estrutura lógica da classificação](#7-estrutura-lógica-da-classificação)
- [8. Tecnologias utilizadas](#8-tecnologias-utilizadas)
- [9. Estrutura de pastas](#9-estrutura-de-pastas)
- [10. Descrição dos módulos](#10-descrição-dos-módulos)
- [11. Como criar o ambiente com Conda](#11-como-criar-o-ambiente-com-conda)
- [12. Como instalar com pip](#12-como-instalar-com-pip)
- [13. Como executar o protótipo](#13-como-executar-o-protótipo)
- [14. Como executar os testes automatizados](#14-como-executar-os-testes-automatizados)
- [15. Fluxo de uso do sistema](#15-fluxo-de-uso-do-sistema)
- [16. Testes existentes](#16-testes-existentes)
- [17. Padrão de desenvolvimento adotado](#17-padrão-de-desenvolvimento-adotado)
- [18. Observações acadêmicas](#18-observações-acadêmicas)
- [19. Limitações do protótipo](#19-limitações-do-protótipo)
- [20. Possíveis melhorias futuras](#20-possíveis-melhorias-futuras)

---

## 1. Finalidade do projeto

Este projeto tem finalidade **acadêmica** e foi desenvolvido para demonstrar como critérios teóricos e normativos relacionados ao perfil do investidor podem ser traduzidos em uma solução computacional simples, rastreável e explicável.

A proposta não é construir uma plataforma financeira, nem um recomendador de investimentos. O foco do projeto está na **modelagem de um sistema de apoio à decisão**, no qual as respostas do usuário são processadas por regras explícitas para gerar uma classificação final acompanhada de justificativa textual.

---

## 2. Tema do TCC

**Sistema de apoio à decisão para classificação do perfil do investidor.**

O trabalho parte da ideia de que a classificação do perfil do investidor pode ser tratada como um problema decisório estruturado, no qual diferentes critérios precisam ser organizados e analisados em conjunto.

A solução proposta utiliza uma árvore de decisão baseada em regras para classificar o usuário em um dos perfis previstos no protótipo.

---

## 3. Objetivo do protótipo

O objetivo do protótipo é permitir a classificação do perfil do investidor a partir de um questionário estruturado, organizado em três blocos principais:

1. **Objetivos e tolerância ao risco**;
2. **Compatibilidade financeira**;
3. **Conhecimento e experiência**.

A partir das respostas, o sistema:

- calcula um perfil preliminar;
- aplica regras de compatibilidade financeira;
- aplica refinamento por conhecimento e experiência;
- consolida o perfil final;
- gera uma justificativa textual rastreável.

---

## 4. O que o sistema faz

O protótipo permite:

- exibir uma tela inicial com informações sobre o sistema;
- apresentar perguntas principais organizadas em blocos;
- ativar subperguntas condicionais conforme as respostas do usuário;
- validar automaticamente o preenchimento;
- indicar o andamento do questionário;
- calcular o perfil preliminar;
- aplicar travas e reduções por compatibilidade financeira;
- aplicar refinamento por conhecimento e experiência;
- consolidar o perfil final;
- exibir ajustes, bloqueios e inconsistências;
- gerar justificativa textual completa;
- permitir nova simulação;
- limpar respostas registradas;
- executar testes automatizados da lógica e do fluxo da interface.

---

## 5. O que o sistema não faz

Este sistema **não**:

- recomenda investimentos;
- indica ativos financeiros;
- monta carteiras;
- consulta dados de mercado;
- calcula rentabilidade;
- realiza previsão de preços;
- utiliza inteligência artificial;
- utiliza aprendizado de máquina;
- utiliza banco de dados;
- possui login ou autenticação;
- armazena histórico persistente de usuários;
- substitui avaliação profissional.

O resultado gerado tem finalidade **classificatória e acadêmica**.

---

## 6. Perfis classificados

O sistema classifica o usuário em um dos três perfis:

### Conservador

Perfil associado a maior prioridade para preservação de recursos, menor tolerância a oscilações e maior necessidade de segurança ou liquidez.

### Moderado

Perfil intermediário, associado ao equilíbrio entre preservação de recursos e aceitação de algum nível de oscilação em busca de crescimento ao longo do tempo.

### Arrojado

Perfil associado a maior tolerância a oscilações e perdas temporárias, horizonte mais longo e maior disposição para assumir riscos em busca de crescimento patrimonial.

A classificação final pode ser reduzida caso as respostas indiquem incompatibilidade financeira, baixa reserva, necessidade de liquidez, pouca familiaridade ou experiência insuficiente.

---

## 7. Estrutura lógica da classificação

A árvore de decisão foi organizada em três etapas principais.

### 7.1 Perfil preliminar

O perfil preliminar é formado a partir das perguntas do primeiro bloco:

- **P1** — finalidade do investimento;
- **P2** — horizonte temporal;
- **P3** — tolerância ao risco.

Essa etapa identifica uma primeira tendência de perfil: Conservador, Moderado ou Arrojado.

### 7.2 Compatibilidade financeira

Depois do perfil preliminar, o sistema verifica se esse perfil é compatível com a situação financeira informada.

São consideradas perguntas relacionadas a:

- necessidade futura de recursos;
- estabilidade de renda;
- reserva financeira ou robustez patrimonial;
- subperguntas condicionais financeiras.

Essa etapa pode:

- manter o perfil;
- reduzir um nível;
- reduzir dois níveis;
- bloquear perfil arrojado por prudência;
- registrar travas e inconsistências.

### 7.3 Conhecimento e experiência

Após a compatibilidade financeira, o sistema verifica se o conhecimento e a experiência informados confirmam ou limitam o perfil.

São consideradas perguntas relacionadas a:

- familiaridade com investimentos;
- experiência prática;
- formação ou experiência profissional relacionada;
- subperguntas condicionais de conhecimento.

Essa etapa pode:

- manter o perfil;
- reduzir o perfil;
- bloquear perfil alto por prudência;
- registrar limitações, moderações e inconsistências.

### 7.4 Consolidação final

A classificação final segue a sequência:

```text
perfil preliminar
→ compatibilidade financeira
→ refinamento por conhecimento e experiência
→ perfil final
```

O sistema preserva os resultados intermediários para gerar a justificativa textual.

---

## 8. Tecnologias utilizadas

- **Python 3.11**;
- **Streamlit**;
- **Pytest**;
- **Streamlit AppTest** para testes automatizados da interface;
- **Conda/Anaconda** para gerenciamento de ambiente.

O projeto não utiliza bibliotecas complexas, banco de dados ou APIs externas.

---

## 9. Estrutura de pastas

```text
prototipo-perfil-investidor/
│
├── app.py
├── environment.yml
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── questions.py
│   └── subquestions.py
│
├── logic/
│   ├── preliminary_profile.py
│   ├── financial_rules.py
│   ├── knowledge_rules.py
│   ├── final_consolidation.py
│   └── justification.py
│
├── ui/
│   ├── __init__.py
│   ├── debug_panel.py
│   ├── layout.py
│   ├── question_blocks.py
│   ├── questionnaire.py
│   ├── result_actions.py
│   └── result_view.py
│
├── utils/
│   ├── session.py
│   └── validation.py
│
└── tests/
    ├── __init__.py
    ├── test_app_flow.py
    └── test_logic.py
```

---

## 10. Descrição dos módulos

### `app.py`

Arquivo principal do projeto.

Responsável por coordenar o fluxo geral da aplicação:

- configurar a página do Streamlit;
- aplicar estilos visuais;
- inicializar o estado da sessão;
- renderizar o cabeçalho;
- renderizar o questionário;
- validar respostas;
- gerar resultado;
- exibir resultado;
- exibir painel técnico;
- exibir botão de limpeza.

O `app.py` foi organizado com uma função principal:

```python
def main():
    ...
```

E é executado por:

```python
if __name__ == "__main__":
    main()
```

### `data/questions.py`

Contém o cadastro das 9 perguntas principais.

Cada pergunta possui:

- identificador;
- bloco;
- eixo;
- critério;
- função lógica;
- peso lógico;
- texto;
- alternativas;
- nível lógico associado a cada alternativa.

As perguntas principais são:

- P1 — finalidade do investimento;
- P2 — horizonte temporal;
- P3 — tolerância ao risco;
- P4 — necessidade futura de recursos;
- P5 — estabilidade de renda;
- P6 — reserva financeira ou robustez patrimonial;
- P7 — familiaridade com investimentos;
- P8 — experiência prática com investimentos;
- P9 — formação ou experiência profissional relacionada.

### `data/subquestions.py`

Contém o cadastro das subperguntas condicionais.

As subperguntas aparecem apenas quando uma alternativa específica de uma pergunta principal ativa seu gatilho.

Elas são usadas para detalhar situações de:

- ambiguidade;
- necessidade de liquidez;
- estabilidade financeira;
- reserva financeira;
- familiaridade;
- experiência prática;
- compreensão de risco.

### `logic/preliminary_profile.py`

Calcula o perfil preliminar com base nas perguntas P1, P2 e P3.

Essa etapa considera:

- finalidade do investimento;
- horizonte temporal;
- tolerância ao risco.

O resultado pode ser:

- Conservador;
- Moderado;
- Arrojado.

Também registra inconsistências preliminares quando há combinações contraditórias, como alta tolerância ao risco com horizonte curto.

### `logic/financial_rules.py`

Aplica as regras de compatibilidade financeira.

Essa etapa considera:

- P4 — necessidade futura de recursos;
- P5 — estabilidade de renda;
- P6 — reserva financeira;
- subperguntas condicionais financeiras.

A função principal pode:

- manter o perfil;
- reduzir um nível;
- reduzir dois níveis;
- bloquear o perfil Arrojado;
- registrar travas fortes;
- registrar moderações;
- registrar inconsistências financeiras.

### `logic/knowledge_rules.py`

Aplica o refinamento por conhecimento e experiência.

Essa etapa considera:

- P7 — familiaridade com investimentos;
- P8 — experiência prática;
- P9 — formação ou experiência relacionada;
- subperguntas condicionais de conhecimento.

A função principal pode:

- manter o perfil;
- reduzir o perfil;
- impedir perfil alto quando há baixa familiaridade ou experiência insuficiente;
- registrar limitações;
- registrar moderações;
- registrar confirmações;
- registrar inconsistências.

O conhecimento e a experiência não elevam o perfil isoladamente.

### `logic/final_consolidation.py`

Centraliza a chamada das etapas lógicas:

1. cálculo do perfil preliminar;
2. compatibilidade financeira;
3. refinamento por conhecimento e experiência;
4. consolidação do perfil final.

Esse módulo preserva:

- perfil preliminar;
- perfil após compatibilidade financeira;
- perfil final;
- ajustes realizados;
- inconsistências;
- perfis bloqueados;
- logs internos.

### `logic/justification.py`

Gera a justificativa textual da classificação.

A justificativa explica:

- perfil preliminar;
- efeitos da compatibilidade financeira;
- efeitos do conhecimento e experiência;
- travas, reduções e bloqueios;
- inconsistências;
- perfil final.

Esse módulo não calcula o perfil. Ele apenas transforma o resultado consolidado em texto explicativo.

### `ui/layout.py`

Contém elementos visuais gerais da interface:

- estilos CSS;
- cabeçalho;
- textos introdutórios dos blocos;
- status automático de preenchimento;
- barra de progresso;
- listagem de pendências.

### `ui/question_blocks.py`

Renderiza perguntas principais e subperguntas condicionais.

Também controla:

- seleção das alternativas;
- ausência de alternativa marcada inicialmente;
- armazenamento das respostas no `st.session_state`;
- exibição de resumo técnico;
- exibição de detalhes técnicos em expansores.

### `ui/questionnaire.py`

Monta os três blocos do questionário:

- Bloco 1 — Objetivos e tolerância ao risco;
- Bloco 2 — Compatibilidade financeira;
- Bloco 3 — Conhecimento e experiência.

Retorna a lista de subperguntas ativas para validação e limpeza de respostas antigas.

### `ui/result_actions.py`

Renderiza a seção de geração do resultado.

Responsável por:

- exibir o botão “Gerar resultado”;
- habilitar o botão apenas quando o questionário está completo;
- chamar a consolidação final;
- chamar a geração da justificativa;
- salvar resultado e justificativa na sessão.

### `ui/result_view.py`

Renderiza a tela de resultado.

Exibe:

- perfil final;
- perfil preliminar;
- perfil após compatibilidade financeira;
- resumo textual;
- ajustes realizados;
- bloqueios;
- inconsistências;
- justificativa textual completa;
- botão “Nova simulação”.

### `ui/debug_panel.py`

Renderiza o painel técnico de respostas e o botão de limpeza.

Contém:

- painel expansível “Ver respostas registradas”;
- respostas principais armazenadas;
- respostas de subperguntas armazenadas;
- botão “Limpar respostas”.

### `utils/session.py`

Centraliza o controle do estado da sessão.

Responsável por:

- inicializar `st.session_state`;
- limpar simulação;
- remover respostas de subperguntas inativas;
- gerar assinatura das respostas;
- remover resultado antigo quando as respostas mudam.

### `utils/validation.py`

Valida o preenchimento obrigatório do questionário.

Verifica:

- perguntas principais pendentes;
- subperguntas condicionais ativas pendentes;
- status geral de validade.

### `tests/test_logic.py`

Contém testes automatizados da lógica da árvore de decisão.

Testa:

- perfil preliminar;
- compatibilidade financeira;
- refinamento por conhecimento;
- consolidação final;
- justificativa textual.

### `tests/test_app_flow.py`

Contém testes automatizados do fluxo principal da interface Streamlit.

Testa:

- abertura do app;
- geração de perfil Arrojado;
- geração de perfil Moderado;
- geração de perfil Conservador por travas financeiras;
- nova simulação;
- limpeza de respostas;
- remoção de resultado antigo quando respostas mudam.

---

## 11. Como criar o ambiente com Conda

Este é o caminho recomendado para o projeto.

No Anaconda Prompt ou PowerShell, entre na pasta do projeto:

```bash
cd caminho/para/prototipo-perfil-investidor
```

Crie o ambiente:

```bash
conda env create -f environment.yml
```

Ative o ambiente:

```bash
conda activate tcc-perfil-investidor
```

Depois confirme se o Python está disponível:

```bash
python --version
```

---

## 12. Como instalar com pip

Caso não utilize Conda, também é possível instalar as dependências com pip:

```bash
pip install -r requirements.txt
```

Dependências principais:

```text
streamlit
pytest
```

---

## 13. Como executar o protótipo

Com o ambiente ativo, execute:

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador.

Caso não abra automaticamente, o terminal mostrará um endereço local parecido com:

```text
http://localhost:8501
```

---

## 14. Como executar os testes automatizados

Para executar todos os testes:

```bash
python -m pytest -v
```

Resultado esperado:

```text
24 passed
```

Também é possível executar apenas os testes da lógica:

```bash
python -m pytest tests/test_logic.py -v
```

Ou apenas os testes da interface:

```bash
python -m pytest tests/test_app_flow.py -v
```

---

## 15. Fluxo de uso do sistema

1. Abrir o protótipo com `streamlit run app.py`.
2. Ler o aviso de finalidade acadêmica.
3. Responder às perguntas do Bloco 1.
4. Responder às perguntas do Bloco 2.
5. Responder às perguntas do Bloco 3.
6. Responder às subperguntas condicionais, quando forem exibidas.
7. Acompanhar o andamento do preenchimento.
8. Gerar o resultado quando o questionário estiver completo.
9. Ler o perfil final e a justificativa textual.
10. Iniciar nova simulação ou limpar respostas.

---

## 16. Testes existentes

O projeto possui dois grupos de testes automatizados.

### Testes da lógica

Arquivo:

```text
tests/test_logic.py
```

Esses testes verificam a lógica da árvore de decisão sem depender da interface visual.

Cobrem:

- perfil preliminar Conservador;
- perfil preliminar Moderado;
- perfil preliminar Arrojado;
- inconsistência entre risco alto e horizonte curto;
- manutenção de Arrojado sem restrições financeiras;
- redução de Arrojado para Moderado por trava forte;
- redução de Arrojado para Conservador por fragilidade financeira;
- manutenção de Arrojado com alto conhecimento;
- redução de Arrojado para Moderado com conhecimento intermediário;
- manutenção de Moderado com conhecimento intermediário;
- impedimento de elevação de Conservador por conhecimento alto;
- consolidação final;
- geração de justificativa.

### Testes da interface

Arquivo:

```text
tests/test_app_flow.py
```

Esses testes utilizam `streamlit.testing.v1.AppTest` para simular o app sem abrir o navegador.

Cobrem:

- abertura do app sem erro;
- geração de resultado Arrojado;
- geração de resultado Moderado;
- geração de resultado Conservador por travas financeiras;
- funcionamento de “Nova simulação”;
- funcionamento de “Limpar respostas”;
- remoção de resultado antigo após alteração nas respostas.

---

## 17. Padrão de desenvolvimento adotado

O projeto foi organizado para manter separação entre:

- dados do questionário;
- lógica de classificação;
- componentes de interface;
- utilitários de sessão e validação;
- testes automatizados.

Essa separação facilita:

- manutenção;
- rastreabilidade;
- revisão acadêmica;
- demonstração para banca;
- evolução futura do protótipo.

A estrutura geral segue o princípio:

```text
data → logic → ui → utils → tests
```

---

## 18. Observações acadêmicas

Este protótipo foi desenvolvido como artefato aplicado de um TCC em Sistemas de Informação.

A proposta acadêmica é demonstrar como critérios de classificação do perfil do investidor podem ser:

1. identificados em literatura e referenciais técnicos;
2. transformados em perguntas estruturadas;
3. organizados em regras explícitas;
4. implementados em um protótipo funcional;
5. testados por casos simulados;
6. explicados por justificativa textual.

O protótipo reforça a ideia de sistema de apoio à decisão explicável, pois o resultado final não aparece isolado: ele é acompanhado de informações sobre perfil preliminar, ajustes aplicados, bloqueios, inconsistências e justificativa.

---

## 19. Limitações do protótipo

O sistema possui limitações intencionais, coerentes com seu escopo acadêmico:

- não possui banco de dados;
- não armazena histórico;
- não possui autenticação;
- não permite cadastro de usuários;
- não possui painel administrativo;
- não consulta fontes externas;
- não realiza recomendação financeira;
- não utiliza inteligência artificial;
- não substitui ferramentas profissionais de suitability.

Essas limitações reduzem a complexidade e mantêm o foco na modelagem da árvore de decisão e na explicabilidade do processo classificatório.

---

## 20. Possíveis melhorias futuras

Possíveis evoluções do projeto incluem:

- geração de relatório em PDF;
- melhoria visual da tela de resultado;
- exportação da justificativa textual;
- criação de modo de demonstração para banca;
- ampliação dos testes simulados;
- parametrização externa das perguntas;
- armazenamento opcional de simulações locais;
- melhoria da documentação técnica;
- criação de versão empacotada para execução simplificada.

Essas melhorias não fazem parte do escopo principal do protótipo atual, mas podem ser consideradas em trabalhos futuros.

---

## Status atual

O protótipo possui:

- questionário estruturado;
- subperguntas condicionais;
- validação automática;
- classificação final;
- justificativa textual;
- interface em Streamlit;
- código modularizado;
- ambiente documentado;
- testes automatizados.

Com isso, o projeto está preparado para a etapa seguinte do TCC: **testes acadêmicos com casos simulados e análise dos resultados**.
