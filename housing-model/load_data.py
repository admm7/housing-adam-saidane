import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import joblib

# Charger les données
housing = pd.read_csv("housing.csv")
print("Données chargées avec succès !")

# Aperçu des données
print("Aperçu des données :")
print(housing.head())

# 1. Statistiques descriptives
print("\nStatistiques descriptives :")
print(housing.describe())

# 2. Vérifier les valeurs manquantes avant traitement
print("\nValeurs manquantes avant traitement :")
print(housing.isnull().sum())

# 3. Lignes avec des valeurs manquantes dans 'total_bedrooms'
print("\nLignes avec valeurs manquantes dans 'total_bedrooms' :")
print(housing[housing['total_bedrooms'].isnull()])

# 4. Traitement des valeurs manquantes
print("\nTraitement des valeurs manquantes...")
median_total_bedrooms = housing['total_bedrooms'].median()
housing['total_bedrooms'] = housing['total_bedrooms'].fillna(median_total_bedrooms)
print(f"Valeurs manquantes remplacées par la médiane : {median_total_bedrooms}")

# 5. Vérifier les valeurs manquantes après traitement
print("\nValeurs manquantes après traitement :")
print(housing.isnull().sum())

# Aperçu des données après traitement
print("\nAperçu des données après traitement :")
print(housing.head())

# Enregistrer les données nettoyées dans un fichier CSV
output_file = "housing_cleaned.csv"
housing.to_csv(output_file, index=False)
print(f"\nLes données nettoyées ont été enregistrées dans le fichier '{output_file}'.")

# 6. Détection des outliers avec des boîtes à moustaches
print("\nDétection des outliers...")
plt.figure(figsize=(15, 10))
for i, column in enumerate(["median_income", "housing_median_age", "total_rooms", "median_house_value"], start=1):
    plt.subplot(2, 2, i)
    sns.boxplot(x=housing[column])
    plt.title(f"Boîte à moustaches - {column}")
plt.tight_layout()
plt.savefig("boxplots.png")  # Enregistre les graphiques pour éviter les interruptions
plt.close()

# 7. Visualisation des relations clés avec scatterplots
print("\nVisualisation des relations clés...")
plt.figure(figsize=(15, 10))

# Relation entre median_income et median_house_value
plt.subplot(2, 2, 1)
sns.scatterplot(data=housing, x="median_income", y="median_house_value", alpha=0.5)
plt.title("median_income vs median_house_value")

# Relation entre housing_median_age et median_house_value
plt.subplot(2, 2, 2)
sns.scatterplot(data=housing, x="housing_median_age", y="median_house_value", alpha=0.5)
plt.title("housing_median_age vs median_house_value")

# Relation entre total_rooms et median_house_value
plt.subplot(2, 2, 3)
sns.scatterplot(data=housing, x="total_rooms", y="median_house_value", alpha=0.5)
plt.title("total_rooms vs median_house_value")

plt.tight_layout()
plt.savefig("scatterplots.png")  # Enregistre les graphiques
plt.close()

# 8. Exploration géographique (latitude/longitude)
print("\nExploration des données géographiques...")
plt.figure(figsize=(10, 8))
sns.scatterplot(data=housing, x="longitude", y="latitude", hue="median_house_value", palette="coolwarm", alpha=0.7)
plt.title("Prix des maisons selon la géographie (longitude vs latitude)")
plt.savefig("geo_scatterplot.png")  # Enregistre le graphique
plt.close()

# Résumé des observations
print("\nRésumé des observations :")
print("1. Les boîtes à moustaches révèlent des valeurs aberrantes dans certaines colonnes.")
print("2. La relation entre median_income et median_house_value montre une forte corrélation positive.")
print("3. Les données géographiques révèlent des schémas intéressants liés aux prix des maisons dans différentes zones.")

# Préparation des données pour le modèle
print("\nPréparation des données pour le modèle...")
X = housing.drop("median_house_value", axis=1)
y = housing["median_house_value"]

# Encoder la colonne 'ocean_proximity' et standardiser les colonnes numériques
categorical_columns = ["ocean_proximity"]
numerical_columns = X.select_dtypes(include=["float64", "int64"]).columns

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_columns),
        ("cat", OneHotEncoder(), categorical_columns),
    ],
    remainder="passthrough"
)

X_processed = preprocessor.fit_transform(X)

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42
)

print("Données divisées :")
print(f"Entraînement : {X_train.shape}, Test : {X_test.shape}")


# Définir les modèles à tester
models = {
    "Random Forest": RandomForestRegressor(random_state=42),
    "Linear Regression": LinearRegression(),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
}

# Stocker les résultats
results = {}

# Tester chaque modèle
for model_name, model in models.items():
    print(f"\nModèle : {model_name}")
    
    # Entraîner le modèle
    model.fit(X_train, y_train)
    
    # Prédire sur le jeu de test
    y_pred = model.predict(X_test)
    
    # Évaluer le modèle
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Stocker les résultats
    results[model_name] = {"MSE": mse, "R2": r2}
    
    # Afficher les performances
    print(f"Mean Squared Error (MSE) : {mse:.2f}")
    print(f"Coefficient de détermination (R²) : {r2:.2f}")
    
    # Visualisation des prédictions vs valeurs réelles
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2)
    plt.title(f"Valeurs réelles vs Valeurs prédites ({model_name})")
    plt.xlabel("Valeurs réelles")
    plt.ylabel("Valeurs prédites")
    plt.show()

# Résumé des performances
print("\nRésumé des performances des modèles :")
for model_name, metrics in results.items():
    print(f"{model_name} -> MSE: {metrics['MSE']:.2f}, R²: {metrics['R2']:.2f}")

# Trouver le meilleur modèle
best_model = min(results, key=lambda x: results[x]["MSE"])
print(f"\nMeilleur modèle : {best_model} avec MSE = {results[best_model]['MSE']:.2f} et R² = {results[best_model]['R2']:.2f}")

# Sauvegarder le meilleur modèle
best_model_instance = models[best_model]
joblib.dump(best_model_instance, "best_model.pkl")
print(f"\nLe modèle '{best_model}' a été sauvegardé dans 'best_model.pkl'.")
