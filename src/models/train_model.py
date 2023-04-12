import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

 

# Load preprocessed training dataset
Train = pd.read_csv('C:/Users/243415/Documents/flaskdocumentation/sree/data/processed/Train.csv')

 



 

# Train k-means clustering model with k=4
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(Train)

 

# Save the trained model as a pickle file
with open("models/scaledmodel.pkl", "wb") as f:
    pickle.dump(kmeans, f)
 