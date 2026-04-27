# O streamlit é a biblioteca que transforma o arquivo Python em uma aplicação web local.
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Classificação do Perfil do Investidor",
    page_icon="📊",
    layout="centered"
)

# Cria o título principal da aplicação
st.title("Sistema de Apoio à Decisão para Classificação do Perfil do Investidor")

# Serve para escrever textos, mostrar variáveis, tabelas e outros conteúdos.
st.write(
    "Este protótipo tem finalidade acadêmica e foi desenvolvido para apoiar a "
    "classificação do perfil do investidor com base em critérios estruturados."
)

# Cria uma caixa visual de alerta
st.warning(
    "Atenção: este sistema não recomenda investimentos, não indica produtos "
    "financeiros, não consulta dados de mercado e não substitui avaliação profissional."
)

# Cria uma caixa informativa.
st.info(
    "Nesta primeira versão, o objetivo é apenas validar a abertura da aplicação "
    "em Streamlit. As perguntas e regras da árvore de decisão serão adicionadas "
    "nas próximas etapas."
)

# Ele apenas ajuda a separar visualmente as partes da tela
st.divider()

# O st.subheader() cria um título menor que o título principal.
st.subheader("Início da simulação")

st.write(
    "Quando o protótipo estiver completo, este botão dará início ao questionário "
    "de classificação do perfil do investidor."
)

# O st.button() cria um botão clicável.
# O st.success() mostra uma mensagem de sucesso em verde.
if st.button("Iniciar questionário"):
    st.success("O botão está funcionando. O questionário será implementado nas próximas etapas.")