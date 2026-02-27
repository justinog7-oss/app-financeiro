import streamlit as st
from supabase import create_client

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(
    page_title="App Financeiro",
    page_icon="💰",
    layout="centered"
)

SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===============================
# TÍTULO
# ===============================
st.title("💰 App Financeiro")

st.markdown("---")

# ===============================
# ADICIONAR GASTO
# ===============================
st.subheader("Adicionar novo registro")

descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Adicionar gasto"):
    if descricao.strip() == "":
        st.warning("Digite uma descrição.")
    else:
        try:
            supabase.table("despesas").insert({
                "descricao": descricao,
                "valor": valor
            }).execute()

            st.success("Gasto inserido com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao inserir: {e}")

# ===============================
# LISTAR + EXCLUIR
# ===============================
st.markdown("---")
st.subheader("📊 Gastos cadastrados")

try:
    dados = supabase.table("despesas").select("*").order("id", desc=True).execute()

    if dados.data:

        for item in dados.data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])

            with col1:
                st.write(item["id"])

            with col2:
                st.write(item["descricao"])

            with col3:
                st.write(f"R$ {item['valor']}")

            with col4:
                if st.button("🗑️", key=f"delete_{item['id']}"):
                    try:
                        supabase.table("despesas").delete().eq("id", item["id"]).execute()
                        st.success("Registro excluído!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")

    else:
        st.info("Nenhum gasto cadastrado ainda.")

except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")
