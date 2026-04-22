import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Bandejas Cirúrgicas", layout="wide")

# --- SIMULAÇÃO DE BANCO DE DADOS (Persistente na sessão) ---
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
# PÁGINA 1: CONFERÊNCIA E RASTREIO
# ---------------------------------------------------------
if pagina == "🔍 Conferência e Rastreio":
    st.header("🔍 Conferência de Saída/Entrada")
    
    id_scan = st.text_input("Escaneie o Código de Barras (ou digite o ID):").upper()

    if id_scan in st.session_state.db_bandejas:
        bandeja = st.session_state.db_bandejas[id_scan]
        st.subheader(f"Bandeja: {bandeja['nome']}")
        
        col_local, col_data = st.columns(2)
        with col_local:
            novo_local = st.selectbox("Atualizar Localização:", ["Almoxarifado", "Esterilização (CME)", "Expurgo", "Sala 01", "Sala 02", "Sala 03"], index=0)
        
        st.divider()
        st.write("### Checklist de Itens")
        
        # Gerar checklist dinâmico
        form_faltas = {}
        for item, qtd_esperada in bandeja['itens'].items():
            c1, c2, c3 = st.columns([2, 1, 3])
            with c1:
                st.write(f"**{item}**")
            with c2:
                qtd_real = st.number_input(f"Qtd presente", min_value=0, max_value=qtd_esperada, value=qtd_esperada, key=f"check_{id_scan}_{item}")
            with c3:
                obs = ""
                if qtd_real < qtd_esperada:
                    obs = st.text_input("Observação (Obrigatório)", placeholder="Ex: Em manutenção", key=f"obs_{id_scan}_{item}")
                    form_faltas[item] = {"falta": qtd_esperada - qtd_real, "obs": obs}

        if st.button("Finalizar e Salvar"):
            # Atualiza o local no "banco"
            st.session_state.db_bandejas[id_scan]['local'] = novo_local
            
            # Registra observações no histórico
            for item, info in form_faltas.items():
                st.session_state.historico_obs.append({
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Bandeja": bandeja['nome'],
                    "Item": item,
                    "Qtd Faltante": info['falta'],
                    "Observação": info['obs'],
                    "Local": novo_local
                })
            st.success(f"Conferência salva! Localização atualizada para: {novo_local}")

# ---------------------------------------------------------
# PÁGINA 2: GERENCIAR/EDITAR BANDEJAS
# ---------------------------------------------------------
elif pagina == "⚙️ Gerenciar/Editar Bandejas":
    st.header("⚙️ Configuração das Bandejas")
    
    escolha = st.selectbox("Selecione uma bandeja para editar ou visualizar:", list(st.session_state.db_bandejas.keys()))
    
    if escolha:
        dados = st.session_state.db_bandejas[escolha]
        
        with st.expander(f"Editar Detalhes de {escolha}", expanded=True):
            novo_nome = st.text_input("Nome da Bandeja:", value=dados['nome'])
            
            st.write("**Itens da Bandeja (Nome do Item : Quantidade Total)**")
            # Aqui transformamos o dicionário em texto para facilitar a edição rápida
            itens_texto = ""
            for i, q in dados['itens'].items():
                itens_texto += f"{i}:{q}\n"
            
            novo_itens_raw = st.text_area("Edite os itens (Formato: Nome:Quantidade - um por linha)", value=itens_texto)
            
            if st.button("Salvar Alterações"):
                # Converter o texto de volta para dicionário
                novos_itens_dict = {}
                try:
                    for linha in novo_itens_raw.strip().split('\n'):
                        nome_item, qtd_item = linha.split(':')
                        novos_itens_dict[nome_item.strip()] = int(qtd_item.strip())
                    
                    st.session_state.db_bandejas[escolha]['nome'] = novo_nome
                    st.session_state.db_bandejas[escolha]['itens'] = novos_itens_dict
                    st.success("Bandeja atualizada com sucesso!")
                    st.rerun()
                except:
                    st.error("Erro no formato! Use 'Nome:Quantidade' (Ex: Pinça:5)")

# ---------------------------------------------------------
# PÁGINA 3: RELATÓRIO DE OBSERVAÇÕES
# ---------------------------------------------------------
elif pagina == "📊 Relatório de Observações":
    st.header("📊 Histórico de Materiais Faltantes")
    
    if len(st.session_state.historico_obs) > 0:
        df = pd.DataFrame(st.session_state.historico_obs)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar Relatório em Excel (CSV)", csv, "relatorio_faltas.csv", "text/csv")
    else:
        st.info("Nenhuma observação registrada até o momento.")
