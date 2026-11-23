#RESUMO DO CHAMADO
# PARA RODAR CODIGO COLE ESSE COMANDO NO TERMINAL:  python -m streamlit run "c:/Users/Igor/OneDrive/Área de Trabalho/PYTHON/COD. RESUMO DE ATENDIMENTO/RESUMO DE ATENDIMENTO.py"
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="FORTH REFRIGERAÇÃO", layout="wide")

# --- CAMINHOS DOS ARQUIVOS ---
caminho = Path(__file__).parent / "resumo de atendimento.csv"
caminho_clientes = Path(__file__).parent / "clientes.csv"
caminho_equipamentos = Path(__file__).parent / "equipamentos.csv"

# --- DADOS INICIAIS ---
dados_iniciais = [
    {"CLIENTE": "SPK EDEN", "CONTATO": ""},
    {"CLIENTE": "SPK SÃO MATEUS", "CONTATO": ""},
    {"CLIENTE": "SPK GUADALUPE", "CONTATO": ""},
    {"CLIENTE": "MTK ANCHIETA", "CONTATO": ""},
    {"CLIENTE": "MTK HIGIENÓPLIS", "CONTATO": ""},
    {"CLIENTE": "FRIGANSO SJM", "CONTATO": ""},
    {"CLIENTE": "FRIGANSO PENHA", "CONTATO": ""},
    {"CLIENTE": "SABOR TRADICIONAL", "CONTATO": ""},
    {"CLIENTE": "RANCHO PORTUGUÊS", "CONTATO": ""},
    {"CLIENTE": "LAR FABIANO DE CRISTO", "CONTATO": ""},
]

lista_base_equipamentos = [
    "ADEGAS", 
    "AR CONDICIONADO SPLIT PAREDE (HI-WALL)", 
    "AR CONDICIONADO SPLIT PISO TETO (SPACE)", 
    "AR CONDICIONADO SPLIT CASSETE", 
    "AR CONDICIONADO SPLIT DUTADO", 
    "AR CONDICIONADO CENTRAL (SELF)", 
    "AR CONDICIONADO DE JANELA (ACJ)",
    "AR CONDICIONADO PORTÁTIL (PINGUINO)", 
    "BALCÃO DO AÇOUGUE", 
    "BALCÃO DE LATICÍNEOS", 
    "BALCÃO DE IOGURTE", 
    "BALCÃO DE BANDEJA AUTO ATENDIMENTO", 
    "BALCÃO DE FLV", 
    "BALCÃO ILHA DE CONGELADOS", 
    "BALCÃO ILHA PLUG-IN", 
    "BALCÃO PLUG-IN DE COZINHA", 
    "BEBEDOURO SIMPLES", 
    "BEBEDOURO COMERCIAL 20 LITROS", 
    "BEBEDOURO COMERCIAL 50 LITROS", 
    "CAMARA DE CONGELAMENTO TÚNEL", 
    "CAMARA DE CONGELADOS",
    "CAMARA DE RESFRIADOS",
    "CAMARA DE RESFRIADOS PRESUNTARIA", 
    "CAMARA DE RESFRIADOS CARNE", 
    "CAMARA DE LATICÍNEOS", 
    "CAMARA DE SALGADOS", 
    "CAMARA DE PEIXES FRESCOS", 
    "CAMARA DE PEIXES CONGELADOS", 
    "CAMARA DE CARCAÇA BOVINA",
    "CAMARA DO AÇOUGUE", 
    "CAMARA DE CARCAÇA SUINA", 
    "CAMARA DE IMPRÓPRIOS", 
    "CAMARA DE LIXO", 
    "CAMARA DE FLV", 
    "CAMARA DE GELO", 
    "CAMARA DA PADARIA",
    "CAMARA DE OSSO",
    "CORREDOR TENDAL",
    "EXPEDIÇÃO",
    "CONDENSADOR REMOTO", 
    "UNIDADE CONDENSADORA", 
    "CONTAINER-REFRIGERADO", 
    "CHOPEIRAS", 
    "GELADEIRA COMERCIAL DUAS/QUATRO PORTAS DE INOX", 
    "GELADEIRA CLIMÁTICA PARA PÃO", 
    "SALA DE PREPARO DE ALIMENTOS", 
    "SALA DE DESOSSA",
    "SALA DE PORCIONADOS CARNES", 
    "SALA DE PORCIONADOS FRANGO",
    "SALA DE EMBALAGEM DE CARNE SECA",
    "SALGA",
    "VITRINE EXPOSITORA DE CONGELADOS", 
    "VITRINE EXPOSITORA DE BEBIDAS", 
    "TORTEIRAS GIRATÓRIAS"
]
equipamentos_iniciais = [{"EQUIPAMENTO": item} for item in lista_base_equipamentos]

colunas = [
    "O.S. NUMERO",
    "CLIENTE",
    "CONTATO",
    "DATA DE ABERTURA",
    "DATA DE ATENDIMENTO",
    "HORA DE ENTRADA",
    "HORA DE SAÍDA",
    "EQUIPAMENTO",
    "PROBLEMA",
    "PARECER TECNICO",
    "PECAS USADAS",
    "PECAS NECESSARIAS",
    "EQUIPAMENTO FUNCIONANDO?",
    "TECNICO",
    "FOTOS"
]

