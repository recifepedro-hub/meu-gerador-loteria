import streamlit as st
import random

# Lógica de geração (mantida a sua regra original)
def gerar_aposta(resultado_anterior_lista):
    dezenas_anteriores = resultado_anterior_lista
    if len(dezenas_anteriores) != 15:
        return None, None, None, None, None
    
    qtd_repetidas = random.randint(8, 10)
    repetidas = random.sample(dezenas_anteriores, qtd_repetidas)
    todas_dezenas = set(range(1, 26))
    fora_do_anterior = list(todas_dezenas - set(dezenas_anteriores))
    
    for _ in range(10000):
        adicionais = random.sample(fora_do_anterior, 15 - qtd_repetidas)
        aposta = sorted(repetidas + adicionais)
        qtd_impares = sum(1 for d in aposta if d % 2 != 0)
        soma = sum(aposta)
        coincidencias = set(aposta) & set(dezenas_anteriores)
        
        if 7 <= qtd_impares <= 9 and 181 <= soma <= 211:
            return aposta, qtd_impares, soma, coincidencias, qtd_repetidas
    return None, None, None, None, None

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LotoFacil Pro IA", page_icon="🍀", layout="centered")

# Estilo para remover o menu do Streamlit e focar no app
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 LotoFácil Inteligente")
st.subheader("Gere jogos baseados em tendências estatísticas")

# --- EXPLICAÇÃO ESCONDIDA (O "MOTOR") ---
with st.expander("🧐 Como funciona a análise?"):
    st.write("""
    Este algoritmo não gera números aleatórios comuns. Ele filtra:
    - **Soma das Dezenas:** Mantém entre 181 e 211 (Média histórica).
    - **Equilíbrio Ímpar/Par:** Busca o padrão de 7 a 9 ímpares.
    - **Fator Repetição:** Seleciona entre 8 e 10 números do sorteio anterior.
    """)

# --- ENTRADA DE DADOS ---
entrada = st.text_input("Insira as 15 dezenas do último sorteio:", 
                         placeholder="Ex: 01 02 03 05 06 08...")

if entrada:
    try:
        lista_anterior = list(map(int, entrada.split()))
        if len(lista_anterior) != 15:
            st.warning("⚠️ Precisamos de exatamente 15 números para analisar.")
        else:
            if st.button("GERAR APOSTA 🚀"):
                aposta, impares, soma, coinc, qtd_rep = gerar_aposta(lista_anterior)
                
                if aposta:
                    st.divider()
                    st.success("### ✅ Aposta Gerada!")
                    
                    # Formatação visual do jogo
                    jogo_formatado = " - ".join([f"{d:02d}" for d in aposta])
                    st.info(f"**{jogo_formatado}**")
                    st.caption("Toque no botão abaixo para copiar o jogo:")
                    st.code(jogo_formatado, language=None)
                    
                    # Painel de métricas (Cards)
                    st.write("---")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Ímpares", f"{impares}", "Ideal")
                    c2.metric("Soma", f"{soma}", "Dentro da média")
                    c3.metric("Repetidas", f"{len(coinc)}", f"Alvo: {qtd_rep}")
                    
                    st.write("---")
                    st.info(f"**Dezenas repetidas do último concurso:** \n\n {sorted(list(coinc))}")
                else:
                    st.error("❌ Não encontramos uma combinação ideal nos critérios agora. Tente gerar novamente.")
    except ValueError:
        st.error("⚠️ Use apenas números separados por espaço.")

st.divider()
st.caption("Desenvolvido com IA para análise de probabilidades. Boa sorte!")
