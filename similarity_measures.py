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
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px;
        color: #31333F;
        font-weight: 400;
    }
    .stTabs [aria-selected="true"] {
        background-color: #31333F;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Load the datasets
@st.cache_data
def load_data():
    movies = pd.read_csv('movielens/movies.csv')
    ratings = pd.read_csv('movielens/ratings.csv')
    tags = pd.read_csv('movielens/tags.csv')
    links = pd.read_csv('movielens/links.csv')
    return movies, ratings, tags, links

movies, ratings, tags, links = load_data()

# Create user-item matrix
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# Title
st.title("Similarity Measures Explained")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Learn", "Explore", "Quiz"])

with tab1:
    st.header("Understanding Similarity Measures")
    st.write("""
    Similarity measures are used in recommender systems to quantify how similar two users or items are. Here are three common measures:

    1. **Cosine Similarity**: Measures the cosine of the angle between two vectors. It ranges from -1 to 1, where 1 means exactly similar, 0 means no similarity, and -1 means exactly opposite.

    2. **Pearson Correlation**: Measures the linear correlation between two variables. It ranges from -1 to 1, where 1 is total positive correlation, 0 is no correlation, and -1 is total negative correlation.

    3. **Euclidean Distance**: Measures the straight-line distance between two points in Euclidean space. A smaller value indicates more similarity.

    These measures help in finding users with similar preferences or items with similar characteristics, which is crucial for making recommendations.
    """)

    st.image('movielens/image.png', caption="Similarity Measures Overview", use_column_width=True)

with tab2:
    st.header("Explore Similarity Measures")
    
    # Sidebar options
    concept = st.radio(
        "Select a Similarity Measure",
        ('Cosine Similarity', 'Pearson Correlation', 'Euclidean Distance')
    )

    # Select two users for demonstration
    user1_id = st.selectbox('Select User 1', user_item_matrix.index)
    user2_id = st.selectbox('Select User 2', user_item_matrix.index)

    user1_ratings = user_item_matrix.loc[user1_id].to_dict()
    user2_ratings = user_item_matrix.loc[user2_id].to_dict()

    # Function to calculate Cosine Similarity
    def calculate_cosine_similarity(user1, user2):
        common_movies = set(user1.keys()).intersection(set(user2.keys()))
        if not common_movies:
            return 0
        
        user1_vector = [user1[movie] for movie in common_movies]
        user2_vector = [user2[movie] for movie in common_movies]
        
        return cosine_similarity([user1_vector], [user2_vector])[0][0]

    # Function to calculate Pearson Correlation
    def calculate_pearson_correlation(user1, user2):
        common_movies = set(user1.keys()).intersection(set(user2.keys()))
        if not common_movies:
            return 0
        
        user1_vector = [user1[movie] for movie in common_movies]
        user2_vector = [user2[movie] for movie in common_movies]
        
        return pearsonr(user1_vector, user2_vector)[0]

    # Function to calculate Euclidean Distance
    def calculate_euclidean_distance(user1, user2):
        common_movies = set(user1.keys()).intersection(set(user2.keys()))
        if not common_movies:
            return float('inf')
        
        user1_vector = [user1[movie] for movie in common_movies]
        user2_vector = [user2[movie] for movie in common_movies]
        
        return euclidean(user1_vector, user2_vector)

    # Calculate similarity/distance based on selected concept
    if concept == 'Cosine Similarity':
        similarity = calculate_cosine_similarity(user1_ratings, user2_ratings)
        st.write(f"**Cosine Similarity** between User {user1_id} and User {user2_id} is: {similarity:.2f}")
        st.write("Cosine Similarity measures the cosine of the angle between two vectors. A value of 1 indicates that the users have identical preferences, while a value of 0 indicates no similarity.")
        metric = "Cosine Similarity"
    elif concept == 'Pearson Correlation':
        correlation = calculate_pearson_correlation(user1_ratings, user2_ratings)
        st.write(f"**Pearson Correlation** between User {user1_id} and User {user2_id} is: {correlation:.2f}")
        st.write("Pearson Correlation measures the linear correlation between two sets of data. A value of 1 indicates a perfect positive correlation, -1 indicates a perfect negative correlation, and 0 indicates no correlation.")
        metric = "Pearson Correlation"
    elif concept == 'Euclidean Distance':
        distance = calculate_euclidean_distance(user1_ratings, user2_ratings)
        st.write(f"**Euclidean Distance** between User {user1_id} and User {user2_id} is: {distance:.2f}")
        st.write("Euclidean Distance measures the straight-line distance between two points in Euclidean space. A smaller value indicates more similar preferences.")
        metric = "Euclidean Distance"

    # Display the sparse user-item matrix visualization
    st.write("### User-Item Matrix (Sparse Matrix)")
    sparse_matrix = user_item_matrix.loc[[user1_id, user2_id]]
    fig = px.imshow(sparse_matrix, aspect='auto', color_continuous_scale='Blues', labels={'color':'Rating'})
    st.plotly_chart(fig)

    # Display ratings in visual format
    common_movies = set(user1_ratings.keys()).intersection(set(user2_ratings.keys()))
    ratings_data = [(movies[movies['movieId'] == movie]['title'].values[0], user1_ratings[movie], user2_ratings[movie]) for movie in common_movies]
    ratings_df = pd.DataFrame(ratings_data, columns=['Movie', 'User 1 Rating', 'User 2 Rating'])

    # Interactive visualization for Cosine Similarity and Pearson Correlation
    if concept in ['Cosine Similarity', 'Pearson Correlation']:
        st.write("### Scatter Plot of Common Movie Ratings")
        fig = px.scatter(ratings_df, x='User 1 Rating', y='User 2 Rating', text='Movie', title=f'{metric} Scatter Plot', 
                         labels={'User 1 Rating': 'User 1 Rating', 'User 2 Rating': 'User 2 Rating'},
                         size_max=10, opacity=0.7)
        fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_layout(autosize=False, width=800, height=600, hovermode='closest')
        st.plotly_chart(fig)

    # Interactive visualization for Euclidean Distance
    elif concept == 'Euclidean Distance':
        fig = px.line(ratings_df, x='Movie', y=['User 1 Rating', 'User 2 Rating'], title=f'{metric} Line Plot',
                      labels={'value': 'Rating', 'variable': 'User'}, markers=True)
        fig.update_layout(autosize=False, width=800, height=600)
        st.plotly_chart(fig)

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
