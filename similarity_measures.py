import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean

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

# Title and description
st.title("Similarity Measures Explained")
st.write("Explore and understand different similarity measures using the movie ratings dataset.")

# Sidebar options
concept = st.sidebar.radio(
    "Select a Similarity Measure",
    ('Cosine Similarity', 'Pearson Correlation', 'Euclidean Distance')
)

st.sidebar.markdown("### Selected Measure: " + concept)

# Select two users for demonstration
user1_id = st.sidebar.selectbox('Select User 1', user_item_matrix.index)
user2_id = st.sidebar.selectbox('Select User 2', user_item_matrix.index)

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

# Display image for better understanding
st.image('movielens/image.png', caption="Similarity Measures Overview", use_column_width=True)
