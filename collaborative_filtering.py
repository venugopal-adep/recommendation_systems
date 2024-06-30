import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from scipy.spatial import distance

st.title("Collaborative Filtering Explained")

st.markdown(r"""
**Collaborative Filtering** is a technique used in recommendation systems. The main idea behind collaborative filtering is that if a user's likes/dislikes are similar to another user's likes/dislikes, then their tastes are similar. We can use this to recommend products that other similar users liked.

It is based on the assumption that if a person liked something in the past, they will also like it in the future. Collaborative filtering is of two types:
- **User-User Collaborative Filtering**: It is based on the search for similar users in terms of interactions with items.
- **Item-Item Collaborative Filtering**: It is based on the search for similar items in terms of user-item interactions.
""")

# Sidebar controls
st.sidebar.subheader("Controls")
filtering_type = st.sidebar.selectbox("Filtering Type", ["User-User", "Item-Item"])
num_users = st.sidebar.slider("Number of Users", 5, 20, 10)
num_items = st.sidebar.slider("Number of Items", 5, 20, 10)
k_value = st.sidebar.slider("Value of k", 1, 10, 5)
regenerate_data = st.sidebar.button("Regenerate Data")

# Initialize or regenerate data
if regenerate_data or 'user_item_matrix' not in st.session_state:
    np.random.seed(42)
    st.session_state.user_item_matrix = np.random.randint(0, 2, size=(num_users, num_items))

user_item_matrix = st.session_state.user_item_matrix

# Display the user-item matrix as a heatmap
st.sidebar.subheader("User-Item Matrix")
fig_user_item_heatmap = px.imshow(user_item_matrix, text_auto=True, aspect="auto", color_continuous_scale='Blues')
fig_user_item_heatmap.update_layout(
    title='User-Item Matrix',
    xaxis_title='Items',
    yaxis_title='Users',
    xaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'Item {i+1}' for i in range(num_items)]),
    yaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'User {i+1}' for i in range(num_users)])
)
st.sidebar.plotly_chart(fig_user_item_heatmap, use_container_width=True)

# Function to calculate similarity
def calculate_similarity(matrix, type='user'):
    if type == 'user':
        return 1 - distance.cdist(matrix, matrix, 'cosine')
    else:
        return 1 - distance.cdist(matrix.T, matrix.T, 'cosine')

# Calculate similarity based on the selected filtering type
if filtering_type == 'User-User':
    similarity_matrix = calculate_similarity(user_item_matrix, type='user')
else:
    similarity_matrix = calculate_similarity(user_item_matrix, type='item')

# Display the similarity matrix as a heatmap
st.subheader(f"{filtering_type} Similarity Matrix")
fig_heatmap = px.imshow(similarity_matrix, text_auto='.2f', aspect="auto", color_continuous_scale='Blues')
if filtering_type == 'User-User':
    fig_heatmap.update_layout(
        xaxis_title='Users',
        yaxis_title='Users',
        xaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'User {i+1}' for i in range(num_users)]),
        yaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'User {i+1}' for i in range(num_users)])
    )
else:
    fig_heatmap.update_layout(
        xaxis_title='Items',
        yaxis_title='Items',
        xaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'Item {i+1}' for i in range(num_items)]),
        yaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'Item {i+1}' for i in range(num_items)])
    )
st.plotly_chart(fig_heatmap, use_container_width=True)

# Select a random user/item to demonstrate the recommendation
if filtering_type == 'User-User':
    random_index = np.random.randint(num_users)
    st.markdown(f"<span style='color: red; font-weight: bold;'>Recommendations for User {random_index + 1} based on similar users:</span>", unsafe_allow_html=True)

    # Find similar users
    similar_users = np.argsort(-similarity_matrix[random_index])[1:k_value + 1]  # Exclude self
    similar_users_display = [f"User{user + 1}" for user in similar_users]
    st.markdown(f"<span style='color: red; font-weight: bold;'>Top similar users: {similar_users_display}</span>", unsafe_allow_html=True)

    st.write("Explanation of similarity calculation:")
    st.write(f"1. We calculate the cosine similarity between User {random_index + 1} and all other users.")
    st.write("2. Cosine similarity measures the cosine of the angle between two vectors, ranging from -1 to 1.")
    st.write("3. We subtract the cosine similarity from 1 to get a distance measure (0 means identical, 2 means opposite).")
    st.write(f"4. We then sort these distances in ascending order to find the {k_value} most similar users.")

    # Recommend items that similar users have interacted with
    recommended_items = np.zeros(num_items, dtype=int)
    for user in similar_users:
        recommended_items += user_item_matrix[user]
    recommended_items = np.where(recommended_items > 0, 1, 0)
    recommended_items = np.where((recommended_items - user_item_matrix[random_index]) > 0)[0]  # Exclude already interacted items
    recommended_items_display = [f"Item{item + 1}" for item in recommended_items]
    st.markdown(f"<span style='color: red; font-weight: bold;'>Recommended items: {recommended_items_display}</span>", unsafe_allow_html=True)

    st.write("Explanation of recommendation process:")
    st.write(f"1. We look at the items that the {k_value} most similar users have interacted with.")
    st.write("2. We sum up these interactions to get a score for each item.")
    st.write("3. We convert these scores to binary (0 or 1) to get a list of all items these similar users have interacted with.")
    st.write(f"4. We remove the items that User {random_index + 1} has already interacted with.")
    st.write("5. The remaining items are our recommendations.")

