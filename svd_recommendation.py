import streamlit as st
import numpy as np
import plotly.express as px
from scipy.linalg import svd
import pandas as pd

# Page setup
st.set_page_config(layout="wide", page_title="SVD for Sparse Matrices")
color_scale = 'Viridis'

# Clean header with minimal text
st.markdown("""
# <center>SVD for Sparse Matrices</center>
<center><small>Visualizing how SVD solves the sparsity problem in recommendation systems</small></center>
""", unsafe_allow_html=True)

# Sidebar controls with better organization
with st.sidebar:
    st.markdown("## Matrix Parameters")
    num_users = st.slider("Users", 5, 15, 8)
    num_items = st.slider("Items", 5, 15, 10)
    sparsity = st.slider("Sparsity Level (%)", 50, 95, 75)
    num_latent_features = st.slider("Latent Features", 2, min(num_users, num_items), 3)
    
    if st.button("🔄 Regenerate Sparse Data", use_container_width=True):
        # Generate a new sparse matrix based on sparsity level
        dense_matrix = np.random.randint(1, 6, size=(num_users, num_items)).astype(float)
        mask = np.random.random(size=(num_users, num_items)) < (sparsity/100)
        sparse_matrix = np.copy(dense_matrix)
        sparse_matrix[mask] = np.nan  # Use NaN to represent missing values
        st.session_state.sparse_matrix = sparse_matrix
        st.session_state.dense_matrix = dense_matrix  # Store the original dense matrix for comparison

# Initialize or use existing data
if 'sparse_matrix' not in st.session_state:
    # Generate initial sparse matrix
    dense_matrix = np.random.randint(1, 6, size=(num_users, num_items)).astype(float)
    mask = np.random.random(size=(num_users, num_items)) < (sparsity/100)
    sparse_matrix = np.copy(dense_matrix)
    sparse_matrix[mask] = np.nan  # Use NaN to represent missing values
    st.session_state.sparse_matrix = sparse_matrix
    st.session_state.dense_matrix = dense_matrix

sparse_matrix = st.session_state.sparse_matrix
dense_matrix = st.session_state.dense_matrix

# Create a copy of the sparse matrix with 0s instead of NaNs for SVD
sparse_matrix_for_svd = np.copy(sparse_matrix)
sparse_matrix_for_svd[np.isnan(sparse_matrix_for_svd)] = 0

# Perform SVD
U, sigma, VT = svd(sparse_matrix_for_svd, full_matrices=False)
Sigma = np.diag(sigma)

# Create tabs with better styling
tabs = st.tabs(["📊 Sparse Matrix", "🧩 Decomposition", "🔄 Reconstruction", "📈 Comparison"])

