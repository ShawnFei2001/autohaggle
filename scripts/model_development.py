from scipy.sparse import hstack
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

""" Model Selection
So we decided to have a hybrid model using both clustering and prediction model

Clustering models based on literature review:
*   K-Means
*   DBSCAN
*   Agglomerative Clustering
*   Gaussian Mixture Model

Evaluation metrics
*   Silhouette Score
*   Davies-Bouldin Index
*   Calinski-Harabasz Index
"""

data_path = "" # Enter path to data

df = pd.read_csv(data_path)

# Define Features Used
clustering_features = {"categorical": ['make', 'model', 'trim', 'state', 'color', 'interior'],
                       "numerical": ['year',  'condition', 'odometer']}

modeling_features = {"categorical": ['make', 'model', 'trim', 'state', 'color', 'interior'],
                        "numerical": ['year', 'condition', 'odometer', 'mmr', 'sale_year']}


df_clustering = df[clustering_features["categorical"] + clustering_features["numerical"]].copy()

# Encode Labels
label_encoders = {}
for col in clustering_features["categorical"]:
    le = LabelEncoder()
    df_clustering[col] = le.fit_transform(df_clustering[col].astype(str))
    label_encoders[col] = le

X_clustering = df_clustering.values

# Define clustering models
clustering_models = {
    "kmeans_2": KMeans(n_clusters= 2, n_init= 10),
    "kmeans_3": KMeans(n_clusters= 3, n_init= 10),
    "kmeans_4": KMeans(n_clusters= 4, n_init= 10)
    # "DBSCAN (eps=0.5, min_samples=5)": DBSCAN(eps=0.5, min_samples=10),
    # "Agglomerative Clustering (n_clusters=3)": AgglomerativeClustering(n_clusters=3),
}

# Store results
clustering_results = {}
best_model = None
best_score = -np.inf


for name, model in clustering_models.items():
    try:
        if isinstance(model, GaussianMixture) or isinstance(model, AgglomerativeClustering):
            cluster_labels = model.fit_predict(X_clustering)
        else:
            cluster_labels = model.fit(X_clustering).labels_
        
        df[f"cluster_{name}"] = cluster_labels

        # Sample Data for Silhouette Score to Improve Speed
        if len(set(cluster_labels)) > 1:
            sample_size = min(10000, len(X_clustering))  # Limit sample size
            silhouette = silhouette_score(X_clustering[:sample_size], cluster_labels[:sample_size])
        else:
            silhouette = None

        # Faster Evaluation Metrics
        davies_bouldin = davies_bouldin_score(X_clustering, cluster_labels)
        calinski_harabasz = calinski_harabasz_score(X_clustering, cluster_labels)

        clustering_results[name] = {
            "Silhouette Score": silhouette,
            "Davies-Bouldin Index": davies_bouldin,
            "Calinski-Harabasz Index": calinski_harabasz
        }

        if silhouette is not None and silhouette > best_score:
            best_score = silhouette
            best_model = name
            
    except Exception as e:
        clustering_results[name] = {"Error": str(e)}

# Convert Results to DataFrame and Select Best Cluster
df_clustering_results = pd.DataFrame(clustering_results).T
df_clustering_results.index.name = "Model"
print(df_clustering_results)
print(f"\nBest Model: {best_model}")

df["final_cluster"] = df[f"cluster_{best_model}"]

drop_cols = [col for col in df.columns if col.startswith("cluster_") and col != "final_cluster"]
df.drop(columns=drop_cols, inplace=True)

"""
Model Training by Cluster

"""
# Define features and target
target_col = "sellingprice"  # Target variable

# Ensure All Categorical Columns Encoded
for col in modeling_features["categorical"]:
    if col not in clustering_features["categorical"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# Store results
model_performance = {}

for cluster in df["final_cluster"].unique():
    print(f"\nTraining models for Cluster {cluster}...")

    # Filter data for the current cluster
    df_cluster = df[df["final_cluster"] == cluster]

    # Train-Test Split (80-20)
    X = df_cluster[modeling_features["categorical"] + modeling_features["numerical"]]
    y = df_cluster[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 1)

    # Define models
    models = {
        "Linear Regression": LinearRegression(),
        # "Support Vector Machine": SVR(kernel="rbf"), # Too Slow 
        "LightGBM": lgb.LGBMRegressor(boosting_type="gbdt", objective="regression")
    }

    cluster_results = {}

    for model_name, model in models.items():
        print(f" - Training {model_name} for Cluster {cluster}...")

        # Train model
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)

        # Evaluate performance
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        # Store results
        cluster_results[model_name] = {"RMSE": rmse, "R²": r2}

    model_performance[f"Cluster {cluster}"] = cluster_results

# Convert results to DataFrame for easy comparison
df_model_performance = pd.DataFrame(model_performance).T

print(df_model_performance)