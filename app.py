import streamlit as st
import random
import requests

# Função para buscar o resultado mais recente via API
def buscar_ultimo_resultado():
    try:
        # API pública que retorna dados das loterias CEF
        url = "https://loteriacaixa.api.ghmattiollo.com/api/v1/lotofacil/latest"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            # Retorna a lista de dezenas e o número do concurso
            return dados['dezenas'], dados['concurso']
    except:
        return None, None

# Lógica de geração (mantida a sua regra original)
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

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LotoFacil Pro IA", page_icon="🍀", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 LotoFácil Inteligente")
st.subheader("Automação Pro: Resultados em tempo real")

# --- BUSCA AUTOMÁTICA ---
dezenas_api, concurso_api = buscar_ultimo_resultado()

if dezenas_api:
    st.success(f"✅ Concurso {concurso_api} carregado automaticamente!")
    # Mostra os números que a IA vai usar como base
    st.write(f"**Base de análise (último sorteio):** {', '.join(dezenas_api)}")
    base_calculo = dezenas_api
else:
    st.warning("⚠️ Não conseguimos conectar à API. Digite manualmente abaixo:")
    entrada_manual = st.text_input("Dezenas do último sorteio:", placeholder="01 02 03...")
    base_calculo = entrada_manual.split() if entrada_manual else None

# --- BOTÃO DE AÇÃO ---
if base_calculo and len(base_calculo) == 15:
    if st.button("GERAR APOSTA AGORA 🚀"):
        with st.spinner('Analisando probabilidades...'):
            aposta, impares, soma, coinc, qtd_rep = gerar_aposta(base_calculo)
            
            if aposta:
                st.divider()
                jogo_formatado = " - ".join([f"{d:02d}" for d in aposta])
                st.info(f"### Seu Jogo Sugerido:\n**{jogo_formatado}**")
                st.code(jogo_formatado, language=None)
                
                # Painel de métricas
                c1, c2, c3 = st.columns(3)
                c1.metric("Ímpares", f"{impares}", "Ideal")
                c2.metric("Soma", f"{soma}", "Dentro da média")
                c3.metric("Repetidas", f"{len(coinc)}", f"Alvo: {qtd_rep}")
            else:
                st.error("Fracasso na geração. Tente novamente.")
else:
    if not dezenas_api:
        st.info("Aguardando os 15 números para iniciar a análise...")

with st.expander("🧐 Critérios da IA"):
    st.write("Soma (181-211), Ímpares (7-9) e Repetição (8-10 do anterior).")

st.caption("Dados via API pública. Boa sorte!")
