import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, KNNBasic, CoClustering
import matplotlib.pyplot as plt
import plotly.express as px

# Custom CSS to make the layout wider and more visually appealing
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            max-width: 95%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .stSelectbox [data-baseweb="select"] {
            background-color: #4a4a4a;
        }
        .stSelectbox [data-baseweb="select"] > div {
            color: white;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #0E1117;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            padding-left: 20px;
            padding-right: 20px;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            background-color: #262730;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        h1, h2, h3 {
            color: #4CAF50;
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
    st.title('🎬 Movie Recommendation System')

    # Create two columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Input Parameters")
        recommendation_type = st.selectbox('Select Recommendation Type', ('Content-based', 'Collaborative Filtering'))
        
        if recommendation_type == 'Content-based':
            movie_list = movies['title'].tolist()
            selected_movie = st.selectbox('Select a movie', movie_list)
        else:
            algo_type = st.selectbox('Select Algorithm', ('SVD', 'KNNBasic', 'CoClustering'))
            user_id = st.number_input('Enter User ID', min_value=1, value=1, step=1)
        
        recommend_button = st.button('Recommend', key='recommend_button')

    with col2:
        # Main content area with tabs
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
            if recommend_button:
                st.header("Recommendation Results")
                with st.spinner('Generating Recommendations...'):
                    if recommendation_type == 'Content-based':
                        recommendations = context_based_recommender(selected_movie)
                        st.write(f'Recommendations based on "{selected_movie}":')
                        st.dataframe(recommendations.style.background_gradient(cmap='YlOrRd'))
                    else:
                        recommendations, model = collaborative_filtering(user_id, algo_type)
                        st.write(f'Top 10 Recommendations for User {user_id} using {algo_type}:')
                        st.dataframe(recommendations.style.background_gradient(cmap='YlOrRd'))

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
