import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Graph Maker - accueil",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"About": "**Repo Github** : https://github.com/ylebecque/graph_maker"},
)

with st.sidebar:
    st.image("graph-maker-logo.png")


st.title("Graph-Maker")
st.markdown(
    "**Grap-Maker** est une appli permettant de générer des graphiques Seaborn sans effort."
)
st.markdown(
    "Pour commencer, rendez-vous sur la page **Graph Maker** pour créer des graphiques."
)
st.markdown("Enregistrez-les en mémoire, un par un.")
st.markdown(
    "Ensuite, si nécessaire, rendez-vous sur la page **Multigraph** qui générera des graphiques subplots automatiquement."
)
