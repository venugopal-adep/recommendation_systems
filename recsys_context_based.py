import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os
import logging
from typing import Tuple, List
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sentence_transformers import SentenceTransformer

# Set page config (this must be the first Streamlit command)
st.set_page_config(page_title="Solution Recommender", layout="wide")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MAIN_DATA_FILE = 'AIOps_Error_and_Solution_Dataset.csv'
SIMILARITY_THRESHOLD = 0.3

# Initialize session state
if 'data_version' not in st.session_state:
    st.session_state.data_version = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'excluded_indices' not in st.session_state:
    st.session_state.excluded_indices = []

# Download necessary NLTK data
@st.cache_resource
def download_nltk_data():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        logging.error(f"Failed to download NLTK data: {e}")
        st.error("Failed to initialize NLP components. Please check your internet connection and try again.")

download_nltk_data()

# Preprocess text
def preprocess_text(text: str) -> str:
    try:
        tokens = word_tokenize(str(text).lower())
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
        return ' '.join(tokens)
    except Exception as e:
        logging.error(f"Error in text preprocessing: {e}")
        return str(text)

# Load the data
@st.cache_data
def load_data(version):
    try:
        if os.path.exists(MAIN_DATA_FILE):
            df = pd.read_csv(MAIN_DATA_FILE)
            if 'Preprocessed_Error' not in df.columns:
                df['Preprocessed_Error'] = df['Error'].apply(preprocess_text)
            if 'Solution' not in df.columns:
                df['Solution'] = ''
            df['Preprocessed_Error'] = df['Error'].apply(preprocess_text)
            logging.info("Successfully loaded and preprocessed data")
        else:
            df = pd.DataFrame(columns=['Error', 'Solution', 'Preprocessed_Error'])
            logging.info("Created new dataframe as file doesn't exist")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        st.error(f"Failed to load data: {e}. Please check the file and try again.")
        return pd.DataFrame(columns=['Error', 'Solution', 'Preprocessed_Error'])

# Create vectorizer
@st.cache_resource
def create_vectorizer(texts: pd.Series, vectorizer_type: str):
    if vectorizer_type == 'TF-IDF':
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(texts)
    elif vectorizer_type == 'Count':
        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(texts)
    elif vectorizer_type == 'Hashing':
        vectorizer = HashingVectorizer(n_features=2**10)
        matrix = vectorizer.fit_transform(texts)
    elif vectorizer_type == 'Sentence-BERT':
        vectorizer = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        matrix = vectorizer.encode(texts.tolist())
    return vectorizer, matrix

# Function to find the top matches
def find_top_matches(query: str, df: pd.DataFrame, vectorizer, matrix, vectorizer_type: str, top_n: int = 5, exclude_indices: List[int] = []) -> List[Tuple[pd.Series, float]]:
    preprocessed_query = preprocess_text(query)
    
    if vectorizer_type in ['TF-IDF', 'Count', 'Hashing']:
        query_vector = vectorizer.transform([preprocessed_query])
        cosine_similarities = cosine_similarity(query_vector, matrix).flatten()
    elif vectorizer_type == 'Sentence-BERT':
        query_vector = vectorizer.encode([preprocessed_query])
        cosine_similarities = cosine_similarity(query_vector, matrix).flatten()
    
    # Create a list of (index, similarity) tuples
    similarity_tuples = list(enumerate(cosine_similarities))
    
    # Sort by similarity in descending order
    similarity_tuples.sort(key=lambda x: x[1], reverse=True)
    
    # Filter out excluded indices and get top matches
    top_matches = []
    for idx, sim in similarity_tuples:
        if idx not in exclude_indices and sim > 0:
            top_matches.append((df.iloc[idx], sim))
        if len(top_matches) == top_n:
            break
    
    return top_matches

