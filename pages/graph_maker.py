import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Graph Maker - graphique",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"About": "**Repo Github** : https://github.com/ylebecque/graph_maker"},
)

# Définition des listes de sélection

# Liste des styles de graphiques
style_graphique = ["Relation", "Distribution", "Catégorie", "Statistiques"]

# Liste des types de graphique selon le style
type_graphique = list()
type_graphique.append(["scatterplot", "lineplot"])
type_graphique.append(["histplot", "kdeplot", "ecdfplot"])
type_graphique.append(["swarmplot", "countplot"])
type_graphique.append(["stripplot", "boxplot", "violinplot", "pointplot"])

for idx in range(len(type_graphique)):
    type_graphique[idx].sort()

# Dictionnaire reliant le type au style
dico_types = {
    style_graphique[idx]: type_graphique[idx] for idx in range(len(style_graphique))
}

# Fonction de génération du code seaborn


def generate_seaborn(type="scatterplot", **kwargs):
    # Nom de la fonction
    code = f"sns.{type}(data = df"
    # x, y
    if kwargs.get("x"):
        x = kwargs["x"]
    else:
        x = None
    if kwargs.get("y"):
        y = kwargs["y"]
    else:
        y = None

    if x:
        # code += f"x = df['{x}']"
        code += f", x = '{x}'"
    if y:
        # code += f", y = df['{y}']"
        code += f", y = '{y}'"

    # Arguments hue / palette
    hue = None
    palette = None
    if kwargs.get("hue"):
        hue = kwargs.pop("hue")
        print(hue)
        if hue == "None":
            hue = None
    if kwargs.get("palette"):
        palette = kwargs.pop("palette")

    # hue/palette

    if hue:
        # code += f", hue = df['{hue}'], palette = '{palette}'"
        code += f", hue = '{hue}', palette = '{palette}'"
    # Fermeture de la parenthèse
    code += ")"
    return code


# Barre latérale de définition du graphique

with st.sidebar:

    # Sélection de la DataFrame

    # Sélection du graphique
    with st.expander("Options dataframe", expanded=False):
        st.write("Selection du fichier :")
        file = st.file_uploader("Choose a file")
        if file is not None:
            df = pd.read_csv(file)
            # st.session_state.df = df
        else:
            if "df" not in st.session_state:
                df = pd.read_csv("df.csv")
                # st.session_state.df = df

    st.write("Sélection du graphique")
    style = st.selectbox("Style de graphique :", style_graphique)
    type = st.selectbox("Type de graphique :", dico_types[style])

    # Sélection des arguments
    st.write("Sélection des arguments :")
    args = list(df.columns)
    x = st.selectbox("x : ", args, 0)

    y = st.selectbox("y : ", args + [None], 1)

    hue = st.selectbox("hue : ", [None] + args)


# Partie centrale


# Insertions de trois colonnes pour les configurations avancées
#   gestion des étiquettes
#   gestion des couleurs
#   gestion des axes

