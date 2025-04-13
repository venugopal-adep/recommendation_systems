import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

# Configure page
st.set_page_config(page_title="SVD Magic", layout="wide")
st.title("✨ SVD: The Secret Sauce of Recommendations")

# Generate synthetic data
@st.cache_data
def generate_data(n_users=100, n_items=50, sparsity=0.7):
    np.random.seed(42)
    dense_matrix = np.random.randint(1,6,size=(n_users,n_items))
    mask = np.random.choice([0,1], size=(n_users,n_items), p=[sparsity,1-sparsity])
    sparse_matrix = dense_matrix * mask
    return sparse_matrix

# Sidebar controls
with st.sidebar:
    st.header("🔧 Controls")
    sparsity = st.slider("Matrix Sparsity", 0.1, 0.9, 0.7)
    k = st.slider("Latent Factors (k)", 1, 20, 5)
    selected_user = st.selectbox("Select User", options=range(1,101))

# Generate and decompose matrix
sparse_matrix = generate_data(sparsity=sparsity)
U, sigma, Vt = svds(sparse_matrix.astype(float), k=k)
sigma = np.diag(sigma)
reconstructed = U @ sigma @ Vt

# Visualization tabs
tab1, tab2, tab3 = st.tabs(["📊 Matrix View", "🔍 Latent Space", "🎯 Recommendations"])

with tab1:
    sparsity_value = (sparse_matrix == 0).mean()
    matrix_title = f"Sparsity: {sparsity_value:.0%}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Sparse Matrix")
        fig = px.imshow(sparse_matrix, color_continuous_scale='Blues',
                       zmin=0, zmax=5,
                       title=matrix_title,
                       labels=dict(x="Items", y="Users", color="Rating"))
        fig.update_layout(
            height=500,
            width=500,
            xaxis_showgrid=False,
            yaxis_showgrid=False
        )
        # Turn off autosize to maintain exact dimensions
        fig.update_layout(autosize=False)
        st.plotly_chart(fig, use_container_width=False)
    
    with col2:
        st.subheader("SVD Reconstructed Matrix")
        fig = px.imshow(reconstructed, color_continuous_scale='Greens',
                       zmin=0, zmax=5,
                       title=f"Using {k} latent factors",
                       labels=dict(x="Items", y="Users", color="Rating"))
        fig.update_layout(
            height=500,
            width=500,
            xaxis_showgrid=False,
            yaxis_showgrid=False
        )
        # Turn off autosize to maintain exact dimensions
        fig.update_layout(autosize=False)
        st.plotly_chart(fig, use_container_width=False)

