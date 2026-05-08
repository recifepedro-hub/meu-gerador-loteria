import streamlit as st
import random
import requests

# --- FUNÇÃO DE BUSCA AUTOMÁTICA (TURBINADA) ---
def buscar_ultimo_resultado():
    # Lista de APIs para redundância
    urls = [
        "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest",
        "https://loteriacaixa.api.ghmattiollo.com/api/v1/lotofacil/latest"
    ]
    
    for url in urls:
        try:
            # Timeout aumentado para 20 segundos para evitar falhas de conexão lenta
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                dados = response.json()
                # Mapeamento flexível para diferentes formatos de API
                dezenas = dados.get('dezenas') or dados.get('listaDezenas')
                concurso = dados.get('concurso') or dados.get('numero')
                
                if dezenas and len(dezenas) == 15:
                    return [int(d) for d in dezenas], concurso
        except:
            continue 
    return None, None

# --- LÓGICA DE GERAÇÃO ESTATÍSTICA ---
def gerar_aposta(resultado_anterior_lista):
    dezenas_anteriores = [int(d) for d in resultado_anterior_lista]
    
    # Define aleatoriamente se vai repetir 8, 9 ou 10 números (padrão da Lotofácil)
    qtd_repetidas = random.randint(8, 10)
    repetidas = random.sample(dezenas_anteriores, qtd_repetidas)
    
    todas_dezenas = set(range(1, 26))
    fora_do_anterior = list(todas_dezenas - set(dezenas_anteriores))
    
    # Tenta encontrar uma combinação que respeite os filtros
    for _ in range(10000):
        adicionais = random.sample(fora_do_anterior, 15 - qtd_repetidas)
        aposta = sorted(repetidas + adicionais)
        
        qtd_impares = sum(1 for d in aposta if d % 2 != 0)
        soma = sum(aposta)
        
        # Filtros: Ímpares (7 a 9) e Soma (181 a 211)
        if 7 <= qtd_impares <= 9 and 181 <= soma <= 211:
            return aposta, qtd_impares, soma, set(aposta) & set(dezenas_anteriores), qtd_repetidas
            
    return None, None, None, None, None

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="LotoFacil Pro IA", page_icon="🍀", layout="centered")

# Estilos customizados
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; background-color: #28a745; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #218838; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 LotoFácil Inteligente")
st.subheader("Análise Estatística com Busca Automática")

# Tentativa de carregar dados automaticamente
dezenas_api, concurso_api = buscar_ultimo_resultado()

base_calculo = None

if dezenas_api:
    st.success(f"✅ Dados do Concurso {concurso_api} obtidos com sucesso!")
    # Mostra as dezenas formatadas
    dezenas_formatadas = " - ".join([f"{d:02d}" for d in dezenas_api])
    st.write(f"**Último sorteio:** `{dezenas_formatadas}`")
    base_calculo = dezenas_api
else:
    st.error("⚠️ Não foi possível conectar às APIs de resultados.")
    entrada_manual = st.text_input("Insira manualmente as 15 dezenas do último sorteio (espaçadas):", 
                                   placeholder="01 02 03 04...")
    if entrada_manual:
        lista_manual = entrada_manual.split()
        if len(lista_manual) == 15:
            base_calculo = lista_manual
        else:
            st.warning("Por favor, insira exatamente 15 números.")

# --- BOTÃO PRINCIPAL ---
if base_calculo:
    st.write("---")
    if st.button("GERAR APOSTA OTIMIZADA 🚀"):
        with st.spinner('Calculando probabilidades...'):
            aposta, impares, soma, coinc, qtd_rep = gerar_aposta(base_calculo)
            
            if aposta:
                st.divider()
                st.balloons()
                
                jogo_formatado = " - ".join([f"{d:02d}" for d in aposta])
                st.info(f"### Jogo Sugerido:\n**{jogo_formatado}**")
                
                # Facilita copiar o jogo
                st.code(jogo_formatado, language=None)
                
                # Painel de Métricas
                st.write("#### Análise Técnica:")
                c1, c2, c3 = st.columns(3)
                c1.metric("Ímpares", f"{impares}", "Ideal")
                c2.metric("Soma", f"{soma}", "Na Média")
                c3.metric("Repetidas", f"{len(coinc)}", f"Alvo: {qtd_rep}")
                
                st.write("---")
                st.caption(f"Este jogo repetiu {len(coinc)} dezenas do concurso anterior conforme a tendência.")
            else:
                st.error("Não foi possível gerar um jogo dentro dos critérios agora. Tente novamente.")

# Rodapé informativo
with st.expander("🧐 Como a IA escolhe os números?"):
    st.write("""
    O algoritmo utiliza três filtros principais baseados no histórico da Lotofácil:
    1. **Frequência de Ímpares:** Mantém entre 7 e 9 números ímpares (ocorre em ~80% dos sorteios).
    2. **Soma das Dezenas:** Filtra resultados com soma total entre 181 e 211.
    3. **Tendência de Repetição:** Seleciona entre 8 e 10 dezenas que saíram no concurso anterior.
    """)

st.divider()
st.caption("Desenvolvido para análise de probabilidades. Use com responsabilidade.")
