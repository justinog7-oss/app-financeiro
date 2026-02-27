import streamlit as st
from supabase import create_client

st.set_page_config(page_title="App Financeiro", page_icon="💰")

# --- Conexão com Supabase ---
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💰 App Financeiro")

# --- Inputs ---
descricao = st.text_input("Descrição do gasto")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Adicionar gasto"):
    try:
        res = supabase.table("despesas").insert({
            "descricao": descricao,
            "valor": valor
        }).execute()

        st.success("Gasto inserido com sucesso!")
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")

# --- Mostrar gastos ---
st.subheader("📊 Gastos atuais")

try:
    dados = supabase.table("despesas").select("*").execute()

    if dados.data:
        st.table(dados.data)
    else:
        st.info("Nenhum gasto cadastrado ainda.")

except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")