if caminho.exists():
    resumo_de_atendimento = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
else:
    resumo_de_atendimento = pd.DataFrame(columns=colunas)

# --- INÍCIO DA BARRA LATERAL ---
st.sidebar.write("# FORTH REFRIGERAÇÃO")
st.sidebar.write("### RESUMO DE ATENDIMENTO")

# 1. CLIENTES
if caminho_clientes.exists():
    df_clientes = pd.read_csv(caminho_clientes, sep=";", encoding="utf-8-sig").fillna("")
else:
    df_clientes = pd.DataFrame(dados_iniciais)
    df_clientes.to_csv(caminho_clientes, index=False, sep=";", encoding="utf-8-sig")

lista_clientes = sorted(df_clientes["CLIENTE"].unique().tolist())
cliente = st.sidebar.selectbox("CLIENTE", [""] + lista_clientes)

contato_atual = ""
if cliente:
    filtro = df_clientes.loc[df_clientes["CLIENTE"] == cliente, "CONTATO"]
    if not filtro.empty:
        contato_atual = str(filtro.values[0])

contato = st.sidebar.text_input("CONTATO", value=contato_atual, placeholder="Nome / Telefone")
if cliente and contato != contato_atual:
    if st.sidebar.button("💾 Atualizar Contato deste Cliente"):
        df_clientes.loc[df_clientes["CLIENTE"] == cliente, "CONTATO"] = contato
        df_clientes.to_csv(caminho_clientes, index=False, sep=";", encoding="utf-8-sig")
        st.sidebar.success("Contato atualizado!")
        st.rerun()

with st.sidebar.expander("➕ Adicionar Novo Cliente / Contato"):
    novo_cliente = st.text_input("Nome do Novo Cliente").strip().upper()
    novo_contato = st.text_input("Contato do Novo Cliente").strip()
    if st.button("Salvar Novo Cadastro"):
        if novo_cliente and novo_cliente not in lista_clientes:
            nova_linha = pd.DataFrame([{"CLIENTE": novo_cliente, "CONTATO": novo_contato}])
            df_clientes = pd.concat([df_clientes, nova_linha], ignore_index=True)
            df_clientes.to_csv(caminho_clientes, index=False, sep=";", encoding="utf-8-sig")
            st.success(f"{novo_cliente} cadastrado!")
            st.rerun()
        elif novo_cliente in lista_clientes:
            st.warning("Cliente já existe. Selecione ele acima para alterar o contato.")

# 2. DADOS DA O.S. (NÚMERO, DATAS E HORAS)
numero = st.sidebar.number_input("NUMERO DA O.S.", step=1)
data_abertura = st.sidebar.date_input("DATA DE ABERTURA", format="DD/MM/YYYY")
data_atendimento = st.sidebar.date_input("DATA DE ATENDIMENTO", format="DD/MM/YYYY")
hora_entrada = st.sidebar.time_input("HORA DE ENTRADA", value="now")
hora_saida = st.sidebar.time_input("HORA DE SAÍDA", value=None)

# 3. EQUIPAMENTOS (AGORA NO LUGAR CERTO E SEM CAMPO DUPLICADO!)
if caminho_equipamentos.exists():
    df_equipamentos = pd.read_csv(caminho_equipamentos, sep=";", encoding="utf-8-sig").fillna("")
else:
    df_equipamentos = pd.DataFrame(equipamentos_iniciais)
    df_equipamentos.to_csv(caminho_equipamentos, index=False, sep=";", encoding="utf-8-sig")

lista_equipamentos = sorted(df_equipamentos["EQUIPAMENTO"].unique().tolist())
equipamento = st.sidebar.selectbox("EQUIPAMENTO", [""] + lista_equipamentos)

with st.sidebar.expander("➕ Adicionar Novo Equipamento"):
    novo_equipamento = st.text_input("Nome do Novo Equipamento").strip().upper()
    if st.button("Salvar Equipamento"):
        if novo_equipamento and novo_equipamento not in lista_equipamentos:
            nova_linha_eq = pd.DataFrame([{"EQUIPAMENTO": novo_equipamento}])
            df_equipamentos = pd.concat([df_equipamentos, nova_linha_eq], ignore_index=True)
            df_equipamentos.to_csv(caminho_equipamentos, index=False, sep=";", encoding="utf-8-sig")
            st.success(f"{novo_equipamento} cadastrado!")
            st.rerun()
        elif novo_equipamento in lista_equipamentos:
            st.warning("Esse equipamento já está na lista.")

# 4. RESTANTE DOS CAMPOS TÉCNICOS
problema = st.sidebar.text_area("PROBLEMA")
parecer_tecnico = st.sidebar.text_area("PARECER TÉCNICO")
pecas_usadas = st.sidebar.text_area("PEÇAS USADAS")
pecas_necessarias = st.sidebar.text_area("PEÇAS NECESSÁRIAS")
funcionando = st.sidebar.selectbox("EQUIPAMENTO FUNCIONANDO?", ["SIM", "NÃO", "PARCIALMENTE"])
tecnico = st.sidebar.selectbox("TÉCNICO", [
    "",
    "ALEXANDRE", 
    "CAROLINA", 
    "IGOR", 
    "MOISÉS", 
    "WALLACE"
    ])
fotos = st.sidebar.file_uploader("FOTOS DO ATENDIMENTO", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
