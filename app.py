import streamlit as st
from supabase import create_client

# --- Conexão com Supabase ---
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("App Financeiro - Teste de Inserção")

# --- Inputs do usuário ---
descricao = st.text_input("Descrição do gasto")
valor = st.text_input("Valor (ex: 12.50)")

if st.button("Adicionar gasto"):
    try:
        valor_float = float(valor)

        res = supabase.table("despesas").insert({
            "descricao": descricao,
            "valor": valor_float
        }).execute()

        # ✅ Se chegou aqui, deu certo
        st.success("Gasto inserido com sucesso!")
        st.write("Dados inseridos:", res.data)

    except ValueError:
        st.error("O valor precisa ser um número (ex: 12.50)")
    except Exception as e:
        st.error(f"Erro ao inserir no banco: {e}")

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
