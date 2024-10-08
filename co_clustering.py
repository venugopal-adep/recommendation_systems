import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

# Set page config
st.set_page_config(page_title="Clustering-Based Recommendation Systems", layout="wide")

# Custom color palette
color_palette = px.colors.qualitative.Pastel

def generate_data(num_users, num_items):
    np.random.seed(42)
    return np.random.randint(0, 6, size=(num_users, num_items))

def compute_similarity(matrix):
    return cosine_similarity(matrix)

def perform_pca(matrix, n_components=3):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(matrix)

def perform_kmeans(matrix, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    return kmeans.fit_predict(matrix)

def plot_clustering(reduced_data, clusters, dimension):
    if dimension == "2D":
        fig = px.scatter(
            x=reduced_data[:, 0], 
            y=reduced_data[:, 1], 
            color=clusters, 
            title="User Clustering Based on Preferences (2D)",
            labels={"x": "PCA Component 1", "y": "PCA Component 2"},
            color_discrete_sequence=color_palette
        )
        for i, (x, y) in enumerate(zip(reduced_data[:, 0], reduced_data[:, 1])):
            fig.add_annotation(x=x, y=y, text=f"User {i+1}", showarrow=False)
    else:
        fig = px.scatter_3d(
            x=reduced_data[:, 0], 
            y=reduced_data[:, 1], 
            z=reduced_data[:, 2], 
            color=clusters, 
            title="User Clustering Based on Preferences (3D)",
            labels={"x": "PCA Component 1", "y": "PCA Component 2", "z": "PCA Component 3"},
            color_discrete_sequence=color_palette
        )
        fig.update_traces(marker=dict(size=5))
        fig.update_layout(scene=dict(
            annotations=[{
                'x': reduced_data[i, 0],
                'y': reduced_data[i, 1],
                'z': reduced_data[i, 2],
                'text': f"User {i+1}",
                'showarrow': False,
                'font': {'size': 12, 'color': 'black'},
            } for i in range(len(reduced_data))]
        ))
    return fig

def plot_heatmap(matrix, title, xaxis_title, yaxis_title):
    fig = px.imshow(matrix, text_auto=True, aspect="auto", color_continuous_scale='YlOrRd')
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )
    return fig

def main():
    st.title("Clustering-Based Recommendation Systems")

    st.markdown(r"""
    We can apply unsupervised methods (clustering) to build recommendation systems. Each cluster is assigned to typical preferences based on the preferences of customers who belong to the cluster. Customers within each cluster would receive recommendations computed at the cluster level.

    ### Steps:
    1. **Compute similarity** between each pair of users.
    2. **Obtain representation** of each user in low-dimensional space.
    3. **Perform K-means clustering** to find the number of clusters (K).

    This demo shows how users with similar preferences are clustered together to receive the same product recommendations.
    """)

    # Sidebar controls
    st.sidebar.subheader("Controls")
    num_users = st.sidebar.slider("Number of Users", 10, 100, 20)
    num_items = st.sidebar.slider("Number of Items", 5, 20, 10)
    num_clusters = st.sidebar.slider("Number of Clusters (K)", 2, 10, 3)
    dimension = st.sidebar.selectbox("Dimension", ["2D", "3D"])
    regenerate_data = st.sidebar.button("Regenerate Data")

    # Initialize or regenerate data
    if regenerate_data or 'user_item_matrix' not in st.session_state:
        st.session_state.user_item_matrix = generate_data(num_users, num_items)

    user_item_matrix = st.session_state.user_item_matrix

    # Compute similarity matrix
    similarity_matrix = compute_similarity(user_item_matrix)

    # Perform PCA for dimensionality reduction
    reduced_data = perform_pca(user_item_matrix)

    # Perform K-means clustering
    clusters = perform_kmeans(user_item_matrix, num_clusters)

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Clustering Visualization", "User-Item Matrix", "Similarity Matrix", "Explanation"])

    with tab1:
        st.plotly_chart(plot_clustering(reduced_data, clusters, dimension), use_container_width=True)

    with tab2:
        st.plotly_chart(plot_heatmap(user_item_matrix, "User-Item Matrix", "Items", "Users"), use_container_width=True)

    with tab3:
        st.plotly_chart(plot_heatmap(similarity_matrix, "User Similarity Matrix", "Users", "Users"), use_container_width=True)

    with tab4:
        st.markdown("""
        ### Explanation:
        - **User-Item Matrix**: Represents interactions between users and items.
        - **User Similarity Matrix**: Shows the cosine similarity between each pair of users.
        - **PCA**: Reduces the dimensionality of the data for visualization purposes.
        - **K-means Clustering**: Groups users with similar preferences into clusters.

        ### Example:
        Imagine a movie recommendation system:
        - Users: People watching movies.
        - Items: Movies available.
        - Clusters: Groups of users with similar movie preferences.

        Clustering helps us understand groups of users with similar preferences. Users within the same cluster receive similar recommendations, improving the efficiency and accuracy of the recommendation system.
        """)

    st.markdown("""
    ### Try adjusting the number of users, items, clusters, and dimensions using the controls in the sidebar to see how the clustering changes.
    """)

if __name__ == "__main__":
    main()
