import streamlit as st
import random

# Mantemos sua lógica original intacta
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

# Interface Web com Streamlit
st.set_page_config(page_title="Gerador Pro - Lotofácil", page_icon="🍀")
st.title("🍀 Gerador de Apostas Inteligentes")

st.markdown("""
Esta ferramenta utiliza filtros de soma (181-211), ímpares (7-9) 
e repetição do sorteio anterior (8-10) para gerar seus jogos.
""")

# Entrada de dados melhorada para celular
entrada = st.text_input("Digite as 15 dezenas do último sorteio (espaçadas):", 
                         placeholder="Ex: 01 02 03 05...")

if entrada:
    try:
        lista_anterior = list(map(int, entrada.split()))
        if len(lista_anterior) != 15:
            st.warning("Por favor, insira exatamente 15 dezenas.")
        else:
            if st.button("Gerar Nova Aposta"):
                aposta, impares, soma, coinc, qtd_rep = gerar_aposta(lista_anterior)
                
                if aposta:
                    st.success(f"**Aposta Gerada:** \n\n {str(aposta)[1:-1]}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Ímpares", impares)
                    col2.metric("Soma", soma)
                    col3.metric("Repetidas", len(coinc))
                    
                    st.info(f"**Dezenas que repetiram:** {sorted(list(coinc))}")
                else:
                    st.error("Não foi possível gerar uma aposta nos critérios após 10.000 tentativas.")
    except ValueError:
        st.error("Entrada inválida. Use apenas números separados por espaço.")

st.caption("Desenvolvido para análise estatística de jogos.")