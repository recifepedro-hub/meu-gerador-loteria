import streamlit as st
import random
import requests

# --- BUSCA AUTOMÁTICA ---
def buscar_ultimo_resultado():
    urls = [
        "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest",
        "https://loteriacaixa.api.ghmattiollo.com/api/v1/lotofacil/latest"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                dados = response.json()
                dezenas = dados.get('dezenas') or dados.get('listaDezenas')
                concurso = dados.get('concurso') or dados.get('numero')
                if dezenas and len(dezenas) == 15:
                    return [int(d) for d in dezenas], concurso
        except:
            continue 
    return None, None

# --- LÓGICA DE GERAÇÃO ---
def gerar_aposta(resultado_anterior_lista):
    dezenas_anteriores = [int(d) for d in resultado_anterior_lista]
    qtd_repetidas = random.randint(8, 10)
    repetidas = random.sample(dezenas_anteriores, qtd_repetidas)
    todas_dezenas = set(range(1, 26))
    fora_do_anterior = list(todas_dezenas - set(dezenas_anteriores))
    
    for _ in range(10000):
        adicionais = random.sample(fora_do_anterior, 15 - qtd_repetidas)
        aposta = sorted(repetidas + adicionais)
        qtd_impares = sum(1 for d in aposta if d % 2 != 0)
        soma = sum(aposta)
        if 7 <= qtd_impares <= 9 and 181 <= soma <= 211:
            return aposta, qtd_impares, soma, set(aposta) & set(dezenas_anteriores), qtd_repetidas
    return None, None, None, None, None

# --- INTERFACE ---
st.set_page_config(page_title="Loto Turbo", page_icon="🍀")

# Estilo para esconder elementos e melhorar o botão
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; background-color: #28a745; color: white; font-weight: bold; border: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Loto Turbo")
st.subheader("Gerador Automático de Apostas")

# 1. Tenta carregar dados da API
dezenas_api, concurso_api = buscar_ultimo_resultado()

# 2. Lógica de exibição Condicional
base_calculo = None

if dezenas_api:
    # Se a API funcionar, mostra o sucesso e define a base
    st.success(f"✅ Concurso {concurso_api} carregado via API")
    base_calculo = dezenas_api
    # O campo de texto NÃO é criado aqui, por isso ele some da tela.
else:
    # Se a API falhar, aí sim o campo manual aparece
    st.error("⚠️ Conexão com a Caixa indisponível.")
    entrada_manual = st.text_input("Insira as 15 dezenas do último sorteio para análise:", placeholder="Ex: 01 02 03...")
    if entrada_manual:
        lista_manual = entrada_manual.split()
        if len(lista_manual) == 15:
            base_calculo = lista_manual
        else:
            st.warning("Aguardando 15 dezenas...")

# 3. Botão de ação (só aparece se houver base de cálculo)
if base_calculo:
    st.divider()
    if st.button("GERAR JOGO AGORA 🚀"):
        with st.spinner('Processando estatísticas...'):
            aposta, impares, soma, coinc, qtd_rep = gerar_aposta(base_calculo)
            if aposta:
                st.balloons()
                jogo_formatado = " - ".join([f"{d:02d}" for d in aposta])
                st.info(f"### Sugestão Loto Turbo:\n**{jogo_formatado}**")
                st.code(jogo_formatado, language=None)
                
                # Métricas em colunas
                col1, col2, col3 = st.columns(3)
                col1.metric("Ímpares", f"{impares}")
                col2.metric("Soma", f"{soma}")
                col3.metric("Repetidas", f"{len(coinc)}")

with st.expander("🧐 Como funciona a análise?"):
    st.write("Filtros: Repetição (8-10), Ímpares (7-9) e Soma (181-211).")