# Function to add new entries to the dataset
def add_new_entry(error: str, solution: str, df: pd.DataFrame) -> pd.DataFrame:
    preprocessed_error = preprocess_text(error)
    new_row = pd.DataFrame({
        'Error': [error],
        'Solution': [solution],
        'Preprocessed_Error': [preprocessed_error]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(MAIN_DATA_FILE, index=False)
    st.session_state.data_version += 1  # Increment data version to force reload
    logging.info(f"New entry added successfully: {error[:50]}...")
    return df

# Load data
df = load_data(st.session_state.data_version)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stDataFrame {
        border-radius: 5px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.title("Solution Recommender")

# Sidebar
st.sidebar.header("About the Dataset")
st.sidebar.write(f"Total entries: {len(df)}")
st.sidebar.write(f"Answered queries: {df['Solution'].notna().sum()}")
st.sidebar.write(f"Unanswered queries: {df['Solution'].isna().sum()}")

# Vectorizer selection
vectorizer_type = st.sidebar.selectbox(
    "Select Vectorizer",
    ["TF-IDF", "Count", "Hashing", "Sentence-BERT"],
    index=0
)

# Create vectorizer based on selection
vectorizer, matrix = create_vectorizer(df['Preprocessed_Error'], vectorizer_type)

# Main content
tab1, tab2, tab3 = st.tabs(["Data Overview", "Recommendation Engine", "Unanswered Queries"])

with tab1:
    st.header("Data Overview")
    
    # Sample Data
    st.subheader("Sample Data")
    st.dataframe(df[['Error', 'Solution']].head(10))

    # Basic Statistics
    st.subheader("Basic Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Error Length Statistics:")
        st.write(df['Error'].str.len().describe())
    with col2:
        st.write("Solution Length Statistics:")
        st.write(df['Solution'].str.len().describe())

    # Most Common Errors
    st.subheader("Most Common Errors")
    error_counts = df['Error'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=error_counts.values, y=error_counts.index, ax=ax)
    ax.set_title("Top 10 Most Common Errors")
    ax.set_xlabel("Count")
    ax.set_ylabel("Error")
    st.pyplot(fig)

    # Error Length Distribution
    st.subheader("Error Length Distribution")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df['Error'].str.len(), bins=30, kde=True, ax=ax)
    ax.set_title("Distribution of Error Lengths")
    ax.set_xlabel("Error Length")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Word Cloud
    st.subheader("Word Cloud of Errors")
    try:
        from wordcloud import WordCloud

        text = ' '.join(df['Preprocessed_Error'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except ImportError:
        st.info("Install 'wordcloud' package to see a word cloud visualization of common terms.")

    # Correlation between Error and Solution lengths
    st.subheader("Correlation between Error and Solution Lengths")
    df['Error_Length'] = df['Error'].str.len()
    df['Solution_Length'] = df['Solution'].str.len()
    
    fig = px.scatter(df, x='Error_Length', y='Solution_Length', 
                     title='Error Length vs Solution Length',
                     labels={'Error_Length': 'Error Length', 'Solution_Length': 'Solution Length'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Error Recommendation Engine")
    user_input = st.text_area("Enter your error message:", height=100)
    
    if st.button("Get Recommendations") or (st.session_state.feedback is not None and st.session_state.last_query == user_input):
        if user_input:
            with st.spinner("Processing your request..."):
                top_matches = find_top_matches(user_input, df, vectorizer, matrix, vectorizer_type, exclude_indices=st.session_state.excluded_indices)
            
            if top_matches:
                st.success(f"Top {len(top_matches)} recommendations found!")
                for i, (match, similarity) in enumerate(top_matches, 1):
                    st.subheader(f"Match {i} (Similarity: {similarity:.2f})")
                    st.info(f"Error: {match['Error']}")
                    st.code(f"Solution: {match['Solution']}")
                    st.markdown("---")
                
                # Feedback mechanism
                st.write("Were these recommendations helpful?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Yes"):
                        st.session_state.feedback = 'up'
                        st.session_state.excluded_indices = []  # Reset excluded indices
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No"):
                        st.session_state.feedback = 'down'
                        # Add current results to excluded indices
                        st.session_state.excluded_indices.extend([df.index.get_loc(match.name) for match, _ in top_matches])
                        st.warning("We're sorry the recommendations weren't helpful. We'll try to provide different suggestions.")
            else:
                st.warning("No satisfactory matches found. This query will be added to our unanswered list.")
                df = add_new_entry(user_input, '', df)
                vectorizer, matrix = create_vectorizer(df['Preprocessed_Error'], vectorizer_type)
                st.success("Query added to unanswered list. You can provide a solution in the 'Unanswered Queries' tab.")
        else:
            st.warning("Please enter an error message.")
        
        st.session_state.last_query = user_input

with tab3:
    st.header("Unanswered Queries")
    unanswered = df[df['Solution'].isna() | (df['Solution'] == '')]
    if not unanswered.empty:
        for index, row in unanswered.iterrows():
            with st.expander(f"Error: {row['Error'][:50]}..."):
                st.write(row['Error'])
                solution = st.text_area(f"Enter solution for error {index}:", key=f"solution_{index}")
                if st.button(f"Submit Solution {index}"):
                    df.at[index, 'Solution'] = solution
                    df.at[index, 'Preprocessed_Error'] = preprocess_text(row['Error'])
                    df.to_csv(MAIN_DATA_FILE, index=False)
                    st.session_state.data_version += 1  # Increment data version to force reload
                    st.success("Solution added successfully! It will now be available for recommendations.")
                    df = load_data(st.session_state.data_version)
                    vectorizer, matrix = create_vectorizer(df['Preprocessed_Error'], vectorizer_type)
    else:
        st.info("No unanswered queries at the moment.")

st.sidebar.markdown("---")
st.sidebar.info("This app uses NLP techniques to match your error with the most relevant solutions from our database. If no match is found, you can contribute by adding a solution.")

# Footer
st.markdown("---")
st.markdown("Similarity app | © 2024 Venu and Company")