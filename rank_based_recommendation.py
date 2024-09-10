import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, KNNBasic, CoClustering
import matplotlib.pyplot as plt
import plotly.express as px

# Custom CSS for full width and light theme
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .stApp {
            background-color: #F0F2F6;
            color: #1E1E1E;
        }
        .stSelectbox [data-baseweb="select"] {
            background-color: white;
        }
        .stSelectbox [data-baseweb="select"] > div {
            color: #1E1E1E;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #E0E0E0;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            padding-left: 20px;
            padding-right: 20px;
            font-weight: bold;
            color: #1E1E1E;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4A4A4A;
            color: white;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        h1, h2, h3 {
            color: #2C3E50;
        }
        .stDataFrame {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data()
def load_data():
    movies = pd.read_csv('movielens/movies.csv')
    ratings = pd.read_csv('movielens/ratings.csv')
    return movies, ratings

movies, ratings = load_data()

# Context-based Filtering
@st.cache_data()
def context_based_recommender(movie_title):
    tfidf = TfidfVectorizer(stop_words='english')
    movies['description'] = movies['title'] + ' ' + movies['genres']
    tfidf_matrix = tfidf.fit_transform(movies['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
    idx = indices[movie_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    similarity_scores = [round(i[1] * 100, 2) for i in sim_scores]

    recommendations = movies.iloc[movie_indices]
    recommendations['similarity_score'] = similarity_scores
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
    else:
        model = CoClustering(n_cltr_u=30, n_cltr_i=30, n_epochs=30)

    trainset = data.build_full_trainset()
    model.fit(trainset)

    user_ratings = ratings[ratings['userId'] == user_id]
    user_ratings = user_ratings.merge(movies[['movieId', 'title']], on='movieId', how='left')
    user_ratings = user_ratings[['userId', 'movieId', 'title', 'rating']]

    recommendations = []
    for movieId in movies['movieId']:
        if movieId not in user_ratings['movieId'].values:
            predicted_rating = model.predict(user_id, movieId).est
            recommendations.append((movieId, predicted_rating))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]

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
    st.plotly_chart(fig, use_container_width=True)

def plot_knn_similarity(model, user_id):
    user_inner_id = model.trainset.to_inner_uid(user_id)
    user_neighbors = model.get_neighbors(user_inner_id, k=10)
    user_neighbors = [model.trainset.to_raw_uid(inner_id) for inner_id in user_neighbors]

    user_similarities = pd.DataFrame({'userId': user_neighbors})
    user_similarities = user_similarities.merge(ratings, on='userId', how='inner')
    user_similarities = user_similarities.merge(movies[['movieId', 'title']], on='movieId', how='inner')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(user_similarities['rating'], bins=20, color='#4CAF50')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title(f'Rating Distribution of Top 10 Similar Users to User {user_id}')
    st.pyplot(fig)

def plot_coclustering_clusters(model):
    n_users = len(model.trainset.all_users())
    n_items = len(model.trainset.all_items())
    n_user_clusters = model.n_cltr_u
    n_item_clusters = model.n_cltr_i

    user_clusters = [model.user_clusters_[model.trainset.to_inner_uid(uid)] for uid in model.trainset.all_users()]
    item_clusters = [model.item_clusters_[model.trainset.to_inner_iid(iid)] for iid in model.trainset.all_items()]

    user_cluster_counts = pd.Series(user_clusters).value_counts().sort_index()
    item_cluster_counts = pd.Series(item_clusters).value_counts().sort_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.bar(user_cluster_counts.index, user_cluster_counts.values)
    ax1.set_title('User Cluster Distribution')
    ax1.set_xlabel('User Cluster')
    ax1.set_ylabel('Number of Users')

    ax2.bar(item_cluster_counts.index, item_cluster_counts.values)
    ax2.set_title('Item Cluster Distribution')
    ax2.set_xlabel('Item Cluster')
    ax2.set_ylabel('Number of Items')

    plt.tight_layout()
    st.pyplot(fig)

    st.write(f"Number of users: {n_users}")
    st.write(f"Number of items: {n_items}")
    st.write(f"Number of user clusters: {n_user_clusters}")
    st.write(f"Number of item clusters: {n_item_clusters}")

# Streamlit interface
def main():
    st.title('🎬 Movie Recommendation System')

    tab1, tab2, tab3 = st.tabs(["🧠 Learn", "🔍 Explore", "🎯 Quiz"])

    with tab1:
        st.header("Understanding Movie Recommendations")
        st.subheader("Content-based Filtering")
        st.write("""
        Content-based filtering recommends movies similar to ones you've liked before. It's like saying, 
        "If you enjoyed 'The Dark Knight', you might like other superhero movies or films directed by Christopher Nolan."

        Example: If you loved 'Jurassic Park', the system might recommend 'Godzilla' or 'King Kong' because they're all about big creatures and adventure.
        """)
        
        st.subheader("Collaborative Filtering")
        st.write("""
        Collaborative filtering suggests movies based on what similar users liked. It's like getting recommendations from friends with similar tastes.

        Example: If you and another user both gave 5 stars to 'The Shawshank Redemption' and 'The Godfather', and they loved 'Goodfellas', 
        the system might recommend 'Goodfellas' to you too.
        """)

    with tab2:
        st.header("Explore Recommendations")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            recommendation_type = st.selectbox('Select Recommendation Type', ('Content-based', 'Collaborative Filtering'))
            
            if recommendation_type == 'Content-based':
                movie_list = movies['title'].tolist()
                selected_movie = st.selectbox('Select a movie', movie_list)
            else:
                algo_type = st.selectbox('Select Algorithm', ('SVD', 'KNNBasic', 'CoClustering'))
                user_id = st.number_input('Enter User ID', min_value=1, value=1, step=1)
            
            recommend_button = st.button('Recommend', key='recommend_button')
        
        with col2:
            if recommend_button:
                st.subheader("Recommendation Results")
                with st.spinner('Generating Recommendations...'):
                    if recommendation_type == 'Content-based':
                        recommendations = context_based_recommender(selected_movie)
                        st.write(f'Recommendations based on "{selected_movie}":')
                        st.dataframe(recommendations.style.background_gradient(cmap='YlGn'), use_container_width=True)
                    else:
                        recommendations, model = collaborative_filtering(user_id, algo_type)
                        st.write(f'Top 10 Recommendations for User {user_id} using {algo_type}:')
                        st.dataframe(recommendations.style.background_gradient(cmap='YlGn'), use_container_width=True)

                        if algo_type == 'SVD':
                            st.subheader('SVD Factor Visualization')
                            plot_svd_factors(model)
                        elif algo_type == 'KNNBasic':
                            st.subheader('User Similarity vs Rating Visualization')
                            plot_knn_similarity(model, user_id)
                        elif algo_type == 'CoClustering':
                            st.subheader('Co-Clustering Visualization')
                            plot_coclustering_clusters(model)

    with tab3:
        st.header("Test Your Knowledge")
        questions = [
            {
                "question": "What does content-based filtering mainly consider?",
                "options": ["User ratings", "Movie features", "User demographics", "Box office performance"],
                "answer": "Movie features"
            },
            {
                "question": "Which algorithm is NOT used in collaborative filtering in this app?",
                "options": ["SVD", "KNNBasic", "CoClustering", "Random Forest"],
                "answer": "Random Forest"
            },
            {
                "question": "What's the main advantage of collaborative filtering?",
                "options": ["It's faster", "It doesn't need movie content information", "It always provides perfect recommendations", "It only works for new movies"],
                "answer": "It doesn't need movie content information"
            }
        ]

        for i, q in enumerate(questions):
            st.subheader(f"Question {i+1}")
            st.write(q["question"])
            answer = st.radio("Select your answer:", q["options"], key=f"q{i}")
            if st.button("Show Answer", key=f"btn{i}"):
                if answer == q["answer"]:
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Incorrect. The correct answer is: {q['answer']}")

if __name__ == '__main__':
    main()
