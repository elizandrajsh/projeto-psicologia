import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Pesquisa de Percepção Social", layout="wide")

# Função para garantir que o Python ache a pasta 'fotos'
pasta_atual = os.path.dirname(__file__)

# Estilo Visual (CSS)
st.markdown("""
    <style>
    [data-testid="stImage"] img { border-radius: 15px; width: 100%; height: 230px; object-fit: cover; border: 3px solid #3498db; }
    .contexto-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 2px solid #dee2e6; }
    .stButton>button { font-weight: bold; border-radius: 10px; height: 3.5em; width: 100%; background-color: #f1f3f5; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS DE PERSONAGENS
personagens = {
    "Ana": {"raca": "Branca", "path": os.path.join(pasta_atual, "fotos", "ana.jpg")},
    "Tiago": {"raca": "Negra", "path": os.path.join(pasta_atual, "fotos", "tiago.jpg")},
    "Léo": {"raca": "Branca", "path": os.path.join(pasta_atual, "fotos", "leo.jpg")},
    "Bia": {"raca": "Negra", "path": os.path.join(pasta_atual, "fotos", "bia.jpg")}
}

# 3. INICIALIZAÇÃO
if 'respostas' not in st.session_state:
    st.session_state.respostas = []
if 'questao' not in st.session_state:
    st.session_state.questao = 0

# 4. LISTA DE 10 QUESTÕES
questoes = [
    {"pergunta": "📚 Quem tirou a nota mais alta na prova de hoje?", "tipo": "Positivo", "icon": "📝"},
    {"pergunta": "⚽ Quem chutou a bola que acabou quebrando o vidro?", "tipo": "Negativo", "icon": "💥"},
    {"pergunta": "🙋‍♀️ Quem a professora chamou para ser o ajudante do dia?", "tipo": "Positivo", "icon": "🤝"},
    {"pergunta": "📢 Quem estava fazendo muita bagunça na hora da fila?", "tipo": "Negativo", "icon": "📣"},
    {"pergunta": "🥇 Quem você escolheria para ser o capitão do time?", "tipo": "Positivo", "icon": "🏆"},
    {"pergunta": "🚫 Alguém contou uma mentira para o diretor. Quem foi?", "tipo": "Negativo", "icon": "🤥"},
    {"pergunta": "🥪 Quem sempre divide o lanche com os amigos?", "tipo": "Positivo", "icon": "🥪"},
    {"pergunta": "🎨 Quem fez o desenho mais bonito do concurso?", "tipo": "Positivo", "icon": "🎨"},
    {"pergunta": "🧩 Alguém deixou os brinquedos espalhados no chão. Quem foi?", "tipo": "Negativo", "icon": "🧸"},
    {"pergunta": "🗣️ Quem perdeu a paciência e gritou com o colega?", "tipo": "Negativo", "icon": "😤"}
]

# --- INTERFACE ---
if st.session_state.questao < len(questoes):
    q = questoes[st.session_state.questao]
    st.title("🔍 Investigação Escolar: Percepção e Sociedade")
    st.markdown(f'<div class="contexto-card"><h1>{q["icon"]}</h1><h3>{q["pergunta"]}</h3></div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (nome, info) in enumerate(personagens.items()):
        with cols[i]:
            if os.path.exists(info['path']):
                st.image(info['path'], caption=f"Estudante {nome}")
            else:
                st.warning(f"Foto de {nome} não encontrada.")
            
            if st.button(f"Foi o(a) {nome}", key=f"q{st.session_state.questao}_{nome}"):
                st.session_state.respostas.append({"Tipo": q["tipo"], "Raca": info["raca"]})
                st.session_state.questao += 1
                st.rerun()

# --- RESULTADOS ---
else:
    st.header("📊 Relatório de Percepção Social")
    df = pd.DataFrame(st.session_state.respostas)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🌟 Atributos Positivos")
        res_pos = df[df['Tipo'] == "Positivo"]['Raca'].value_counts()
        if not res_pos.empty: st.bar_chart(res_pos)
    with c2:
        st.subheader("⚠️ Atributos Negativos")
        res_neg = df[df['Tipo'] == "Negativo"]['Raca'].value_counts()
        if not res_neg.empty: st.bar_chart(res_neg)
    
    st.divider()
    st.subheader("🧐 Reflexão de Psicologia Social")
    st.markdown("Este experimento observa se o **Racismo Estrutural** influencia nossos 'atalhos mentais'.")
    if st.button("🔄 Reiniciar"):
        st.session_state.respostas = []
        st.session_state.questao = 0
        st.rerun()