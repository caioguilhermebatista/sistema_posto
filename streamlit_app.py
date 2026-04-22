import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Gestão de Bandejas", layout="wide")

# Inicialização do Banco de Dados na Sessão
if 'db_bandejas' not in st.session_state:
    st.session_state.db_bandejas = {
        "BND-001": {"nome": "Pequena Cirurgia", "itens": {"Bisturi nº4": 2, "Pinça Kelly": 5}, "local": "Expurgo"},
        "BND-002": {"nome": "Sutura Adulto", "itens": {"Porta-agulha": 1, "Pinça com dente": 2}, "local": "Esterilização"},
    }

if 'historico_obs' not in st.session_state:
    st.session_state.historico_obs = []

# --- MENU LATERAL ---
st.sidebar.title("Menu Principal")
pagina = st.sidebar.radio("Ir para:", ["🔍 Conferência e Rastreio", "⚙️ Gerenciar/Editar Bandejas", "📊 Relatório de Observações"])

# ---------------------------------------------------------
# PÁGINA 1: CONFERÊNCIA (Mantida com melhorias)
# ---------------------------------------------------------
if pagina == "🔍 Conferência e Rastreio":
    st.header("🔍 Conferência de Fluxo")
    id_scan = st.text_input("Escaneie o Código de Barras:").upper()

    if id_scan in st.session_state.db_bandejas:
        bandeja = st.session_state.db_bandejas[id_scan]
        st.subheader(f"Bandeja: {bandeja['nome']}")
        
        novo_local = st.selectbox("Localização:", ["Almoxarifado", "CME", "Expurgo", "Sala 01", "Sala 02"], key="loc_conf")
        
        st.write("### Itens")
        for item, qtd_esp in bandeja['itens'].items():
            col1, col2, col3 = st.columns([2, 1, 3])
            with col1: st.write(f"**{item}** ({qtd_esp})")
            with col2: q_real = st.number_input(f"Qtd", 0, qtd_esp, qtd_esp, key=f"q_{id_scan}_{item}")
            with col3: 
                if q_real < qtd_esp:
                    motivo = st.text_input("Motivo da falta", key=f"obs_{id_scan}_{item}")
                    if st.button(f"Registrar Falta de {item}"):
                        st.session_state.historico_obs.append({
                            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Bandeja": bandeja['nome'], "Item": item, "Tipo": "FALTA NO FLUXO", "Obs": motivo
                        })
                        st.toast(f"Falta de {item} registrada!")

# ---------------------------------------------------------
# PÁGINA 2: GERENCIAR/EDITAR (NOVA LÓGICA DE CHECKLIST)
# ---------------------------------------------------------
elif pagina == "⚙️ Gerenciar/Editar Bandejas":
    st.header("⚙️ Configuração e Manutenção de Bandejas")
    
    id_sel = st.selectbox("Selecione a Bandeja:", list(st.session_state.db_bandejas.keys()))
    bandeja = st.session_state.db_bandejas[id_sel]

    col_edit, col_obs = st.columns([2, 1])

    with col_edit:
        st.subheader("📝 Editar Itens da Checklist")
        # Mostrar itens atuais com opção de excluir
        itens_para_remover = []
        for item, qtd in bandeja['itens'].items():
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"🔹 {item}")
            c2.write(f"Qtd: {qtd}")
            if c3.button("❌", key=f"del_{id_sel}_{item}"):
                itens_para_remover.append(item)
        
        # Processar remoções
        for item in itens_para_remover:
            del st.session_state.db_bandejas[id_sel]['itens'][item]
            st.rerun()

        st.divider()
        st.write("**Adicionar Novo Item**")
        c_nome, c_qtd, c_add = st.columns([3, 1, 1])
        novo_item_nome = c_nome.text_input("Nome do Utensílio", key="n_item")
        novo_item_qtd = c_qtd.number_input("Qtd", 1, 50, 1, key="n_qtd")
        if c_add.button("Adicionar"):
            if novo_item_nome:
                st.session_state.db_bandejas[id_sel]['itens'][novo_item_nome] = novo_item_qtd
                st.rerun()

    with col_obs:
        st.subheader("📌 Observação Direta")
        st.info("Use este campo para notas permanentes ou avisos de manutenção.")
        nota_direta = st.text_area("Escreva a observação:")
        if st.button("Salvar Nota no Relatório"):
            if nota_direta:
                st.session_state.historico_obs.append({
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Bandeja": bandeja['nome'],
                    "Item": "GERAL / MANUTENÇÃO",
                    "Tipo": "NOTA DE ADMINISTRAÇÃO",
                    "Obs": nota_direta
                })
                st.success("Nota enviada para a página de observações!")

# ---------------------------------------------------------
# PÁGINA 3: RELATÓRIO
# ---------------------------------------------------------
elif pagina == "📊 Relatório de Observações":
    st.header("📊 Histórico de Ocorrências e Notas")
    if st.session_state.historico_obs:
        df = pd.DataFrame(st.session_state.historico_obs)
        st.table(df) # Mostra uma tabela limpa
    else:
        st.info("Nenhum registro encontrado.")
