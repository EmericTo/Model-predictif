import pandas as pd
from sklearn.linear_model import LinearRegression
import psycopg2 

#les noms des données 'DoughProduced' 'EnergyUsed' 'WashWaterUsed' servent d'exemples

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname='votre_nom_de_base_de_données',
    user='votre_utilisateur',
    password='votre_mot_de_passe',
    host='votre_host',
    port='votre_port'
)

try:
    # Récupération des données depuis la base de données
    query = "SELECT DoughProduced, EnergyUsed, WashWaterUsed FROM votre_table;"
    data = pd.read_sql(query, conn)

    # Conversion des colonnes en numériques si nécessaire
    data['DoughProduced'] = pd.to_numeric(data['DoughProduced'])
    data['EnergyUsed'] = pd.to_numeric(data['EnergyUsed'])
    data['WashWaterUsed'] = pd.to_numeric(data['WashWaterUsed'])

    # Entraînement du modèle de régression linéaire
    model = LinearRegression()
    X = data[['DoughProduced', 'EnergyUsed']]  # Variables indépendantes
    y = data['WashWaterUsed']  # Variable dépendante
    model.fit(X, y)

    # Prédiction sur de nouvelles données en fonction d'un paramètre
    new_data = pd.DataFrame({                       
        'DoughProduced': [1500, 1600, 1700],
        #'EnergyUsed': [10000, 10500, 11000]  paramètre à ajouter si on veut 
    })

    predictions = model.predict(new_data)

    # Création du DataFrame pour stocker les prédictions
    predictions_df = pd.DataFrame({                             
        'DoughProduced': new_data['DoughProduced'],
        'EnergyUsed': new_data['EnergyUsed'],
        'Predicted_WashWaterUsed': predictions
    })

    # Création du curseur pour exécuter les requêtes SQL
    cur = conn.cursor()

    # Création de la table si elle n'existe pas / ou modifier si table existante, Predisctions est le nom de la table mais sera remplacer par le nom d'une table 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Predictions (                                
            DoughProduced FLOAT,
            EnergyUsed FLOAT,
            Predicted_WashWaterUsed FLOAT
        );
    """)

    # Insertion des prédictions dans la table
    for index, row in predictions_df.iterrows():
        cur.execute("""
            INSERT INTO Predictions (DoughProduced, EnergyUsed, Predicted_WashWaterUsed)
            VALUES (%s, %s, %s);
        """, (row['DoughProduced'], row['EnergyUsed'], row['Predicted_WashWaterUsed']))

    conn.commit()

except psycopg2.Error as e:
    print("Erreur lors de l'interaction avec la base de données:", e)

finally:
    # Fermeture de la connexion à la base de données
    conn.close()

print("Les prédictions ont été stockées dans la base de données.")