else:
    random_index = np.random.randint(num_items)
    st.markdown(f"<span style='color: red; font-weight: bold;'>Recommendations for Item {random_index + 1} based on similar items:</span>", unsafe_allow_html=True)

    # Find similar items
    similar_items = np.argsort(-similarity_matrix[random_index])[1:k_value + 1]  # Exclude self
    similar_items_display = [f"Item{item + 1}" for item in similar_items]
    st.markdown(f"<span style='color: red; font-weight: bold;'>Top similar items: {similar_items_display}</span>", unsafe_allow_html=True)

    st.write("Explanation of similarity calculation:")
    st.write(f"1. We calculate the cosine similarity between Item {random_index + 1} and all other items.")
    st.write("2. Cosine similarity measures the cosine of the angle between two vectors, ranging from -1 to 1.")
    st.write("3. We subtract the cosine similarity from 1 to get a distance measure (0 means identical, 2 means opposite).")
    st.write(f"4. We then sort these distances in ascending order to find the {k_value} most similar items.")

    # Recommend to users who have interacted with similar items
    recommended_users = np.zeros(num_users, dtype=int)
    for item in similar_items:
        recommended_users += user_item_matrix[:, item]
    recommended_users = np.where(recommended_users > 0, 1, 0)
    recommended_users = np.where((recommended_users - user_item_matrix[:, random_index]) > 0)[0]  # Exclude already interacted users
    recommended_users_display = [f"User{user + 1}" for user in recommended_users]
    st.markdown(f"<span style='color: red; font-weight: bold;'>Recommended to users: {recommended_users_display}</span>", unsafe_allow_html=True)

    st.write("Explanation of recommendation process:")
    st.write(f"1. We look at the users who have interacted with the {k_value} most similar items.")
    st.write("2. We sum up these interactions to get a score for each user.")
    st.write("3. We convert these scores to binary (0 or 1) to get a list of all users who have interacted with these similar items.")
    st.write(f"4. We remove the users who have already interacted with Item {random_index + 1}.")
    st.write("5. The remaining users are our recommendations.")

# Visualize the recommendations
fig = go.Figure()

# Plotting the user-item matrix
for i in range(num_users):
    for j in range(num_items):
        color = 'blue' if user_item_matrix[i, j] == 1 else 'red'
        fig.add_trace(go.Scatter(
            x=[j + 1],
            y=[i + 1],
            mode='markers',
            marker=dict(color=color, size=10),
            name=f"User {i + 1}, Item {j + 1}"
        ))

# Highlight the random user/item and their recommendations
if filtering_type == 'User-User':
    for item in recommended_items:
        fig.add_trace(go.Scatter(
            x=[item + 1],
            y=[random_index + 1],
            mode='markers',
            marker=dict(color='green', size=15),
            name=f"Recommended Item {item + 1}"
        ))
else:
    for user in recommended_users:
        fig.add_trace(go.Scatter(
            x=[random_index + 1],
            y=[user + 1],
            mode='markers',
            marker=dict(color='green', size=15),
            name=f"Recommended to User {user + 1}"
        ))

fig.update_layout(
    title='Collaborative Filtering Visualization',
    xaxis=dict(title='Items', tickmode='array', tickvals=list(range(1, num_items+1)), ticktext=[f'Item {i}' for i in range(1, num_items+1)]),
    yaxis=dict(title='Users', tickmode='array', tickvals=list(range(1, num_users+1)), ticktext=[f'User {i}' for i in range(1, num_users+1)]),
    showlegend=False,
    width=800,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Legend:**
- **Blue Dots**: Existing interactions between users and items.
- **Red Dots**: No interaction between users and items.
- **Green Dots**: Recommended interactions based on the collaborative filtering algorithm.
""")

# Display User and Item indices
st.subheader("User and Item Indices:")
st.write("Users:", ", ".join([f"User{i+1}" for i in range(num_users)]))
st.write("Items:", ", ".join([f"Item{i+1}" for i in range(num_items)]))
