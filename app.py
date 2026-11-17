# 1. Les imports (on ajoute Streamlit avec le raccourci "st")
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. Configuration de la page (titre de l'onglet et utilisation de toute la largeur)
st.set_page_config(page_title="Dashboard Sport", layout="wide")

# 3. Affichage du titre principal sur la page web
st.title("Analyse des Licences Sportives en France")

# 4. Chargement des données 
st.write("Chargement des données en cours...")

# ---> À TOI DE JOUER : Écris la ligne pour charger ton CSV
df = pd.read_csv("donnees_sport.zip", sep=";", low_memory=False)

# 5. Affichage d'un message de succès sur le site web (shape = totalité des lignes et colonnes du tableau)
st.success(f"Données chargées avec succès ! Taille du tableau : {df.shape}")

# --- ÉTAPE 3 : La Barre latérale (Sidebar) ---
st.sidebar.header("Paramètres d'analyse")

# 1. Filtre de région dans la sidebar
liste_regions = df['Région'].dropna().unique()
# INDICE : Pour mettre un élément dans la barre latérale, on utilise st.sidebar au lieu de st
region_choisie = st.sidebar.selectbox("Sélectionnez une région :", liste_regions)
df_filtre = df[df['Région'] == region_choisie]

# 2. Filtre de sport dans la sidebar
liste_sports = df_filtre['Fédération'].dropna().unique()
sport_choisi = st.sidebar.selectbox("Choisissez un sport :", liste_sports)
df_sport = df_filtre[df_filtre['Fédération'] == sport_choisi]


# --- ÉTAPE 4 : Les Onglets (Tabs) ---
# INDICE : La fonction Streamlit pour créer des onglets s'appelle tabs()
onglet1, onglet2 = st.tabs(["Analyse Régionale", "Analyse Locale"])


# --- CONTENU DE L'ONGLET 1 (Région) ---
with onglet1:
    st.subheader(f"Aperçu de la région : {region_choisie}")
    
    # Les KPIs (Key Performance Indicators)
    total_licencies = df_filtre['Total'].sum()
    nombre_communes = df_filtre['Commune'].nunique()
    nombre_federations = df_filtre['Fédération'].nunique()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Licenciés", total_licencies)
    with col2:
        st.metric("Communes", nombre_communes)
    with col3:
        st.metric("Fédérations", nombre_federations)
        
    st.divider()
    
    # Le graphique du Top 5
    classement = df_filtre.groupby('Fédération')['Total'].sum().sort_values(ascending=False).head(5).reset_index()
    fig_region = px.bar(classement, x='Fédération', y='Total', color='Fédération', title="Top 5 des fédérations")
    
    # INDICE : Affiche le graphique fig_region
    st.plotly_chart(fig_region)


# --- CONTENU DE L'ONGLET 2 (Ville) ---
with onglet2:
    st.subheader(f"Maillage territorial pour : {sport_choisi}")
    
    # Le graphique du Top 10 des villes
    classement_villes = df_sport.groupby('Commune')['Total'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_villes = px.bar(classement_villes, x='Total', y='Commune', orientation='h', title=f"Top 10 des communes en {sport_choisi}")
    
    # INDICE : Affiche le graphique fig_villes
    st.plotly_chart(fig_villes)