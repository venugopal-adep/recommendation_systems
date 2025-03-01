import streamlit as st
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

# Set page config with custom theme
st.set_page_config(page_title="Smart Recommendations", layout="wide")

# Custom color palette - modern and aesthetic
colors = {
    "primary": "#6C5CE7",
    "secondary": "#FDA7DF",
    "accent": "#12CBC4",
    "background": "#F8F9FA",
    "clusters": px.colors.qualitative.Pastel
}

# Apply custom CSS
st.markdown("""
<style>
    .main {background-color: #F8F9FA;}
    h1 {color: #6C5CE7;}
    h2 {color: #12CBC4;}
    .stTabs [data-baseweb="tab-list"] {gap: 8px;}
    .stTabs [data-baseweb="tab"] {
        background-color: #F8F9FA;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        color: #6C5CE7;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6C5CE7 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_data(num_users, num_items):
    np.random.seed(42)
    return np.random.randint(0, 6, size=(num_users, num_items))

def plot_clustering(reduced_data, clusters, dimension):
    if dimension == "2D":
        fig = px.scatter(
            x=reduced_data[:, 0], y=reduced_data[:, 1], 
            color=clusters, 
            labels={"x": "Component 1", "y": "Component 2"},
            color_discrete_sequence=colors["clusters"],
            template="plotly_white"
        )
        fig.update_traces(marker=dict(size=12, opacity=0.8))
    else:
        fig = px.scatter_3d(
            x=reduced_data[:, 0], y=reduced_data[:, 1], z=reduced_data[:, 2], 
            color=clusters, 
            labels={"x": "Component 1", "y": "Component 2", "z": "Component 3"},
            color_discrete_sequence=colors["clusters"],
            template="plotly_white"
        )
        fig.update_traces(marker=dict(size=8, opacity=0.8))
    
    fig.update_layout(
        title=f"User Clustering ({dimension})",
        legend_title="Clusters",
        plot_bgcolor=colors["background"],
        height=600
    )
    return fig

def plot_heatmap(matrix, title):
    fig = px.imshow(
        matrix, 
        color_continuous_scale=["#FFFFFF", colors["primary"]],
        template="plotly_white"
    )
    fig.update_layout(
        title=title,
        height=500,
        plot_bgcolor=colors["background"]
    )
    return fig

def main():
    st.title("✨ Clustering based Recommendation System")
    
    with st.sidebar:
        st.markdown(f"<h2 style='color:{colors['primary']}'>Controls</h2>", unsafe_allow_html=True)
        
        num_users = st.slider("👥 Number of Users", 10, 50, 20)
        num_items = st.slider("🛍️ Number of Items", 5, 20, 10)
        num_clusters = st.slider("🔍 Number of Clusters", 2, 8, 3)
        dimension = st.radio("📊 Visualization", ["2D", "3D"])
        
        if st.button("🔄 Regenerate Data", use_container_width=True):
            st.session_state.user_item_matrix = generate_data(num_users, num_items)
    
    # Initialize or get data
    if 'user_item_matrix' not in st.session_state:
        st.session_state.user_item_matrix = generate_data(num_users, num_items)
    
    user_item_matrix = st.session_state.user_item_matrix
    
    # Process data
    similarity_matrix = cosine_similarity(user_item_matrix)
    reduced_data = PCA(n_components=3).fit_transform(user_item_matrix)
    clusters = KMeans(n_clusters=num_clusters, random_state=42).fit_predict(user_item_matrix)
    
    # Create tabs with visualizations
    tab1, tab2, tab3 = st.tabs(["📊 Clustering", "📈 Data Matrix", "ℹ️ About"])
    
    with tab1:
        st.plotly_chart(plot_clustering(reduced_data, clusters, dimension), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Users", num_users)
        with col2:
            st.metric("Clusters", num_clusters)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_heatmap(user_item_matrix, "User-Item Interactions"), use_container_width=True)
        with col2:
            st.plotly_chart(plot_heatmap(similarity_matrix, "User Similarity"), use_container_width=True)
    
    with tab3:
        st.markdown("""
        ## How It Works
        
        This system groups users with similar preferences to provide targeted recommendations:
        
        1. **Collect** user interaction data
        2. **Analyze** similarities between users
        3. **Group** similar users into clusters
        4. **Recommend** items popular within each cluster
        
        Adjust the controls to see how different parameters affect user grouping.
        """)

if __name__ == "__main__":
    main()
