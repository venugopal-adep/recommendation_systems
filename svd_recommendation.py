import streamlit as st
import numpy as np
import plotly.express as px
from scipy.linalg import svd

st.title("Matrix Factorization (SVD) Explained")

st.markdown(r"""
**Matrix Factorization** using Singular Value Decomposition (SVD) is a powerful technique used in recommendation systems to deal with sparsity and scalability issues. It decomposes the original sparse matrix into low-dimensional matrices with latent features, helping us understand user preferences and item characteristics.

### Key Concepts:
- **Sparsity**: Many real-world datasets are sparse, meaning most entries are zero.
- **Scalability**: Handling large datasets efficiently.
- **Latent Features**: Hidden factors that can explain observed interactions between users and items.
- **Singular Value Decomposition (SVD)**: A mathematical technique to factorize a matrix into three matrices: \( A = U \Sigma V^T \).

Where:
- \( U \) is the user-latent feature matrix.
- \( \Sigma \) is the diagonal matrix containing singular values.
- \( V^T \) is the transpose of the item-latent feature matrix.
""")

# Sidebar controls
st.sidebar.subheader("Controls")
num_users = st.sidebar.slider("Number of Users", 3, 10, 5)
num_items = st.sidebar.slider("Number of Items", 3, 10, 5)
num_latent_features = st.sidebar.slider("Number of Latent Features", 2, min(num_users, num_items), 2)
regenerate_data = st.sidebar.button("Regenerate Data")

# Initialize or regenerate data
if regenerate_data or 'user_item_matrix' not in st.session_state:
    np.random.seed(42)
    st.session_state.user_item_matrix = np.random.randint(0, 6, size=(num_users, num_items))

user_item_matrix = st.session_state.user_item_matrix

# Perform SVD
U, sigma, VT = svd(user_item_matrix, full_matrices=False)
Sigma = np.diag(sigma)

# Display the user-item matrix as a heatmap
st.subheader("User-Item Matrix")
fig_user_item_heatmap = px.imshow(user_item_matrix, text_auto=True, aspect="auto", color_continuous_scale='Blues')
fig_user_item_heatmap.update_layout(
    title='User-Item Matrix',
    xaxis_title='Items',
    yaxis_title='Users'
)
st.plotly_chart(fig_user_item_heatmap, use_container_width=True)

# Display U, Sigma, and VT matrices
st.subheader("Decomposed Matrices")

# Display U matrix
st.markdown("**U Matrix (User-Latent Features):**")
fig_U = px.imshow(U, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
fig_U.update_layout(
    title='U Matrix',
    xaxis_title='Latent Features',
    yaxis_title='Users'
)
st.plotly_chart(fig_U, use_container_width=True)

# Display Sigma matrix
st.markdown("**Sigma Matrix (Singular Values):**")
fig_Sigma = px.imshow(Sigma, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
fig_Sigma.update_layout(
    title='Sigma Matrix',
    xaxis_title='Latent Features',
    yaxis_title='Latent Features'
)
st.plotly_chart(fig_Sigma, use_container_width=True)

# Display VT matrix
st.markdown("**VT Matrix (Item-Latent Features):**")
fig_VT = px.imshow(VT, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
fig_VT.update_layout(
    title='VT Matrix',
    xaxis_title='Items',
    yaxis_title='Latent Features'
)
st.plotly_chart(fig_VT, use_container_width=True)

# Example: Reconstructing the original matrix
st.subheader("Reconstructed Matrix Example")
k = num_latent_features
reconstructed_matrix = np.dot(U[:, :k], np.dot(Sigma[:k, :k], VT[:k, :]))

# Display original and reconstructed matrices side by side
st.markdown(f"Using top {k} latent features to reconstruct the original matrix:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Original User-Item Matrix**")
    fig_original = px.imshow(user_item_matrix, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
    fig_original.update_layout(
        title='Original User-Item Matrix',
        xaxis_title='Items',
        yaxis_title='Users'
    )
    st.plotly_chart(fig_original, use_container_width=True)

with col2:
    st.markdown("**Reconstructed User-Item Matrix**")
    fig_reconstructed = px.imshow(reconstructed_matrix, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
    fig_reconstructed.update_layout(
        title='Reconstructed User-Item Matrix',
        xaxis_title='Items',
        yaxis_title='Users'
    )
    st.plotly_chart(fig_reconstructed, use_container_width=True)

st.markdown("""
### Explanation:
- **User-Item Matrix**: Represents interactions between users and items.
- **U Matrix**: Shows how much each user aligns with the latent features.
- **Sigma Matrix**: Contains singular values, representing the importance of each latent feature.
- **VT Matrix**: Shows how much each item aligns with the latent features.
- **Reconstructed Matrix**: An approximation of the original user-item matrix using a reduced number of latent features.

### Example:
Imagine a movie recommendation system:
- Users: People watching movies.
- Items: Movies available.
- Latent Features: Genres, actors, directors, etc.

Matrix Factorization helps us understand hidden patterns in user preferences and item characteristics, improving recommendations by predicting how users would rate unseen items.
""")

st.markdown("""
### Try adjusting the number of users, items, and latent features using the controls in the sidebar to see how the decomposition and reconstruction change.
""")
