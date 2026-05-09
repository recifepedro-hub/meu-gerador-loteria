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

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; background-color: #28a745; color: white; font-weight: bold; border: none; }
    .metric-container { text-align: center; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Loto Turbo")

dezenas_api, concurso_api = buscar_ultimo_resultado()
base_calculo = None

if dezenas_api:
    st.success(f"✅ Concurso {concurso_api} carregado!")
    base_calculo = dezenas_api
else:
    st.error("⚠️ Informe os dados manualmente:")
    entrada_manual = st.text_input("15 dezenas do último sorteio:", placeholder="Ex: 01 02 03...")
    if entrada_manual:
        lista_manual = entrada_manual.split()
        if len(lista_manual) == 15:
            base_calculo = lista_manual

if base_calculo:
    def exibir_jogo(dados_base):
        aposta, impares, soma, coinc, qtd_rep = gerar_aposta(dados_base)
        if aposta:
            st.divider()
            jogo_formatado = " - ".join([f"{d:02d}" for d in aposta])
            st.info(f"### Jogo Sugerido:\n**{jogo_formatado}**")
            st.code(jogo_formatado, language=None)
            
            # --- NOVA ESTRUTURA DE MÉTRICAS ALINHADAS ---
            st.write("#### Análise Técnica:")
            # Criamos 3 colunas para alinhar títulos e valores
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<p style='text-align: center; margin-bottom: -15px;'><b>Ímpares</b></p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{impares}</h3>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<p style='text-align: center; margin-bottom: -15px;'><b>Soma</b></p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{soma}</h3>", unsafe_allow_html=True)
                
            with col3:
                st.markdown("<p style='text-align: center; margin-bottom: -15px;'><b>Repetidas</b></p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{len(coinc)}</h3>", unsafe_allow_html=True)

    if 'primeira_vez' not in st.session_state:
        st.session_state.primeira_vez = True
        
    exibir_jogo(base_calculo)

    st.write("---")
    if st.button("GERAR NOVO PALPITE 🔄"):
        st.rerun()

with st.expander("🧐 Critérios da IA"):
    st.write("Repetição (8-10), Ímpares (7-9) e Soma (181-211).")
