import streamlit as st
import pandas as pd
import numpy as np
import json
import gzip
import spacy
import tensorflow as tf
from keras import layers, models
from keras.optimizers import Adam
from collections import deque
import random
import plotly.express as px

# Load necessary libraries and data
@st.cache_resource
def load_nlp():
    return spacy.load('en_core_web_sm')

nlp = load_nlp()

@st.cache_data
def load_data():
    data = []
    with gzip.open('AMAZON_FASHION.json.gz') as f:
        for l in f:
            data.append(json.loads(l.strip()))
    return pd.DataFrame(data)

# Load and preprocess the data
df = load_data()
df = df[['overall','verified','reviewerID','asin','style','reviewerName','reviewText', 'summary','reviewTime']]
filtered_df = df[(df['verified'] == True) & (~df['overall'].isnull())]

# Streamlit app
st.title("Amazon Fashion Recommendation System")

# Display basic statistics
st.header("Dataset Overview")
st.write(f"Total number of reviews: {len(filtered_df)}")
st.write(f"Number of unique products: {filtered_df['asin'].nunique()}")
st.write(f"Number of unique reviewers: {filtered_df['reviewerID'].nunique()}")

# Rating distribution
st.header("Rating Distribution")
rating_counts = filtered_df['overall'].value_counts().sort_index()
fig_ratings = px.bar(x=rating_counts.index, y=rating_counts.values, labels={'x': 'Rating', 'y': 'Count'})
fig_ratings.update_layout(title='Distribution of Ratings')
st.plotly_chart(fig_ratings)

# Function to extract nouns from review text
@st.cache_data
def extract_nouns(doc):
    return " ".join([token.text for token in nlp(doc) if token.pos_ == "NOUN" or token.pos_ == "PROPN"])

# Simplified FashionProduct class
class FashionProduct:
    def __init__(self, product_asin, reviewerId, metadata, ratings):
        self.product_asin = product_asin
        self.reviewerId = reviewerId
        self.metadata = metadata
        self.ratings = ratings

# Simplified DQNAgent class
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self.build_model()

    def build_model(self):
        encoder = tf.keras.layers.TextVectorization(max_tokens=10000)
        model = tf.keras.Sequential([
            encoder,
            layers.Embedding(10000, 64, mask_zero=True),
            layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
            layers.Bidirectional(tf.keras.layers.LSTM(32)),
            layers.Dense(64, activation='relu')
        ])
        ratings_input = tf.keras.layers.Input(shape=(1,), name='ratings_input')
        concatenated = layers.concatenate([model.output, ratings_input])
        dense_layer = layers.Dense(64, activation='relu')(concatenated)
        output_layer = layers.Dense(self.action_size, activation='linear')(dense_layer)
        model = tf.keras.Model(inputs=[model.input, ratings_input], outputs=output_layer)
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model

    def get_action(self, state):
        q_value = self.model.predict([np.array([state.metadata]), np.array([state.ratings])])
        return np.argpartition(q_value[0], -10)[-10:]

# Simplified environment
class RecommendationEnv:
    def __init__(self, states, states_dict):
        self.states = states
        self.states_dict = states_dict
        self.state = self.states[0]
        self.index = 0

    def step(self, actions):
        reward = 0
        done = False
        reviewerId = self.state.reviewerId
        future_asins = [p for p in self.states_dict if self.states_dict[p].reviewerId == reviewerId and self.states_dict[p].product_asin != self.state.product_asin]
        
        for i in actions:
            if self.states[i].product_asin in future_asins:
                reward = 1
                break
        
        self.index += 1
        if self.index >= len(self.states):
            done = True
        else:
            self.state = self.states[self.index]
        
        return self.state, reward, done, {}

    def reset(self):
        self.state = self.states[0]
        self.index = 0
        return self.state

# Create sample data for demonstration
sample_products = [
    FashionProduct("A001", "R001", "red dress cotton summer", 4.5),
    FashionProduct("A002", "R001", "blue jeans denim casual", 4.0),
    FashionProduct("A003", "R002", "black shoes leather formal", 3.5),
    FashionProduct("A004", "R002", "white shirt cotton office", 4.2),
    FashionProduct("A005", "R003", "green sweater wool winter", 4.8),
]

sample_states_dict = {p.product_asin: p for p in sample_products}

# Initialize environment and agent
env = RecommendationEnv(sample_products, sample_states_dict)
agent = DQNAgent(len(sample_products), len(sample_products))

# Streamlit interface for recommendation
st.header("Product Recommendation Demo")
st.write("This demo shows how the recommendation system would work. It uses a simplified version of the DQN agent to recommend products based on the current product.")

selected_product = st.selectbox("Select a product:", [p.product_asin for p in sample_products])
current_product = sample_states_dict[selected_product]

st.write(f"Selected product: {current_product.product_asin}")
st.write(f"Product metadata: {current_product.metadata}")
st.write(f"Product rating: {current_product.ratings}")

if st.button("Get Recommendations"):
    recommended_indices = agent.get_action(current_product)
    st.write("Recommended products:")
    for idx in recommended_indices:
        rec_product = sample_products[idx]
        st.write(f"- {rec_product.product_asin}: {rec_product.metadata} (Rating: {rec_product.ratings})")

st.write("Note: This is a simplified demonstration. In a real scenario, the model would be trained on the full dataset and provide more accurate recommendations.")

# Additional information about the recommendation system
st.header("About the Recommendation System")
st.write("This recommendation system uses a Deep Q-Network (DQN) to learn and predict product recommendations. The system considers product metadata (extracted from reviews) and ratings to make its decisions.")

st.write("Key components of the system:")
st.write("1. Text vectorization and embedding of product metadata")
st.write("2. LSTM layers for processing sequential data")
st.write("3. Integration of product ratings")
st.write("4. Q-value prediction for each potential recommendation")

st.write("In a full implementation, the system would be trained over multiple episodes, learning to recommend products that users are likely to purchase in the future based on their current selection and past behavior.")
