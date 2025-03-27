import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix

# Fonction pour charger et explorer les données
def load_data():
    data = pd.read_csv("data/BeansDataset.csv")
    return data

# Fonction pour effectuer l'analyse
def analyze_data(data, selected_filters):
    # Analyser les ventes totales par produit
    total_sales = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
    
    # Appliquer les filtres de sélection
    if 'Canal' in selected_filters:
        sales_by_channel = data.groupby('Channel')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
    else:
        sales_by_channel = None
    
    if 'Région' in selected_filters:
        sales_by_region = data.groupby('Region')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
    else:
        sales_by_region = None

    return total_sales, sales_by_channel, sales_by_region

# Fonction pour afficher des graphiques
def plot_sales_data(total_sales, sales_by_channel, sales_by_region, sales_by_online_store=None):
    # Graphique des ventes totales par produit
    fig, ax = plt.subplots()
    total_sales.plot(kind='bar', ax=ax, color=['#FF6347', '#FFCC00', '#4CAF50', '#00BCD4', '#9C27B0', '#FF5722'])
    ax.set_title('Ventes Totales par Produit')
    ax.set_ylabel('Montant des ventes')
    st.pyplot(fig)

    # Graphique des ventes par canal (si disponible)
    if sales_by_channel is not None:
        fig, ax = plt.subplots()
        sales_by_channel.plot(kind='bar', ax=ax)
        ax.set_title('Ventes par Canal')
        ax.set_ylabel('Montant des ventes')
        st.pyplot(fig)

    # Graphique des ventes par région (si disponible)
    if sales_by_region is not None:
        fig, ax = plt.subplots()
        sales_by_region.plot(kind='bar', ax=ax)
        ax.set_title('Ventes par Région')
        ax.set_ylabel('Montant des ventes')
        st.pyplot(fig)
    
    # Graphique des ventes en ligne vs en magasin (si les données sont disponibles)
    if sales_by_online_store is not None:
        fig, ax = plt.subplots()
        sales_by_online_store.plot(kind='bar', ax=ax, color=['#66b3ff', '#ff6666'])
        ax.set_title('Ventes en ligne vs en magasin')
        ax.set_ylabel('Montant des ventes')
        ax.set_xticklabels(['En ligne', 'En magasin'], rotation=0)
        st.pyplot(fig)

# Fonction pour générer des recommandations
def generate_recommendations(total_sales, sales_by_channel, sales_by_region):
    recommendations = []

    # Recommandations basées sur les ventes totales par produit
    max_product_sales = total_sales.idxmax()
    recommendations.append(f"Le produit le plus vendu est {max_product_sales}. il faudra faire une campagne dans cette zone pour augmenter les vent.")

    # Recommandations basées sur les ventes par canal
    if sales_by_channel is not None:
        max_channel_sales = sales_by_channel.sum(axis=1).idxmax()
        recommendations.append(f"Le canal de vente le plus performant est {max_channel_sales}.pour augmenter les ventes onr devrait faire une campagne de marketing.")

    # Recommandations basées sur les ventes par région
    if sales_by_region is not None:
        max_region_sales = sales_by_region.sum(axis=1).idxmax()
        recommendations.append(f"La région la plus performante est {max_region_sales}. Beans & Pods devrait s'installer plus dans cette zone.")

    return recommendations

# Fonction pour afficher les suggestions de données à collecter
def suggest_additional_data():
    suggestions = [
        "Collecter des informations sur les préférences des clients par produit (ex : goûts, types de boissons préférées).",
        "Analyser l'impact des promotions et des campagnes marketing sur les ventes.",
        "Suivre les comportements d'achat des clients en ligne (ex : fréquence des achats, panier moyen).",
        "Recueillir des avis clients sur les produits pour identifier des axes d'amélioration."
    ]
    return suggestions

# Application Streamlit (sans la fonction main())
st.markdown(
    """
    <div style='text-align:center'>
    <h1> Statistiques descriptives et Analyse de données </h1>
    </div>
    """, unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("Menu")
page = st.sidebar.radio("Choisir une option", ["Accueil", "Analyse des Ventes", "Peek at the Data", "Visualisation"])

# Multiselect pour choisir les filtres (canaux et/ou régions) dans le menu
selected_filters = st.sidebar.multiselect(
    "Choisissez les critères d'analyse",
    ["Canal", "Région"],
    default=["Canal", "Région"]
)

if page == "Accueil":
    st.subheader('Affichage des données des ventes de Beans & Pods')
    data = load_data()
    st.dataframe(data)

elif page == "Peek at the Data":
    st.subheader('Aperçu des 10 premières lignes')
    data = load_data()
    st.dataframe(data.head(10))

    # Calcul du nombre de produits vendus par class
    st.subheader('Répartition des ventes par produit')
    st.write(data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum())

    # Affichage des graphiques de répartition des ventes par produit
    st.subheader('Graphiques des ventes totales par produit')
    total_sales, _, _ = analyze_data(data, selected_filters)
    plot_sales_data(total_sales, None, None)

elif page == "Visualisation":
    st.subheader('Graphiques des ventes')
    data = load_data()
    total_sales, sales_by_channel, sales_by_region = analyze_data(data, selected_filters)

    # Créer un graphique pour les ventes en ligne vs en magasin
    sales_by_online_store = data.groupby('Channel')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
    online_store_sales = sales_by_online_store.loc[['Online', 'Store']].sum(axis=1)  # Prendre les ventes en ligne et en magasin
    plot_sales_data(total_sales, sales_by_channel, sales_by_region, online_store_sales)

elif page == "Analyse des Ventes":
    st.title("Analyse des Ventes de Beans & Pods")
    
    # Charger les données
    data = load_data()
    
    st.write("### Aperçu des Données")
    st.write(data.head())
    
    # Analyse des données en fonction des filtres sélectionnés
    total_sales, sales_by_channel, sales_by_region = analyze_data(data, selected_filters)
    
    # Visualisation des résultats
    st.write("### Graphiques des Ventes")
    plot_sales_data(total_sales, sales_by_channel, sales_by_region)
    
    # Recommandations
    st.write("### Recommandations")
    recommendations = generate_recommendations(total_sales, sales_by_channel, sales_by_region)
    for rec in recommendations:
        st.write(f"- {rec}")
    
    # Suggestions de collecte de données futures
    st.write("### Suggestions pour l'Avenir")
    additional_data_suggestions = suggest_additional_data()
    for suggestion in additional_data_suggestions:
        st.write(f"- {suggestion}")

