import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, KNNBasic, CoClustering
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px

# Load data
@st.cache_data()
def load_data():
    movies = pd.read_csv('movies.csv')
    ratings = pd.read_csv('ratings.csv')
    return movies, ratings

movies, ratings = load_data()

# Context-based Filtering
@st.cache_data()
def context_based_recommender(movie_title):
    # Using TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    movies['description'] = movies['title'] + ' ' + movies['genres']
    tfidf_matrix = tfidf.fit_transform(movies['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get index of the movie that matches the title
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

    idx = indices[movie_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get the scores of the 10 most similar movies
    movie_indices = [i[0] for i in sim_scores]
    similarity_scores = [round(i[1] * 100, 2) for i in sim_scores]  # Convert to percentage

    recommendations = movies.iloc[movie_indices]
    recommendations['similarity_score'] = similarity_scores

    # Sort recommendations by similarity score in descending order
    recommendations = recommendations.sort_values('similarity_score', ascending=False)

    return recommendations[['title', 'genres', 'similarity_score']]

# Collaborative Filtering
@st.cache_data()
def collaborative_filtering(user_id, algo_type):
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    if algo_type == 'SVD':
        model = SVD(n_factors=150, n_epochs=30, lr_all=0.01, reg_all=0.1)
    elif algo_type == 'KNNBasic':
        model = KNNBasic(k=30, sim_options={'user_based': True})
    elif algo_type == 'CoClustering':
        model = CoClustering(n_cltr_u=30, n_cltr_i=30, n_epochs=30)

    trainset = data.build_full_trainset()
    model.fit(trainset)

    # Get top 10 movie recommendations for the user
    user_ratings = ratings[ratings['userId'] == user_id]
    user_ratings = user_ratings.merge(movies[['movieId', 'title']], on='movieId', how='left')
    user_ratings = user_ratings[['userId', 'movieId', 'title', 'rating']]

    recommendations = []
    for movieId in movies['movieId']:
        if movieId not in user_ratings['movieId'].values:
            predicted_rating = model.predict(user_id, movieId).est
            recommendations.append((movieId, predicted_rating))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    recommendations = recommendations[:10]  # Get top 10 recommendations

    movie_ids = [r[0] for r in recommendations]
    predicted_ratings = [round(r[1], 2) for r in recommendations]

    recommendations_df = movies[movies['movieId'].isin(movie_ids)]
    recommendations_df['predicted_rating'] = predicted_ratings

    return recommendations_df[['title', 'genres', 'predicted_rating']], model

# Visualization functions
def plot_svd_factors(model):
    fig = px.scatter_3d(x=model.pu[:, 0], y=model.pu[:, 1], z=model.pu[:, 2],
                        labels={'x': 'Factor 1', 'y': 'Factor 2', 'z': 'Factor 3'},
                        title='SVD Factors')
    fig.update_layout(scene=dict(xaxis_title='Factor 1', yaxis_title='Factor 2', zaxis_title='Factor 3'))
    st.plotly_chart(fig)

def plot_knn_similarity(model, user_id):
    user_inner_id = model.trainset.to_inner_uid(user_id)
    user_neighbors = model.get_neighbors(user_inner_id, k=10)
    user_neighbors = [model.trainset.to_raw_uid(inner_id) for inner_id in user_neighbors]

    user_similarities = pd.DataFrame({'userId': user_neighbors})
    user_similarities = user_similarities.merge(ratings, on='userId', how='inner')
    user_similarities = user_similarities.merge(movies[['movieId', 'title']], on='movieId', how='inner')

    plt.figure(figsize=(8, 6))
    plt.hist(user_similarities['rating'], bins=20)
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.title(f'Rating Distribution of Top 10 Similar Users to User {user_id}')
    st.pyplot(plt)

def plot_coclustering_clusters(model):
    user_labels = [model.user_labels_[model.trainset.to_inner_uid(uid)] for uid in model.trainset.all_users()]
    item_labels = [model.item_labels_[model.trainset.to_inner_iid(iid)] for iid in model.trainset.all_items()]

    df = pd.DataFrame({'User Cluster': user_labels, 'Item Cluster': item_labels})

    fig = px.scatter(df, x='User Cluster', y='Item Cluster', title='Co-Clustering Clusters')
    st.plotly_chart(fig)

# Streamlit interface
def main():
    st.title('Movie Recommendation System')

    # Sidebar
    recommendation_type = st.sidebar.selectbox('Select Recommendation Type', ('Content-based', 'Collaborative Filtering'))
    
    if recommendation_type == 'Content-based':
        movie_list = movies['title'].tolist()
        selected_movie = st.sidebar.selectbox('Select a movie', movie_list)
        recommend_button = st.sidebar.button('Recommend')
        
        if recommend_button:
            st.subheader("Understanding Content-based Recommendation")
            st.write("""
            This recommendation approach considers the descriptions and genres of movies. 
            It calculates how similar words appear in the descriptions (TF-IDF) and then determines 
            the similarity between movies based on these descriptions.
            """)

            with st.spinner('Calculating Recommendations...'):
                recommendations = context_based_recommender(selected_movie)
                st.write('Recommendations based on similar content:')
                st.write(recommendations)

    elif recommendation_type == 'Collaborative Filtering':
        algo_type = st.sidebar.selectbox('Select Algorithm', ('SVD', 'KNNBasic', 'CoClustering'))
        user_id = st.sidebar.number_input('Enter User ID', min_value=1, value=1, step=1)
        recommend_button = st.sidebar.button('Recommend')
        
        if recommend_button:
            st.subheader("Understanding Collaborative Filtering")
            st.write("""
            Collaborative filtering predicts what a user will like based on what similar users liked. 
            It doesn't need to know anything about the movies themselves (like genre or director).
            """)

            with st.spinner('Generating Collaborative Filtering Recommendations...'):
                recommendations, model = collaborative_filtering(user_id, algo_type)
                st.write(f'Top 10 Recommendations for User {user_id} using {algo_type}:')
                st.write(recommendations)

                if algo_type == 'SVD':
                    st.subheader('SVD Factor Visualization')
                    st.write('This visualization shows the latent factors learned by the SVD algorithm. Each point represents a user or item in the latent space.')
                    plot_svd_factors(model)
                elif algo_type == 'KNNBasic':
                    st.subheader('User Similarity vs Rating Visualization')
                    st.write('This visualization shows the relationship between user similarity and movie ratings. It helps understand how similar users influence the recommendations.')
                    plot_knn_similarity(model, user_id)
                elif algo_type == 'CoClustering':
                    st.subheader('Co-Clustering Clusters Visualization')
                    st.write('This visualization shows the user and item clusters learned by the Co-Clustering algorithm. Each point represents a user or item cluster.')
                    plot_coclustering_clusters(model)

if __name__ == '__main__':
    main()