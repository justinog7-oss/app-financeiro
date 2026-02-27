import streamlit as st
from supabase import create_client

# --- Conexão com Supabase ---
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]  # via Streamlit Secrets
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("App Financeiro - Teste de Inserção")

# --- Inputs do usuário ---
descricao = st.text_input("Descrição do gasto")
valor = st.text_input("Valor (ex: 12.50)")

if st.button("Adicionar gasto"):
    try:
        # Tenta converter valor para float
        valor_float = float(valor)
        
        # Inserção no Supabase
        res = supabase.table("despesas").insert({
            "descricao": descricao,
            "valor": valor_float
        }).execute()
        
        if res.error:
            st.error(f"Erro ao inserir: {res.error.message}")
        else:
            st.success(f"Gasto inserido com sucesso: {res.data}")
    
    except ValueError:
        st.error("O valor precisa ser um número (ex: 12.50)")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# --- Mostra todos os gastos atuais ---
st.subheader("Gastos atuais")
try:
    dados = supabase.table("despesas").select("*").execute()
    if dados.data:
        st.table(dados.data)
    else:
        st.info("Nenhum gasto cadastrado ainda.")
except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")
