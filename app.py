import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="App Financeiro", page_icon="💰", layout="centered")

st.title("💰 App Financeiro Pessoal")
st.markdown("Controle simples de receitas e despesas")

# Inicializar dados na sessão
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor"])

# Formulário
with st.form("form_lancamento"):
    data = st.date_input("Data", datetime.today())
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    categoria = st.text_input("Categoria")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        novo = pd.DataFrame(
            [[data, tipo, categoria, valor]],
            columns=["Data", "Tipo", "Categoria", "Valor"]
        )
        st.session_state.dados = pd.concat(
            [st.session_state.dados, novo],
            ignore_index=True
        )
        st.success("Lançamento adicionado com sucesso!")

st.divider()

# Mostrar tabela
st.subheader("📋 Lançamentos")
st.dataframe(st.session_state.dados, use_container_width=True)

# Resumo financeiro
if not st.session_state.dados.empty:
    total_receitas = st.session_state.dados[
        st.session_state.dados["Tipo"] == "Receita"
    ]["Valor"].sum()

    total_despesas = st.session_state.dados[
        st.session_state.dados["Tipo"] == "Despesa"
    ]["Valor"].sum()

    saldo = total_receitas - total_despesas

    st.divider()
    st.subheader("📊 Resumo")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
    col2.metric("Total Despesas", f"R$ {total_despesas:,.2f}")
    col3.metric("Saldo", f"R$ {saldo:,.2f}")

    grafico = st.session_state.dados.groupby("Categoria")["Valor"].sum()
    st.bar_chart(grafico)