with st.expander("Options graphiques", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("étiquettes")
        titre = st.text_input("Titre du graphique", None)
        nom_x = st.text_input("Etiquette de l'axe x :", x)
        nom_y = st.text_input("Etiquette de l'axe y :", y)

    with col2:
        st.write("couleurs")
        pal_qualitatives = [
            "deep",
            "muted",
            "pastel",
            "bright",
            "dark",
            "colorblind",
        ]
        pal_sequentielles = ["crest", "flare", "magma", "mako", "rocket", "viridis"]
        choixpal = st.selectbox("Palette  : ", pal_qualitatives + pal_sequentielles, 0)
        if choixpal not in pal_qualitatives:
            inv = st.toggle("inversé")
            if inv:
                choixpal += "_r"
        palette = sns.color_palette(choixpal)
        plt.figure(figsize=(6, 1))
        sns.palplot(palette)
        st.pyplot(plt)

        st.write("Taille du graphique")
        fig_size_x = st.number_input("largeur", value=8, min_value=3, max_value=15)
        fig_size_y = st.number_input("hauteur", value=5, min_value=3, max_value=15)

    with col3:
        st.write("axes")
        sizex = st.selectbox(
            "taille (x) : ",
            ["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"],
            3,
        )
        # x_is_cat = st.toggle("x var. catégorique")
        rotationx = st.slider("rotation (x): ", 0, 90, 0, 5)
        sns_ticklabelsx = {"size": sizex, "rotation": rotationx}

        sizey = st.selectbox(
            "taille (y) : ",
            ["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"],
            3,
        )
        # y_is_cat = st.toggle("y var. catégorique")
        rotationy = st.slider("rotation (y): ", 0, 90, 0, 5)
        sns_ticklabelsy = {"size": sizey, "rotation": rotationy}


# Partie principale

# Création du code

# graphique
if "sns_code" not in st.session_state:
    st.session_state["sns_code"] = ""

sns_code_in = f"fig, ax = plt.subplots(figsize=({fig_size_x}, {fig_size_y}))\n"
sns_code = generate_seaborn(type=type, data=df, x=x, y=y, hue=hue, palette=choixpal)

# Titre / Etiquettes

if titre:
    sns_code += f"\nax.set_title('{titre}')"
if nom_x:
    sns_code += f"\nax.set_xlabel('{nom_x}')"
if nom_y:
    sns_code += f"\nax.set_ylabel('{nom_y}')"

# Mise en forme des axes
if (sizex != "medium") or (sizey != "medium") or (rotationx != 0) or (rotationy != 0):

    sns_code += f"""\ntx=ax.get_xticks()
txlabels = ax.get_xticklabels()
ax.set_xticks(tx, txlabels, rotation={rotationx}, size='{sizex}')"""
    sns_code += f"""\nty=ax.get_yticks()
tylabels = ax.get_yticklabels()
ax.set_yticks(ty, tylabels, rotation={rotationy}, size='{sizey}')"""

sns_code_out = "\nplt.show()"

# Affichage du graphique

# Vérification de la faisabilité du graphique
try:
    code = sns_code_in + sns_code + sns_code_out
    cmd = compile(code, "file", "exec")
    exec(cmd)
    st.pyplot(fig)
except Exception as e:
    st.header("Impossible de créer ce visuel")
    st.error(f"Erreur : {e}")
    st.write(
        "Veuillez vérifier que les données x, y correspondent au type de graphique."
    )
    st.write("Certains graphiques nécessitent que y soit réglé sur None, notamment.")


# affichage du code final
# Ajout des libraires à importer ?
activate = st.toggle("Imports")
if activate:
    imports = f"import seaborn as sns\nimport matplotlib.pyplot as plt\n"
else:
    imports = ""

st.markdown("**Code généré :**")
st.code(imports + code)

st.divider()

# Mémorisation dU numéro de la dernière figure enregistrée
if "max_fig" not in st.session_state:
    max_fig = 0
else:
    max_fig = st.session_state.max_fig

if "memoire" not in st.session_state:
    memoire = dict()
    st.session_state["memoire"] = memoire
else:
    memoire = st.session_state["memoire"]

col1, col2 = st.columns([0.3, 0.7])
with col1:
    num_fig = st.number_input(
        "Num. graphique : ",
        value=min(8, max_fig + 1),
        min_value=1,
        max_value=min(8, max_fig + 1),
    )
    st.caption(f"{max_fig} figure(s) mémorisée(s)")
with col2:
    st.header("\n\n\n")
    if st.button("Enr. fig"):
        st.session_state[f"fig_{num_fig}"] = sns_code
        # Vérification du numéro de la "dernière" figure enregistrée
        if num_fig >= max_fig:
            max_fig = num_fig
            st.session_state["max_fig"] = max_fig
            memoire.update(
                {
                    num_fig: (
                        style,
                        type,
                        x,
                        y,
                        hue,
                        titre,
                        nom_x,
                        nom_y,
                        choixpal,
                        fig_size_x,
                        fig_size_y,
                        sizex,
                        rotationx,
                        sizey,
                        rotationy,
                        sns_code,
                    )
                }
            )
            st.session_state["memoire"] = memoire
