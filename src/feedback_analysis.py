import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def analyze_feedback(feedback_file):
    with open(feedback_file, 'r') as f:
        feedback = f.readlines()

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(feedback)

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X)

    for i, cluster in enumerate(kmeans.cluster_centers_):
        print(f"Cluster {i}: {', '.join(vectorizer.inverse_transform(cluster)[0])}")

if __name__ == "__main__":
    analyze_feedback("user_feedback.txt")
