import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Popularity-Based Recommender System", layout="wide")

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
def load_data(dataset_name):
    if dataset_name == 'Movies':
        data = pd.read_csv('imdb_top_2000_movies.csv')
        data['Votes'] = data['Votes'].str.replace(',', '').astype(int)
    elif dataset_name == 'Books - Book Dataset':
        data = pd.read_csv('book_dataset.csv')
    elif dataset_name == 'Books - Good Reads Top 1000':
        data = pd.read_csv('good_reads_top_1000_books.csv')
    elif dataset_name == 'Restaurants':
        data = pd.read_csv('North America Restaurants.csv')
    return data

# Main content
st.title('Popularity-Based Recommender System')
st.write('**Developed by : Venugopal Adep**')

# Create tabs
tab1, tab2, tab3 = st.tabs(["Learn", "Explore", "Quiz"])

with tab1:
    st.header("Understanding Popularity-Based Recommender Systems")
    st.write("""
    A popularity-based recommender system is a simple yet effective way to suggest items to users based on how popular those items are among all users. Here's how it works:

    1. **Data Collection**: The system gathers data on user interactions with items, such as ratings, views, or purchases.

    2. **Popularity Calculation**: It calculates the popularity of each item, often using metrics like average rating, number of ratings, or a combination of both.

    3. **Ranking**: Items are then ranked based on their popularity scores.

    4. **Recommendation**: The system recommends the top-ranked items to users.

    **Example**: 
    Let's say we have a movie recommender system. If the movie "The Shawshank Redemption" has an average rating of 9.3 out of 10 from 2.5 million votes, it would likely be ranked higher and recommended more often than a movie with an average rating of 7.5 from 100,000 votes.

    This system is easy to implement and understand, but it doesn't personalize recommendations for individual users. It's often used as a baseline or for new users where personalized data isn't available yet.
    """)

with tab2:
    st.header("Explore Popularity-Based Recommendations")
    
    # Select dataset
    dataset_name = st.selectbox(
        "Select a dataset",
        ('Movies', 'Books - Book Dataset', 'Books - Good Reads Top 1000', 'Restaurants')
    )
    df = load_data(dataset_name)

    # Sidebar options for sorting based on columns present in the dataset
    if dataset_name == 'Books - Book Dataset':
        sorting_options = ['average_rating', 'ratings_count']
    elif dataset_name == 'Books - Good Reads Top 1000':
        sorting_options = ['Average Rating', 'Number of Ratings', 'Score on Goodreads']
    elif dataset_name == 'Restaurants':
        sorting_options = ['weighted_rating_value', 'aggregated_rating_count']
    else:
        sorting_options = [col for col in df.columns if 'rating' in col.lower() or 'votes' in col.lower() or 'score' in col.lower()]
        if not sorting_options:
            sorting_options = ['ID'] if 'ID' in df.columns else df.columns[:1]

    metric_to_sort_by = st.radio("Sort by", sorting_options)
    number_of_items = st.slider('Number of Items to Display', min_value=10, max_value=100, value=50, step=10)

    # Sorting data
    sorted_df = df.sort_values(by=metric_to_sort_by, ascending=False).head(number_of_items)
    columns_to_display = sorted_df.columns

    # Displaying data in a table
    st.write(sorted_df[columns_to_display])

    # Visualizing data
    fig = px.bar(sorted_df, x=columns_to_display[0], y=metric_to_sort_by, hover_data=columns_to_display)
    st.plotly_chart(fig)

    st.markdown(f"This interactive application helps you explore the most popular items and understand the factors that contribute to their success in the {dataset_name.lower()} industry.")

with tab3:
    st.header("Test Your Knowledge")
    
    st.subheader("Question 1: What is the main advantage of a popularity-based recommender system?")
    q1_options = ["It provides highly personalized recommendations", "It's simple to implement and understand", "It requires a lot of user data", "It's always the most accurate system"]
    q1_answer = st.radio("Select your answer:", q1_options, key="q1")
    if st.button("Show Answer", key="b1"):
        st.write("The correct answer is: It's simple to implement and understand.")
        st.write("Explanation: Popularity-based recommender systems are easy to set up and interpret. They don't require complex algorithms or extensive user data, making them a good starting point for many applications.")

    st.subheader("Question 2: What's a potential drawback of popularity-based recommender systems?")
    q2_options = ["They're too complex", "They require too much computing power", "They don't provide personalized recommendations", "They only work for movies"]
    q2_answer = st.radio("Select your answer:", q2_options, key="q2")
    if st.button("Show Answer", key="b2"):
        st.write("The correct answer is: They don't provide personalized recommendations.")
        st.write("Explanation: These systems recommend the same popular items to everyone, regardless of individual preferences. This means they might not be as effective for users with unique tastes or for discovering niche items.")

    st.subheader("Question 3: In a movie recommender system, which of these metrics would likely be used to determine popularity?")
    q3_options = ["Movie budget", "Release date", "Average user rating", "Director's age"]
    q3_answer = st.radio("Select your answer:", q3_options, key="q3")
    if st.button("Show Answer", key="b3"):
        st.write("The correct answer is: Average user rating.")
        st.write("Explanation: Popularity-based systems often use metrics like average rating or number of ratings to determine an item's popularity. While factors like budget or release date might influence a movie's success, they're not direct measures of user preference or popularity.")
