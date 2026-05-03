# ==========================================
# PRACTICAL: K-MEANS CLUSTERING
# ==========================================

# Import required libraries
import pandas as pd                      # For data handling
import matplotlib.pyplot as plt          # For plotting graphs
from sklearn.cluster import KMeans       # K-Means algorithm


# ------------------------------------------
# STEP 1: LOAD DATASET
# ------------------------------------------

# Load dataset (Mall Customers)
data = pd.read_excel("D:/Practicals/Mall_Customers.xlsx")

# Display first 5 rows
print("Dataset Preview:")
print(data.head())

# Display column names
print("\nColumns:", data.columns)


# ------------------------------------------
# STEP 2: SELECT FEATURES
# ------------------------------------------

# Select relevant features for clustering
# We are using:
# 1. Annual Income
# 2. Spending Score

X = data[['Annual Income (k$)', 'Spending Score (1-100)']]


# ------------------------------------------
# STEP 3: ELBOW METHOD (Find Optimal K)
# ------------------------------------------

# WCSS = Within-Cluster Sum of Squares
# It measures how compact the clusters are

wcss = []

# Try cluster sizes from 1 to 10
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X)
    
    # Append inertia (WCSS)
    wcss.append(kmeans.inertia_)

# Plot Elbow Graph
plt.figure()
plt.plot(range(1, 11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.show()


# ------------------------------------------
# STEP 4: APPLY K-MEANS WITH OPTIMAL K
# ------------------------------------------

# From elbow graph, we assume K = 5
kmeans = KMeans(n_clusters=5, random_state=42)

# Fit model and predict clusters
data['Cluster'] = kmeans.fit_predict(X)


# ------------------------------------------
# STEP 5: VISUALIZE CLUSTERS
# ------------------------------------------

# Define colors for clusters
colors = ['red', 'blue', 'green', 'purple', 'orange']

# Plot each cluster
for i in range(5):
    plt.scatter(
        data[data['Cluster'] == i]['Annual Income (k$)'],
        data[data['Cluster'] == i]['Spending Score (1-100)'],
        color=colors[i],
        label=f'Cluster {i}'
    )

# Plot centroids (center of each cluster)
plt.scatter(
    kmeans.cluster_centers_[:, 0],  # X-axis (Income)
    kmeans.cluster_centers_[:, 1],  # Y-axis (Spending)
    s=200,
    c='black',
    marker='X',
    label='Centroids'
)

# Add labels and title
plt.title("Customer Segmentation (K-Means)")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend()

# Show final plot
plt.show()
