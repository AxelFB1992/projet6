# Projet 6 — Anticipez les besoins en consommation de bâtiments

> OpenClassrooms · Parcours Data Engineer
> Prédiction de la consommation énergétique des bâtiments non résidentiels de Seattle, exposée par une API déployée dans le cloud.

---

## Contexte

La ville de Seattle s'est fixé un objectif de neutralité carbone. Les relevés de consommation des bâtiments non résidentiels sont coûteux à obtenir : l'objectif est de **prédire la consommation énergétique d'un bâtiment à partir de ses caractéristiques** (usage, surface, année de construction, quartier, sources d'énergie…), puis de **mettre ce modèle à disposition des équipes de la ville via une API**.

Le projet se déroule en deux parties :
1. **Modélisation** : analyse exploratoire, préparation des données, comparaison et optimisation de modèles supervisés.
2. **Mise en production** : exposition du meilleur modèle par une API BentoML, conteneurisation et déploiement sur Google Cloud Run.

## Outils

| Domaine | Outils |
|---|---|
| Analyse et modélisation | Python, pandas, NumPy, scikit-learn, XGBoost, Matplotlib, Seaborn |
| Exposition du modèle | BentoML, Pydantic |
| Conteneurisation et cloud | Docker, Google Cloud Run |
| Environnement | JupyterLab, environnement virtuel Python, Git |

## Structure du dépôt

```
projet6/
├── template_modelisation_supervisee.ipynb  # Notebook principal : analyse, modélisation, mise en production
├── main.ipynb                              # Journal de bord : environnement de travail et Git
├── 2016_Building_Energy_Benchmarking.csv   # Données sources
├── dataset_clean.csv                       # Données nettoyées
├── service.py                              # Service BentoML (endpoint de prédiction)
├── schemas.py                              # Schéma d'entrée de l'API (Pydantic)
├── bentofile.yaml                          # Configuration du « bento » (archive déployable)
└── requirements.txt                        # Dépendances Python
```

## Démarche

### Partie 1 — Modélisation

1. **Analyse exploratoire et filtrage**
   - Description des variables quantitatives et qualitatives.
   - Filtrage des lignes : types de bâtiments hors périmètre, valeurs aberrantes, relevés non conformes.
   - Filtrage des colonnes : taux de valeurs manquantes élevé, variance nulle, identifiants, **fuites de données** (composantes ou dérivées de la cible), redondances (émissions de gaz, localisation, usages).
2. **Feature engineering**
   - Indicateurs des sources d'énergie utilisées (électricité, gaz, vapeur).
   - Regroupement des usages des bâtiments en grandes catégories (bureaux, commerce, logistique, éducation, santé…) et surfaces associées.
   - Variable d'âge du bâtiment et contrôles de cohérence des surfaces.
3. **Préparation des données** : passage au logarithme de la cible, séparation des jeux d'entraînement et de test.
4. **Comparaison de modèles** : régression linéaire comme référence, puis plusieurs modèles comparés sur plusieurs échantillons (R², RMSE, MAE).
5. **Optimisation et interprétation** : recherche des meilleurs hyperparamètres des trois meilleurs modèles ; **XGBoost** est retenu.

### Partie 2 — Mise en production

1. **Sauvegarde du modèle** dans le magasin de modèles de BentoML.
2. **Création du service** (`service.py`) : un endpoint `predict` reçoit les caractéristiques d'un bâtiment, applique les mêmes transformations que lors de l'entraînement, puis renvoie la consommation prédite.
3. **Validation des entrées** (`schemas.py`) : schéma Pydantic avec des listes de valeurs autorisées (quartiers, usages), pour rejeter les requêtes invalides.
4. **Construction du bento et de l'image Docker** à partir de `bentofile.yaml`.
5. **Déploiement sur Google Cloud Run**.

## Lancer le service en local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Le modèle doit être présent dans le magasin BentoML (voir le notebook)
bentoml models list

# Lancer le service
bentoml serve service:EnergyPrediction
```

L'API est alors accessible sur `http://localhost:3000`, avec une documentation interactive permettant de tester l'endpoint `predict`.

## Compétences mises en œuvre

- Préparer et transformer des données pour un modèle d'apprentissage
- Entraîner, comparer et évaluer des modèles supervisés
- Exposer un modèle par une API et la conteneuriser
- Déployer un service dans le cloud
