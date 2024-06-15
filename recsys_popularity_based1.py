import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
@st.cache_data
def load_data(dataset_name):
    if dataset_name == 'Movies':
        data = pd.read_csv('imdb_top_2000_movies.csv')
        data['Votes'] = data['Votes'].str.replace(',', '').astype(int)  # Cleaning the 'Votes' column
    elif dataset_name == 'Books - Book Dataset':
        data = pd.read_csv('book_dataset.csv')
    elif dataset_name == 'Books - Good Reads Top 1000':
        data = pd.read_csv('good_reads_top_1000_books.csv')
    elif dataset_name == 'Restaurants':
        data = pd.read_csv('North America Restaurants.csv')
    return data

# Select dataset
dataset_name = st.sidebar.selectbox(
    "Select a dataset",
    ('Movies', 'Books - Book Dataset', 'Books - Good Reads Top 1000', 'Restaurants')
)

df = load_data(dataset_name)

# Title and description
st.title(f'Popularity-Based Recommender System for {dataset_name}')
st.write(f"Explore the most popular items based on ratings and votes from the selected {dataset_name.lower()} dataset.")

# Sidebar options for sorting based on columns present in the dataset
if dataset_name == 'Books - Book Dataset':
    sorting_options = ['average_rating', 'ratings_count']
elif dataset_name == 'Books - Good Reads Top 1000':
    sorting_options = ['Average Rating', 'Number of Ratings', 'Score on Goodreads']
elif dataset_name == 'Restaurants':
    sorting_options = ['weighted_rating_value', 'aggregated_rating_count']
else:
    sorting_options = [col for col in df.columns if 'rating' in col.lower() or 'votes' in col.lower() or 'score' in col.lower()]
    if not sorting_options:  # Fallback if no typical sorting columns are found
        sorting_options = ['ID'] if 'ID' in df.columns else df.columns[:1]  # Use ID or the first column as a fallback

metric_to_sort_by = st.sidebar.radio("Sort by", sorting_options)

number_of_items = st.sidebar.slider('Number of Items to Display', min_value=10, max_value=100, value=50, step=10)

# Sorting data
sorted_df = df.sort_values(by=metric_to_sort_by, ascending=False).head(number_of_items)

# Displaying all columns in the sorted dataset
columns_to_display = sorted_df.columns

# Displaying data in a table
st.write(sorted_df[columns_to_display])

# Visualizing data
fig = px.bar(sorted_df, x=columns_to_display[0], y=metric_to_sort_by, hover_data=columns_to_display)
st.plotly_chart(fig)

# Conclusion
st.markdown(f"This interactive application helps you explore the most popular items and understand the factors that contribute to their success in the {dataset_name.lower()} industry.")