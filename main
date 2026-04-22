import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL (SIMULANDO BANCO DE DADOS) ---
if 'db_bandejas' not in st.session_state:
    st.session_state.db_bandejas = {
        "BND-001": {"nome": "Pequena Cirurgia", "itens": {"Bisturi nº4": 2, "Pinça Kelly": 5, "Tesoura": 1}, "local": "Expurgo"},
        "BND-002": {"nome": "Sutura Adulto", "itens": {"Porta-agulha": 1, "Pinça com dente": 2}, "local": "Esterilização"},
    }

st.title("🏥 Sistema de Rastreio de Bandejas - Posto de Saúde")

# --- CAMINHO 1: RASTREIO E CÓDIGO DE BARRAS ---
st.header("🔍 Localizar Bandeja")
id_scan = st.text_input("Escaneie o Código de Barras (ou digite o ID):")

if id_scan in st.session_state.db_bandejas:
    bandeja = st.session_state.db_bandejas[id_scan]
    st.success(f"Bandeja Identificada: **{bandeja['nome']}**")
    st.info(f"📍 Localização Atual: **{bandeja['local']}**")

    # --- CAMINHO 2: CHECKLIST DINÂMICO ---
    st.subheader("📋 Conferência de Materiais")
    itens = bandeja['itens']
    faltantes = {}

    for item, qtd_total in itens.items():
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.write(f"**{item}** (Esperado: {qtd_total})")
        with col2:
            qtd_presente = st.number_input(f"Qtd em {item}", min_value=0, max_value=qtd_total, value=qtd_total, key=f"qtd_{item}")
        with col3:
            obs = ""
            if qtd_presente < qtd_total:
                obs = st.text_input(f"Motivo da falta ({item})", key=f"obs_{item}")
                faltantes[item] = {"faltando": qtd_total - qtd_presente, "obs": obs}

    if st.button("Salvar Conferência e Atualizar Local"):
        # Aqui você salvaria no banco de dados real
        st.warning("Relatório de Faltas Gerado:")
        for item, dados in faltantes.items():
            st.write(f"❌ {item}: Faltam {dados['faltando']} unidades. Motivo: {dados['obs']}")
        st.success("Histórico atualizado com sucesso!")
else:
    if id_scan:
        st.error("Bandeja não encontrada no sistema.")

# --- GERADOR DE CÓDIGO DE BARRAS (ADMIN) ---
with st.sidebar:
    st.header("⚙️ Admin")
    if st.button("Gerar Novos Códigos de Barras"):
        st.write("Gerando arquivos .png para impressão...")
        # Lógica de salvar imagem do barcode entraria aqui
