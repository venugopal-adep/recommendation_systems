import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean

# Set page config
st.set_page_config(page_title="Similarity Measures Explained", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    body {
        color: #1E1E1E;
        background-color: #F0F2F6;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #E1E5EA;
        border-radius: 4px;
        color: #1E1E1E;
        font-weight: 400;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4A90E2;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: #FFFFFF;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF;
    }
    .stRadio [data-baseweb="radio"] {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Load the datasets
@st.cache_data
def load_data():
    movies = pd.read_csv('movielens/movies.csv')
    ratings = pd.read_csv('movielens/ratings.csv')
    return movies, ratings

movies, ratings = load_data()

# Create user-item matrix
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# Title
st.title("Similarity Measures Explained")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Learn", "Explore", "Quiz"])

with tab1:
    st.header("Understanding Similarity Measures")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        Similarity measures are used in recommender systems to quantify how similar two users or items are. Here are three common measures:

        1. **Cosine Similarity**: Measures the cosine of the angle between two vectors. It ranges from -1 to 1, where 1 means exactly similar, 0 means no similarity, and -1 means exactly opposite.

        2. **Pearson Correlation**: Measures the linear correlation between two variables. It ranges from -1 to 1, where 1 is total positive correlation, 0 is no correlation, and -1 is total negative correlation.

        3. **Euclidean Distance**: Measures the straight-line distance between two points in Euclidean space. A smaller value indicates more similarity.

        These measures help in finding users with similar preferences or items with similar characteristics, which is crucial for making recommendations.
        """)
    with col2:
        st.image('movielens/image.png', caption="Similarity Measures Overview", use_column_width=True)

with tab2:
    st.header("Explore Similarity Measures")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Input elements
        concept = st.radio(
            "Select a Similarity Measure",
            ('Cosine Similarity', 'Pearson Correlation', 'Euclidean Distance')
        )

        user1_id = st.selectbox('Select User 1', user_item_matrix.index)
        user2_id = st.selectbox('Select User 2', user_item_matrix.index)

        n_movies = st.slider("Number of movies to compare", 5, 50, 20)

    user1_ratings = user_item_matrix.loc[user1_id]
    user2_ratings = user_item_matrix.loc[user2_id]

    # Function to calculate similarities
    def calculate_similarity(user1, user2, method):
        common_movies = user1.index[user1.notnull() & user2.notnull()]
        u1 = user1[common_movies]
        u2 = user2[common_movies]
        
        if method == 'Cosine Similarity':
            return cosine_similarity([u1], [u2])[0][0]
        elif method == 'Pearson Correlation':
            return pearsonr(u1, u2)[0]
        else:  # Euclidean Distance
            return euclidean(u1, u2)

    similarity = calculate_similarity(user1_ratings, user2_ratings, concept)

    with col2:
        st.write(f"**{concept}** between User {user1_id} and User {user2_id} is: {similarity:.2f}")

        if concept == 'Cosine Similarity':
            st.write("Cosine Similarity measures the cosine of the angle between two vectors. A value of 1 indicates identical preferences, while 0 indicates no similarity.")
        elif concept == 'Pearson Correlation':
            st.write("Pearson Correlation measures the linear correlation between two sets of data. A value of 1 indicates perfect positive correlation, -1 indicates perfect negative correlation, and 0 indicates no correlation.")
        else:
            st.write("Euclidean Distance measures the straight-line distance between two points in space. A smaller value indicates more similar preferences.")

    # Get common rated movies
    common_movies = user1_ratings.index[user1_ratings.notnull() & user2_ratings.notnull()]
    common_movies = common_movies[:n_movies]  # Limit to selected number of movies

    ratings_data = []
    for movie in common_movies:
        movie_title = movies.loc[movies['movieId'] == movie, 'title'].values[0]
        ratings_data.append({
            'Movie': movie_title,
            'User 1 Rating': user1_ratings[movie],
            'User 2 Rating': user2_ratings[movie]
        })

    ratings_df = pd.DataFrame(ratings_data)

    # Interactive visualization
    st.write("### Comparison of User Ratings")
    fig = px.scatter(ratings_df, x='User 1 Rating', y='User 2 Rating', 
                     text='Movie', title=f'{concept}: User {user1_id} vs User {user2_id}',
                     labels={'User 1 Rating': f'User {user1_id} Rating', 'User 2 Rating': f'User {user2_id} Rating'},
                     color='Movie', hover_data=['Movie'])

    fig.update_traces(textposition='top center', marker=dict(size=10))
    fig.update_layout(
        height=600, 
        xaxis=dict(range=[0, 5.5]), 
        yaxis=dict(range=[0, 5.5]),
        xaxis_title=f"User {user1_id} Rating",
        yaxis_title=f"User {user2_id} Rating",
        showlegend=False
    )

    # Add reference line
    fig.add_shape(type="line", line=dict(dash="dash", color="gray"),
                  x0=0, y0=0, x1=5.5, y1=5.5)

    st.plotly_chart(fig, use_container_width=True)

    # Interactive movie comparison
    st.write("### Movie-by-Movie Comparison")
    selected_movie = st.selectbox("Select a movie to compare ratings", ratings_df['Movie'])
    movie_data = ratings_df[ratings_df['Movie'] == selected_movie].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Movie", selected_movie)
    col2.metric(f"User {user1_id} Rating", movie_data['User 1 Rating'])
    col3.metric(f"User {user2_id} Rating", movie_data['User 2 Rating'])

    # Explanation of the similarity for this movie
    rating_diff = abs(movie_data['User 1 Rating'] - movie_data['User 2 Rating'])
    if rating_diff < 1:
        st.write("These users have very similar opinions on this movie.")
    elif rating_diff < 2:
        st.write("These users have somewhat different opinions on this movie.")
    else:
        st.write("These users have very different opinions on this movie.")

    # Explanation of the plot
    st.write("""
    **Understanding the Plot:**
    - Each point represents a movie that both users have rated.
    - The x-axis shows ratings from User 1, while the y-axis shows ratings from User 2.
    - Points closer to the dashed line indicate movies where both users gave similar ratings.
    - Points far from the line show movies where users disagreed.
    - The color of each point represents a unique movie (hover to see the title).

    **Interpreting Similarity:**
    - For Cosine Similarity and Pearson Correlation: More points close to the line indicate higher similarity.
    - For Euclidean Distance: More spread out points indicate larger distance (less similarity).
    """)

with tab3:
    st.header("Test Your Knowledge")
    
    st.subheader("Question 1: What does a Cosine Similarity of 1 indicate?")
    q1_options = ["Users have opposite preferences", "Users have no similarity", "Users have identical preferences", "The calculation failed"]
    q1_answer = st.radio("Select your answer:", q1_options, key="q1")
    if st.button("Show Answer", key="b1"):
        st.write("The correct answer is: Users have identical preferences.")
        st.write("Explanation: A Cosine Similarity of 1 means the angle between the two vectors is 0°, indicating that the users have exactly the same preferences.")

    st.subheader("Question 2: What is the range of Pearson Correlation?")
    q2_options = ["0 to 1", "-1 to 1", "0 to infinity", "-infinity to infinity"]
    q2_answer = st.radio("Select your answer:", q2_options, key="q2")
    if st.button("Show Answer", key="b2"):
        st.write("The correct answer is: -1 to 1.")
        st.write("Explanation: Pearson Correlation ranges from -1 (perfect negative correlation) to 1 (perfect positive correlation), with 0 indicating no correlation.")

    st.subheader("Question 3: For Euclidean Distance, what does a smaller value indicate?")
    q3_options = ["More dissimilar preferences", "More similar preferences", "No relationship between preferences", "Perfect negative correlation"]
    q3_answer = st.radio("Select your answer:", q3_options, key="q3")
    if st.button("Show Answer", key="b3"):
        st.write("The correct answer is: More similar preferences.")
        st.write("Explanation: In Euclidean Distance, a smaller value indicates that the two points (representing user preferences) are closer together in the feature space, meaning the users have more similar preferences.")
