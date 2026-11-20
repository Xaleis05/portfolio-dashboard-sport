# 1. Les imports
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# 2. Configuration de la page
st.set_page_config(page_title="Dashboard Sport", layout="wide")

# 3. Affichage du titre principal sur la page web
st.title("Analyse des Licences Sportives en France")

# 4. Chargement des données avec CACHE (Évite les crashs de mémoire)
st.write("Chargement des données en cours...")

# On demande à Streamlit de garder ce fichier lourd en mémoire
@st.cache_data
def charger_donnees():
    return pd.read_csv("donnees_sport.zip", sep=";", low_memory=False)

# On appelle la fonction
df = charger_donnees()

# Affichage du message de succès
st.success(f"Données chargées avec succès ! Taille du tableau : {df.shape}")


# --- ÉTAPE 3 : La Barre latérale (Sidebar) ---
st.sidebar.header("Paramètres d'analyse")

# 1. Filtre de région dans la sidebar
liste_regions = df['Région'].dropna().unique()
region_choisie = st.sidebar.selectbox("Sélectionnez une région :", liste_regions)
df_filtre = df[df['Région'] == region_choisie]

# 2. Filtre de sport dans la sidebar
liste_sports = df_filtre['Fédération'].dropna().unique()
sport_choisi = st.sidebar.selectbox("Choisissez un sport :", liste_sports)
df_sport = df_filtre[df_filtre['Fédération'] == sport_choisi]


# --- ÉTAPE 4 : Les Onglets (Tabs) ---
onglet1, onglet2 = st.tabs(["Analyse Régionale", "Analyse Locale"])

# --- CONTENU DE L'ONGLET 1 (Région) ---
with onglet1:
    st.subheader(f"Aperçu de la région : {region_choisie}")
    
    # Les KPIs
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
    
    st.plotly_chart(fig_region, use_container_width=True)


# --- CONTENU DE L'ONGLET 2 (Ville) ---
with onglet2:
    st.subheader(f"Maillage territorial pour : {sport_choisi}")
    
    # Le graphique du Top 10 des villes
    classement_villes = df_sport.groupby('Commune')['Total'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_villes = px.bar(classement_villes, x='Total', y='Commune', orientation='h', title=f"Top 10 des communes en {sport_choisi}")
    
    st.plotly_chart(fig_villes, use_container_width=True)


# --- ÉTAPE 5 : IA & Machine Learning (Preuve de Concept) ---
st.divider()
st.header("IA & Machine Learning : Prédictions Football")

# Avertissement de la démarche POC pour les recruteurs
st.info("💡 Démonstration du modèle prédictif (POC) isolée sur l'historique de la région Nouvelle-Aquitaine pour la stabilité du serveur.")

# 1. Historique simulé et mis à l'échelle (Étape ETL)
historique_foot = pd.DataFrame({
    'Annee': [2018, 2019, 2020, 2021, 2022, 2023],
    'Licencies': [189000, 191500, 168000, 162000, 182000, 192365] 
})

# 2. Préparation des variables pour l'algorithme
X_train = historique_foot[['Annee']] 
y_train = historique_foot['Licencies'] 

# 3. Création et Entraînement de l'Intelligence Artificielle
modele_ia = LinearRegression()
modele_ia.fit(X_train, y_train) 

# 4. On demande à l'IA de deviner l'avenir
annees_futures = pd.DataFrame({'Annee': [2024, 2025, 2026, 2027]})
annees_futures['Licencies'] = modele_ia.predict(annees_futures).round()

# 5. Dataviz : Préparation des données pour le graphique
historique_foot['Type'] = 'Historique Réel'
annees_futures['Type'] = 'Prédiction IA'
df_complet = pd.concat([historique_foot, annees_futures])

# 6. Affichage du graphique interactif
fig_ia = px.line(
    df_complet, x='Annee', y='Licencies', color='Type', markers=True,
    title="Évolution et Prédictions des licences de Football (Nouvelle-Aquitaine)",
    color_discrete_map={"Historique Réel": "#1f77b4", "Prédiction IA": "#ff7f0e"}
)
fig_ia.update_layout(yaxis_range=[140000, 220000])

st.plotly_chart(fig_ia, use_container_width=True)
