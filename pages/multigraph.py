import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

# Configuration de la page
st.set_page_config(
    page_title="Graph Maker - subplots",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"About": "**Repo Github** : https://github.com/ylebecque/graph_maker"},
)


def calculate_rows_cols(nb_figs: int) -> dict:
    # Fonction calculant les lignes possibles en fn. du nb de figures
    # arg : nb_figs : int
    # return : dictionnaire {nb_lignes : nb_cols}
    dico_res = dict()
    for k in range(1, nb_figs + 1):
        if (nb_figs % k) > 0:
            total = nb_figs // k + 1
        else:
            total = nb_figs // k
        dico_res.update({k: total})
    return dico_res


def create_axes(row, col, fig):
    axes = []
    delta = (row * col) - fig + 1
    print(delta)
    # si autant de figures que d'axes
    if delta == 0:
        for f in range(1, fig + 1):
            axes.append(f"ax{f} = plt.subplot({row},{col},{f})")
    # si la figure restante tient sur une ligne
    elif delta <= col:
        for f in range(1, fig):
            axes.append(f"ax{f} = plt.subplot({row},{col},{f})")
        index = (fig, row * col)
        axes.append(f"ax{f} = plt.subplot({row},{col},{index})")
    # sinon elle tient sur une colonne
    else:
        list_index = [i for i in range(1, (row * col) + 1) if i % col != 0]
        print(list_index)
        for f in range(1, fig):
            axes.append(f"ax{f} = plt.subplot({row},{col},{list_index[f-1]})")
        index = (col, row * col)
        axes.append(f"ax{f} = plt.subplot({row},{col},{index})")
    return axes


def add_plot(code, fig):
    lines = code.split("\n")
    lines[0] = f"ax{fig} = " + lines[0]
    for i in range(1, len(lines)):
        lines[i] = re.sub("ax", f"ax{fig}", lines[i])
    return "\n".join(lines)


def create_subplots():
    pass


# Barre latérale

if "max_fig" not in st.session_state:
    max_fig = 1
else:
    max_fig = st.session_state["max_fig"]

with st.sidebar:
    nb_figs = st.number_input(
        "Nb figures : ", value=2, min_value=2, max_value=max(max_fig, 2)
    )
    dico_rc = calculate_rows_cols(nb_figs)
    nb_rows = st.number_input("Nb lignes : ", value=1, min_value=1, max_value=nb_figs)
    nb_cols = dico_rc[nb_rows]
    st.caption("Nb colonnes :")
    st.write(nb_cols)

    st.divider()
    st.write("Taille du graphique")
    fig_x = st.number_input("largeur", min_value=8, max_value=15)
    fig_y = st.number_input("hauteur", min_value=8, max_value=15)

# Partie centrale

# Initialisation de la figure princiaple
subplots_code = f"fig = plt.figure(figsize=({fig_x}, {fig_y}))\n"

# Initialisation de df
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = pd.read_csv("df.csv")

# Initialisation des axes sous-figures
list_figs = ["nope"]
for figs in range(1, 9):
    if f"fig_{figs}" in st.session_state:
        list_figs.append(st.session_state[f"fig_{figs}"])
    else:
        list_figs.append("")

axes = create_axes(nb_rows, nb_cols, nb_figs)

# Création des sous-figures
for figs in range(1, nb_figs + 1):
    subplots_code += "\n"
    subplots_code += axes[figs - 1] + "\n"
    subplots_code += add_plot(list_figs[figs], figs)


# Fin de la figure principale
subplots_code += "\nplt.tight_layout()\nplt.show()"

# Création si nombre de figures mémorisées >= 2

if max_fig > 1:
    # Affichage du graphique
    cmd = compile(subplots_code, "file", "exec")
    exec(cmd)
    st.pyplot(fig)

    # Affichage du code
    st.code(subplots_code)
else:
    st.error(
        """Vous devez créer au moins 2 figures avant de créer un subplots\n
Rendez-vous sur la page graph maker à cette fin"""
    )
