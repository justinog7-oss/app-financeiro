import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(page_title="App Financeiro Pro", page_icon="💰", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= LOGIN SIMPLES =================
st.sidebar.title("🔐 Login")

user_id = st.sidebar.text_input("Digite seu usuário")

if not user_id:
    st.warning("Digite um usuário para continuar.")
    st.stop()

st.title("💰 App Financeiro Pro")

# ================= INSERIR REGISTRO =================
st.subheader("Adicionar Registro")

col1, col2, col3 = st.columns(3)

with col1:
    descricao = st.text_input("Descrição")

with col2:
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")

with col3:
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])

if st.button("Salvar"):
    if descricao:
        try:
            supabase.table("despesas").insert({
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo,
                "user_id": user_id
            }).execute()

            st.success("Salvo com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Digite uma descrição.")

# ================= BUSCAR DADOS =================
st.markdown("---")
st.subheader("📊 Seus Registros")

try:
    dados = supabase.table("despesas")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .execute()

    if dados.data:

        df = pd.DataFrame(dados.data)
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["mes"] = df["created_at"].dt.strftime("%Y-%m")

        # FILTRO POR MÊS
        mes_selecionado = st.selectbox("Filtrar por mês", sorted(df["mes"].unique(), reverse=True))
        df = df[df["mes"] == mes_selecionado]

        receita_total = df[df["tipo"] == "Receita"]["valor"].sum()
        despesa_total = df[df["tipo"] == "Despesa"]["valor"].sum()
        saldo = receita_total - despesa_total

        col1, col2, col3 = st.columns(3)
        col1.metric("Receitas", f"R$ {receita_total:,.2f}")
        col2.metric("Despesas", f"R$ {despesa_total:,.2f}")
        col3.metric("Saldo", f"R$ {saldo:,.2f}")

        st.markdown("### 📋 Lista")

        for _, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1,3,2,2,1])

            col1.write(row["id"])
            col2.write(row["descricao"])
            col3.write(row["tipo"])
            col4.write(f"R$ {row['valor']:,.2f}")

            # EDITAR
            if col5.button("✏️", key=f"edit_{row['id']}"):
                st.session_state["edit_id"] = row["id"]

            # EXCLUIR
            if col5.button("🗑️", key=f"del_{row['id']}"):
                supabase.table("despesas").delete().eq("id", row["id"]).execute()
                st.rerun()

        # GRÁFICO
        st.markdown("### 📈 Gráfico Mensal")
        grafico = df.groupby("tipo")["valor"].sum()
        st.bar_chart(grafico)

    else:
        st.info("Nenhum registro encontrado.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
