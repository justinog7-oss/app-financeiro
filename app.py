import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# 🔑 COLE AQUI SUAS INFORMAÇÕES DO SUPABASE
SUPABASE_URL = "COLE_SUA_URL_AQUI"
SUPABASE_KEY = "COLE_SUA_ANON_PUBLIC_KEY_AQUI"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="App Financeiro", page_icon="💰", layout="centered")

st.title("💰 App Financeiro com Banco de Dados")

# FORMULÁRIO
with st.form("form_lancamento"):
    data = st.date_input("Data", datetime.today())
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    categoria = st.text_input("Categoria")
    valor = st.number_input("Valor", min_value=0.0)
    submitted = st.form_submit_button("Salvar")

    if submitted:
        supabase.table("lancamentos").insert({
            "data": str(data),
            "tipo": tipo,
            "categoria": categoria,
            "valor": valor
        }).execute()
        st.success("Salvo no banco com sucesso!")

st.divider()

# BUSCAR DADOS DO BANCO
resposta = supabase.table("lancamentos").select("*").execute()
dados = pd.DataFrame(resposta.data)

if not dados.empty:
    st.subheader("📋 Lançamentos")
    st.dataframe(dados, use_container_width=True)

    total_receitas = dados[dados["tipo"] == "Receita"]["valor"].sum()
    total_despesas = dados[dados["tipo"] == "Despesa"]["valor"].sum()
    saldo = total_receitas - total_despesas

    st.subheader("📊 Resumo")
    st.metric("Saldo", f"R$ {saldo:,.2f}")
else:
    st.info("Nenhum lançamento ainda.")