with tab2:
    st.subheader("3D Latent Space Projection")
    
    # Add explanation
    st.markdown("""
    ### Interpreting the Latent Space
    This 3D visualization shows users and items positioned in the latent factor space:
    - **Proximity** between users/items indicates similarity
    - **Clusters** represent groups with similar preferences/characteristics
    - **Distance** represents preference dissimilarity
    
    Each axis corresponds to a latent factor that captures some underlying pattern in the data.
    """)
    
    # User embeddings
    user_df = pd.DataFrame(U, columns=[f"Factor {i+1}" for i in range(U.shape[1])])
    user_df['Type'] = 'User'
    user_df['ID'] = [f"User {i+1}" for i in range(U.shape[0])]
    
    # Apply clustering to users
    from sklearn.cluster import KMeans
    
    # Choose number of clusters - this is adjustable
    n_clusters = min(5, k)
    
    # Apply KMeans clustering to user embeddings
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    user_clusters = kmeans.fit_predict(U)
    
    # Add cluster information to user dataframe
    user_df['Cluster'] = [f"User Cluster {i+1}" for i in user_clusters]
    
    # Item embeddings
    item_df = pd.DataFrame(Vt.T, columns=[f"Factor {i+1}" for i in range(Vt.shape[0])])
    item_df['Type'] = 'Item'
    item_df['ID'] = [f"Item {i+1}" for i in range(Vt.T.shape[0])]
    item_df['Cluster'] = 'Items'  # All items in one group for color distinction
    
    combined_df = pd.concat([user_df, item_df])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create visualization with cluster-based coloring
        fig = px.scatter_3d(combined_df, 
                          x='Factor 1', y='Factor 2', z='Factor 3',
                          color='Cluster', symbol='Type',
                          hover_name='ID',
                          hover_data={
                              'Factor 1': ':.2f',
                              'Factor 2': ':.2f', 
                              'Factor 3': ':.2f',
                              'Type': True,
                              'Cluster': True,
                              'ID': False
                          },
                          title="Users & Items in Latent Space")
        
        # Enhance visualization
        fig.update_layout(
            scene=dict(
                xaxis_title="Factor 1",
                yaxis_title="Factor 2",
                zaxis_title="Factor 3"
            ),
            legend_title="Groups"
        )
        
        # Add explanatory annotations
        st.plotly_chart(fig, use_container_width=True)
        
        # Show clustering explanation
        st.markdown("""
        **User Clusters**: Users are grouped by color based on similar preferences in the latent space.
        Users in the same cluster likely have similar rating patterns and would receive similar recommendations.
        """)
    
    with col2:
        st.markdown("### Latent Factor Analysis")
        
        # Show factor importance
        sigma_diag = np.diag(sigma)
        factor_importance = pd.DataFrame({
            'Latent Factor': [f"Factor {i+1}" for i in range(len(sigma_diag))],
            'Importance': sigma_diag / sum(sigma_diag)
        })
        
        fig2 = px.bar(factor_importance, x='Latent Factor', y='Importance', 
                     color='Importance', text_auto='.1%',
                     title="Relative Factor Importance")
        fig2.update_layout(yaxis_tickformat='.1%')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Add an explanation
        st.markdown("""
        **What to look for:**
        - Users close to items: strong preference
        - Users in the same cluster: similar taste groups
        - Distant users/items: dissimilar preferences
        
        The bar chart shows how much each factor contributes to explaining the variance in user-item ratings.
        """)
        
        # Add cluster information
        st.markdown("### Cluster Information")
        cluster_counts = user_df['Cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Cluster', 'Number of Users']
        st.dataframe(cluster_counts)

with tab3:
    st.subheader("Personalized Recommendations")
    
    # Get user predictions
    user_idx = selected_user - 1
    predicted_ratings = reconstructed[user_idx]
    top_items = np.argsort(-predicted_ratings)[:5] + 1
    
    # Display recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛍️ Recommended Items")
        for i, item in enumerate(top_items, 1):
            st.markdown(f"{i}. **Item {item}** (Predicted Rating: {predicted_ratings[item-1]:.1f})")
    
    with col2:
        st.markdown("### 📈 Preference Analysis")
        factors = pd.DataFrame({
            'Latent Factor': [f"Factor {i+1}" for i in range(k)],
            'Weight': U[user_idx]
        })
        fig = px.bar(factors, x='Latent Factor', y='Weight', 
                    color='Weight', color_continuous_scale='Bluered')
        st.plotly_chart(fig, use_container_width=True)

# Explanation section
st.markdown("---")
with st.expander("🔮 How SVD Works with Sparse Data"):
    sparsity_percentage = (sparse_matrix == 0).mean() * 100
    st.markdown(f"""
    **Singular Value Decomposition (SVD)** handles sparse matrices by:
    1. **Finding latent patterns**: Even with missing data ($\\approx$ {sparsity_percentage:.0f}% empty cells)
    2. **Matrix factorization**: Breaking down $A_{{m×n}}$ into $U_{{m×k}}Σ_{{k×k}}V^T_{{k×n}}$
    3. **Noise reduction**: Keeping only the top {k} most important patterns
    4. **Prediction**: Reconstructing the matrix to fill in missing values
    
    *Hover over matrix cells to see predicted vs original values!*
    """)
 
