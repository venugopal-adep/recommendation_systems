import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# Custom CSS for a clean, compact, and visually appealing interface
st.set_page_config(layout="wide", page_title="Movie Recommender")
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            max-width: 90%;
            padding: 1rem;
        }
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
        }
        .stButton>button {
            width: 100%;
            background-color: #6c5ce7;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #5649c0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2d3436;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .movie-card {
            background-color: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .recommendation-score {
            font-weight: bold;
            color: #6c5ce7;
        }
        .stDataFrame {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header-container {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        .header-text {
            margin-left: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data()
def load_data():
    movies = pd.read_csv('movielens/movies.csv')
    return movies

movies = load_data()

# Content-based Filtering
@st.cache_data()
def content_based_recommender(movie_title, num_recommendations=10):
    tfidf = TfidfVectorizer(stop_words='english')
    movies['description'] = movies['title'] + ' ' + movies['genres']
    tfidf_matrix = tfidf.fit_transform(movies['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
    idx = indices[movie_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    similarity_scores = [round(i[1] * 100, 2) for i in sim_scores]

    recommendations = movies.iloc[movie_indices].copy()
    recommendations['similarity_score'] = similarity_scores
    recommendations = recommendations.sort_values('similarity_score', ascending=False)

    return recommendations[['title', 'genres', 'similarity_score']]

# Visualization function
def plot_genre_distribution(recommendations):
    # Extract all genres from recommendations
    all_genres = []
    for genre_list in recommendations['genres'].str.split('|'):
        all_genres.extend(genre_list)
    
    # Count genre occurrences
    genre_counts = pd.Series(all_genres).value_counts()
    
    # Create a bar chart
    fig = px.bar(
        x=genre_counts.index, 
        y=genre_counts.values,
        labels={'x': 'Genre', 'y': 'Count'},
        title='Genre Distribution in Recommendations',
        color=genre_counts.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Count",
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# Main function
def main():
    st.markdown("""
    <div class="header-container">
        <h1>🎬 Smart Movie Recommender</h1>
    </div>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">
        Discover movies similar to your favorites using content-based filtering
    </p>
    """, unsafe_allow_html=True)
    
    # Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🔍 Find Recommendations")
        movie_list = sorted(movies['title'].tolist())
        selected_movie = st.selectbox('Select a movie you like', movie_list)
        
        num_recommendations = st.slider(
            "Number of recommendations", 
            min_value=5, 
            max_value=20, 
            value=10,
            step=1
        )
        
        recommend_button = st.button('Get Recommendations', key='recommend_button')
        
        # Add some information about content-based filtering
        with st.expander("How does this work?"):
            st.markdown("""
            **Content-based filtering** recommends movies by analyzing the characteristics of your selected movie.
            
            The system looks at features like:
            - Movie genres
            - Movie titles
            
            It then finds movies with similar features using text analysis and cosine similarity.
            
            The similarity score (0-100%) indicates how closely a recommended movie matches your selection.
            """)
    
    with col2:
        if recommend_button:
            with st.spinner('Finding the perfect movies for you...'):
                recommendations = content_based_recommender(selected_movie, num_recommendations)
                
                st.markdown(f"### Recommendations based on '{selected_movie}'")
                
                # Display recommendations in a styled table
                st.dataframe(
                    recommendations.style
                    .format({'similarity_score': '{:.2f}%'})
                    .background_gradient(subset=['similarity_score'], cmap='viridis'),
                    use_container_width=True,
                    height=400
                )
                
                # Show genre distribution visualization
                st.markdown("### Genre Analysis")
                genre_fig = plot_genre_distribution(recommendations)
                st.plotly_chart(genre_fig, use_container_width=True)
                
                # Show top genres in the selected movie
                selected_movie_genres = movies[movies['title'] == selected_movie]['genres'].values[0].split('|')
                st.markdown(f"**Genres in '{selected_movie}':** {', '.join(selected_movie_genres)}")

if __name__ == '__main__':
    main()
