import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean

# Set page config
st.set_page_config(page_title="Similarity Measures Visualizer", layout="wide")

# Custom CSS for clean, compact UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #3498db;
        --secondary: #f8f9fa;
        --text: #2c3e50;
        --success: #2ecc71;
        --warning: #f39c12;
        --danger: #e74c3c;
    }
    
    /* Typography */
    body {
        color: var(--text);
        background-color: var(--secondary);
    }
    
    h1 {
        color: var(--primary);
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--primary);
        font-size: 1.4rem;
        margin-top: 1rem;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 0.8rem;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 6px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    /* Metric styling */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        border-left: 4px solid var(--primary);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--primary);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    /* Compact elements */
    .stRadio > div {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    
    .stRadio [data-testid="stMarkdownContainer"] > p {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Load the datasets with caching
@st.cache_data
def load_data():
    movies = pd.read_csv('movielens/movies.csv')
    ratings = pd.read_csv('movielens/ratings.csv')
    return movies, ratings

movies, ratings = load_data()

# Create user-item matrix
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# App header
st.title("Interactive Similarity Measures Visualizer")
st.markdown('<p style="margin-top:-10px; color:#6c757d;">Developed by: Venugopal Adep</p>', unsafe_allow_html=True)

# Main content
st.markdown('<div class="card">', unsafe_allow_html=True)

# Select users and similarity measure
col1, col2 = st.columns([1, 1])

with col1:
    user1_id = st.selectbox('Select User 1', user_item_matrix.index, index=0)
    user2_id = st.selectbox('Select User 2', user_item_matrix.index, index=1)

with col2:
    concept = st.radio(
        "Select Similarity Measure",
        ('Cosine Similarity', 'Pearson Correlation', 'Euclidean Distance'),
        horizontal=True
    )
    n_movies = st.slider("Number of movies to compare", 5, 30, 15)

# Get user ratings
user1_ratings = user_item_matrix.loc[user1_id]
user2_ratings = user_item_matrix.loc[user2_id]

# Get common rated movies for visualization
common_rated_indices = (user1_ratings > 0) & (user2_ratings > 0)
common_movies = user1_ratings.index[common_rated_indices]
common_movies = common_movies[:n_movies]

ratings_data = []
for movie in common_movies:
    movie_title = movies.loc[movies['movieId'] == movie, 'title'].values[0]
    ratings_data.append({
        'Movie': movie_title,
        'User 1 Rating': user1_ratings[movie],
        'User 2 Rating': user2_ratings[movie]
    })

ratings_df = pd.DataFrame(ratings_data)

# Calculate similarity
def calculate_similarity(user1, user2, method):
    # Extract only common rated movies (non-zero ratings)
    common_indices = (user1 > 0) & (user2 > 0)
    u1 = user1[common_indices]
    u2 = user2[common_indices]
    
    if len(u1) == 0:
        return 0  # No common movies
    
    if method == 'Cosine Similarity':
        return cosine_similarity([u1], [u2])[0][0]
    elif method == 'Pearson Correlation':
        if len(u1) < 2:  # Need at least 2 points for correlation
            return 0
        return pearsonr(u1, u2)[0]
    else:  # Euclidean Distance
        return euclidean(u1, u2)

similarity = calculate_similarity(user1_ratings, user2_ratings, concept)

# Display similarity score
st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card" style="width: 300px;">', unsafe_allow_html=True)
st.markdown(f'<div class="metric-value">{similarity:.2f}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-label">{concept}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Visual explanation of the similarity measure
st.markdown("## Visual Explanation")

col1, col2 = st.columns([3, 2])

with col1:
    # Create scatter plot
    fig = px.scatter(ratings_df, x='User 1 Rating', y='User 2 Rating', 
                    text='Movie', title=f'Rating Comparison: User {user1_id} vs User {user2_id}',
                    color='User 1 Rating', color_continuous_scale='Viridis',
                    hover_data=['Movie'])

    fig.update_traces(textposition='top center', marker=dict(size=12, opacity=0.8))
    fig.update_layout(
        height=450, 
        xaxis=dict(range=[0, 5.5], title=f"User {user1_id} Rating", gridcolor='#f0f0f0'), 
        yaxis=dict(range=[0, 5.5], title=f"User {user2_id} Rating", gridcolor='#f0f0f0'),
        plot_bgcolor='white',
        showlegend=False,
    )

    # Add reference line
    fig.add_shape(type="line", line=dict(dash="dash", color="gray", width=1),
                x0=0, y0=0, x1=5.5, y1=5.5)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### What This Means")
    
    if concept == 'Cosine Similarity':
        st.markdown("""
        **Cosine Similarity** measures the angle between two vectors, ignoring their magnitude.
        
        - **Range**: -1 to 1
        - **Interpretation**: 
          - 1 = Users have identical preferences
          - 0 = No similarity
          - -1 = Opposite preferences
        
        **In the plot**: Points clustered along the diagonal line indicate similar ratings patterns, regardless of the actual rating values.
        """)
        
        # Visual representation of cosine similarity
        st.markdown("#### Vector Representation")
        
        # Create a simple vector visualization
        u1_vec = ratings_df['User 1 Rating'].values[:5]  # First 5 movies
        u2_vec = ratings_df['User 2 Rating'].values[:5]  # First 5 movies
        
        fig = go.Figure()
        
        # Add vectors
        fig.add_trace(go.Scatter(x=[0, u1_vec[0]], y=[0, u1_vec[1]], 
                                mode='lines+markers', name='User 1',
                                line=dict(color='blue', width=3)))
        
        fig.add_trace(go.Scatter(x=[0, u2_vec[0]], y=[0, u2_vec[1]], 
                                mode='lines+markers', name='User 2',
                                line=dict(color='red', width=3)))
        
        fig.update_layout(
            height=200,
            xaxis=dict(range=[0, 5.5], title="Movie 1 Rating"),
            yaxis=dict(range=[0, 5.5], title="Movie 2 Rating"),
            plot_bgcolor='white',
            title="Vector Angle Visualization (First 2 Movies)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif concept == 'Pearson Correlation':
        st.markdown("""
        **Pearson Correlation** measures the linear relationship between two sets of ratings.
        
        - **Range**: -1 to 1
        - **Interpretation**: 
          - 1 = Perfect positive correlation
          - 0 = No correlation
          - -1 = Perfect negative correlation
        
        **In the plot**: Points forming a straight line indicate strong correlation. Pearson accounts for different rating scales (e.g., if one user rates everything higher).
        """)
        
        # Show trend line
        x = ratings_df['User 1 Rating']
        y = ratings_df['User 2 Rating']
        
        fig = px.scatter(ratings_df, x='User 1 Rating', y='User 2 Rating')
        fig.add_trace(go.Scatter(x=x, y=np.poly1d(np.polyfit(x, y, 1))(x),
                                mode='lines', name='Trend Line',
                                line=dict(color='red', width=2, dash='dash')))
        
        fig.update_layout(
            height=200,
            xaxis=dict(range=[0, 5.5], title="User 1 Rating"),
            yaxis=dict(range=[0, 5.5], title="User 2 Rating"),
            plot_bgcolor='white',
            title="Correlation Trend Line"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Euclidean Distance
        st.markdown("""
        **Euclidean Distance** measures the straight-line distance between rating points.
        
        - **Range**: 0 to ∞
        - **Interpretation**: 
          - 0 = Identical preferences
          - Larger values = More different preferences
        
        **In the plot**: Points closer to each other in the space indicate more similar ratings. This measure is sensitive to the actual rating values.
        """)
        
        # Show distance visualization
        st.markdown("#### Distance Visualization")
        
        # Create a simple distance visualization for first two points
        fig = go.Figure()
        
        # Add points
        fig.add_trace(go.Scatter(x=[ratings_df['User 1 Rating'][0]], 
                                y=[ratings_df['User 2 Rating'][0]],
                                mode='markers', name='Movie 1',
                                marker=dict(size=12, color='blue')))
        
        fig.add_trace(go.Scatter(x=[ratings_df['User 1 Rating'][1]], 
                                y=[ratings_df['User 2 Rating'][1]],
                                mode='markers', name='Movie 2',
                                marker=dict(size=12, color='red')))
        
        # Add line between points to show distance
        fig.add_shape(type="line", 
                    x0=ratings_df['User 1 Rating'][0], y0=ratings_df['User 2 Rating'][0],
                    x1=ratings_df['User 1 Rating'][1], y1=ratings_df['User 2 Rating'][1],
                    line=dict(color="black", width=2, dash="dash"))
        
        fig.update_layout(
            height=200,
            xaxis=dict(range=[0, 5.5], title="User 1 Rating"),
            yaxis=dict(range=[0, 5.5], title="User 2 Rating"),
            plot_bgcolor='white',
            title="Distance Between Points (First 2 Movies)"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Movie comparison table
st.markdown("## Movie-by-Movie Comparison")

# Create a table with the ratings
st.dataframe(
    ratings_df.style.background_gradient(
        cmap='RdYlGn', subset=['User 1 Rating', 'User 2 Rating'], vmin=1, vmax=5
    ).format({'User 1 Rating': '{:.1f}', 'User 2 Rating': '{:.1f}'}),
    use_container_width=True,
    height=300
)

# Practical interpretation
st.markdown("## Practical Interpretation")

if concept == 'Cosine Similarity':
    if similarity > 0.8:
        st.success("These users have very similar preferences. They would likely enjoy similar movies.")
    elif similarity > 0.5:
        st.info("These users have somewhat similar preferences. They might enjoy some of the same movies.")
    else:
        st.warning("These users have different preferences. They would likely enjoy different movies.")
elif concept == 'Pearson Correlation':
    if similarity > 0.7:
        st.success("These users' ratings are strongly correlated. They tend to rate movies similarly.")
    elif similarity > 0.3:
        st.info("These users' ratings are moderately correlated. They sometimes rate movies similarly.")
    elif similarity > -0.3:
        st.warning("These users' ratings show little correlation. They rate movies independently.")
    else:
        st.error("These users' ratings are negatively correlated. When one rates a movie highly, the other tends to rate it poorly.")
else:  # Euclidean Distance
    if similarity < 5:
        st.success("These users are very close in preference space. They would likely enjoy similar movies.")
    elif similarity < 10:
        st.info("These users are moderately close in preference space. They might enjoy some of the same movies.")
    else:
        st.warning("These users are far apart in preference space. They would likely enjoy different movies.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:15px; color:#6c757d; font-size:0.8em">
    © 2025 Similarity Measures Visualizer | Last updated: Saturday, March 01, 2025, 3:05 PM IST
</div>
""", unsafe_allow_html=True)
