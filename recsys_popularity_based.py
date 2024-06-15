import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('imdb_top_2000_movies.csv')
    data['Votes'] = data['Votes'].str.replace(',', '').astype(int)
    return data

df = load_data()

# Title and description
st.title('Popularity-Based Movie Recommender System')
st.write("Explore the most popular movies based on IMDb ratings and votes.")

# Sidebar options
number_of_movies = st.sidebar.slider('Number of Movies to Display', min_value=10, max_value=100, value=50, step=10)
metric_to_sort_by = st.sidebar.radio("Sort by", ['IMDB Rating', 'Votes'])

# Sorting data
sorted_df = df.sort_values(by=metric_to_sort_by, ascending=False).head(number_of_movies)

# Displaying data in a table
st.write(sorted_df[['Movie Name', 'Release Year', 'IMDB Rating', 'Votes', 'Director']])

# Visualizing data
fig = px.bar(sorted_df, x='Movie Name', y=metric_to_sort_by, hover_data=['Director', 'Genre', 'Gross'], color='IMDB Rating')
st.plotly_chart(fig)

# Conclusion
st.markdown("This interactive application helps you explore the most popular movies and understand the factors that contribute to their success.")