with tabs[0]:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create a heatmap with NaN values shown as empty/white
        fig = px.imshow(sparse_matrix, 
                        color_continuous_scale=color_scale,
                        labels=dict(x="Items", y="Users", color="Rating"))
        
        # Add text annotations only for non-NaN values
        for i in range(sparse_matrix.shape[0]):
            for j in range(sparse_matrix.shape[1]):
                if not np.isnan(sparse_matrix[i, j]):
                    fig.add_annotation(
                        x=j, y=i,
                        text=str(int(sparse_matrix[i, j])),
                        showarrow=False,
                        font=dict(color="white" if sparse_matrix[i, j] > 2.5 else "black")
                    )
        
        fig.update_layout(
            title=f'Sparse User-Item Matrix (Sparsity: {sparsity}%)',
            height=500, 
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate and display sparsity statistics
        total_cells = sparse_matrix.size
        missing_cells = np.isnan(sparse_matrix).sum()
        actual_sparsity = (missing_cells / total_cells) * 100
        
        st.markdown("### Sparsity Statistics")
        st.markdown(f"**Total cells:** {total_cells}")
        st.markdown(f"**Missing values:** {missing_cells}")
        st.markdown(f"**Actual sparsity:** {actual_sparsity:.1f}%")
        st.markdown(f"**Available data:** {100-actual_sparsity:.1f}%")
        
        st.markdown("### The Sparsity Problem")
        st.markdown("""
        In real-world recommendation systems:
        - Netflix: >98% sparsity
        - Amazon: >99.5% sparsity
        - YouTube: >99.9% sparsity
        
        SVD helps recover the missing values by identifying latent patterns in the available data.
        """)

with tabs[1]:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = px.imshow(U, text_auto='.2f', aspect="auto", color_continuous_scale=color_scale)
        fig.update_layout(title='U Matrix (Users)', height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**User-latent feature matrix**")
        st.markdown("Shows how each user relates to the underlying latent features")

    with col2:
        fig = px.imshow(Sigma, text_auto='.2f', aspect="auto", color_continuous_scale=color_scale)
        fig.update_layout(title='Σ Matrix (Weights)', height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Singular values matrix**")
        st.markdown("Represents the importance of each latent feature")

    with col3:
        fig = px.imshow(VT, text_auto='.2f', aspect="auto", color_continuous_scale=color_scale)
        fig.update_layout(title='VT Matrix (Items)', height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Item-latent feature matrix (transposed)**")
        st.markdown("Shows how each item relates to the underlying latent features")

with tabs[2]:
    # Reconstruct the matrix using the top k latent features
    k = num_latent_features
    reconstructed_matrix = np.dot(U[:, :k], np.dot(Sigma[:k, :k], VT[:k, :]))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a heatmap with NaN values shown as empty/white
        fig = px.imshow(sparse_matrix, 
                        color_continuous_scale=color_scale,
                        labels=dict(x="Items", y="Users", color="Rating"))
        
        # Add text annotations only for non-NaN values
        for i in range(sparse_matrix.shape[0]):
            for j in range(sparse_matrix.shape[1]):
                if not np.isnan(sparse_matrix[i, j]):
                    fig.add_annotation(
                        x=j, y=i,
                        text=str(int(sparse_matrix[i, j])),
                        showarrow=False,
                        font=dict(color="white" if sparse_matrix[i, j] > 2.5 else "black")
                    )
        
        fig.update_layout(
            title='Original Sparse Matrix',
            height=500, 
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.imshow(reconstructed_matrix, text_auto='.1f', 
                       color_continuous_scale=color_scale,
                       labels=dict(x="Items", y="Users", color="Rating"))
        fig.update_layout(
            title=f'Reconstructed Matrix (k={k} features)',
            height=500, 
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### How SVD Solves the Sparsity Problem
    
    1. **Dimensionality Reduction**: By using only the top latent features, SVD captures the most important patterns
    
    2. **Filling in Missing Values**: The reconstructed matrix provides predictions for all missing values
    
    3. **Noise Reduction**: Less important singular values are discarded, reducing noise in the data
    
    4. **Pattern Recognition**: SVD identifies hidden patterns even with limited data
    """)

with tabs[3]:
    # Compare the reconstructed values with the original dense matrix
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.imshow(dense_matrix, text_auto=True, 
                       color_continuous_scale=color_scale,
                       labels=dict(x="Items", y="Users", color="Rating"))
        fig.update_layout(
            title='Original Dense Matrix (Ground Truth)',
            height=500, 
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Round the reconstructed matrix for better visualization
        rounded_reconstructed = np.round(reconstructed_matrix).clip(1, 5)
        
        fig = px.imshow(rounded_reconstructed, text_auto=True, 
                       color_continuous_scale=color_scale,
                       labels=dict(x="Items", y="Users", color="Rating"))
        fig.update_layout(
            title=f'Reconstructed Matrix (Rounded)',
            height=500, 
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Calculate and display error metrics
    # Only compare cells that were originally missing
    mask = np.isnan(sparse_matrix)
    predicted_values = reconstructed_matrix[mask]
    actual_values = dense_matrix[mask]
    
    mae = np.mean(np.abs(predicted_values - actual_values))
    rmse = np.sqrt(np.mean((predicted_values - actual_values)**2))
    
    # Calculate accuracy (percentage of predictions within 0.5 of actual value)
    accuracy = np.mean(np.abs(predicted_values - actual_values) <= 0.5) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Absolute Error", f"{mae:.2f}")
    col2.metric("Root Mean Square Error", f"{rmse:.2f}")
    col3.metric("Prediction Accuracy", f"{accuracy:.1f}%")
    
    st.markdown("""
    ### Prediction Performance
    
    The metrics above show how well SVD reconstructs the missing values compared to the original data.
    
    **Key Insights:**
    
    1. **Lower MAE/RMSE is better** - indicates predictions are closer to actual values
    
    2. **Accuracy** shows the percentage of predictions within 0.5 of the actual rating
    
    3. **Trade-off**: Using more latent features typically improves accuracy but may lead to overfitting
    
    4. **Real-world applications** often use 20-100 latent features depending on the dataset size
    """)

# Add expandable explanation section
with st.expander("📚 SVD for Recommendation Systems - Detailed Explanation"):
    st.markdown("""
    ## How SVD Solves the Sparse Matrix Problem
    
    ### The Challenge of Sparsity
    
    In recommendation systems, we typically have:
    - Many users (thousands to millions)
    - Many items (thousands to millions)
    - Very few ratings per user (often <1% of items rated)
    
    This creates an extremely sparse matrix with most values missing, making it difficult to:
    1. Find similar users or items
    2. Make reliable recommendations
    3. Discover patterns in the data
    
    ### SVD Solution
    
    SVD decomposes a matrix A into three matrices: A = UΣV^T, where:
    
    - **U**: User-latent feature matrix (how each user relates to each latent feature)
    - **Σ**: Diagonal matrix with singular values (importance of each latent feature)
    - **V^T**: Item-latent feature matrix (how each item relates to each latent feature)
    
    ### Example: Movie Recommendations
    
    Consider a movie rating system:
    
    - **Users**: People who watch and rate movies
    - **Items**: Movies that can be rated
    - **Ratings**: 1-5 stars
    - **Missing Values**: Movies a user hasn't watched/rated
    
    **Latent Features** might represent concepts like:
    - Action content
    - Romance level
    - Visual effects quality
    - Humor style
    - Emotional depth
    
    Even though these features aren't explicitly labeled, SVD discovers them from patterns in the available ratings.
    
    ### Benefits in Production Systems
    
    - **Netflix**: Reduced prediction error by 10% using SVD-based approaches
    - **Amazon**: Improved recommendation relevance by up to 35%
    - **Spotify**: Uses SVD to power music recommendations with >30% higher engagement
    
    ### Practical Implementation Notes
    
    For very large matrices, specialized algorithms like:
    - Stochastic Gradient Descent (SGD)
    - Alternating Least Squares (ALS)
    - Implicit SVD
    
    are used to efficiently compute the factorization without materializing the full sparse matrix.
    """)

# Footer with cleaner styling
st.markdown("""
<div style="text-align:center; margin-top:30px; color:#888;">
Adjust parameters in the sidebar to see how SVD handles different sparsity levels
</div>
""", unsafe_allow_html=True)
