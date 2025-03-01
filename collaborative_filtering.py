import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from scipy.spatial import distance

# Page configuration
st.set_page_config(page_title="Collaborative Filtering", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {text-align: center; color: #1E88E5; margin-bottom: 0;}
    .sub-header {text-align: center; color: #757575; margin-top: 0; font-size: 1.1em;}
    .section-header {color: #1E88E5; border-bottom: 1px solid #E0E0E0; padding-bottom: 5px;}
    .explanation {background-color: #F8F9FA; padding: 10px; border-radius: 5px; margin: 10px 0;}
    .highlight {color: #FF5733; font-weight: bold;}
    .legend-item {display: flex; align-items: center; margin-bottom: 5px;}
    .legend-color {width: 15px; height: 15px; margin-right: 10px; border-radius: 50%;}
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown("<h1 class='main-header'>Collaborative Filtering Explained</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Developed by: Venugopal Adep</p>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("<h3 class='section-header'>Controls</h3>", unsafe_allow_html=True)
    filtering_type = st.radio("Filtering Type", ["User-User", "Item-Item"])
    num_users = st.slider("Number of Users", 5, 20, 10)
    num_items = st.slider("Number of Items", 5, 20, 10)
    k_value = st.slider("Value of k", 1, 10, 5)
    regenerate_data = st.button("Regenerate Data")

    # Initialize or regenerate data
    if regenerate_data or 'user_item_matrix' not in st.session_state:
        np.random.seed(42)
        st.session_state.user_item_matrix = np.random.randint(0, 2, size=(num_users, num_items))

    user_item_matrix = st.session_state.user_item_matrix

    # Display the user-item matrix as a compact heatmap
    fig_user_item_heatmap = px.imshow(
        user_item_matrix, 
        text_auto=True, 
        aspect="auto", 
        color_continuous_scale='Blues',
        labels=dict(x="Items", y="Users", color="Interaction")
    )
    fig_user_item_heatmap.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        height=250,
        title='User-Item Matrix',
        xaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'{i+1}' for i in range(num_items)]),
        yaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'{i+1}' for i in range(num_users)])
    )
    st.plotly_chart(fig_user_item_heatmap, use_container_width=True)

with col1:
    # Brief explanation in a collapsible section
    with st.expander("About Collaborative Filtering"):
        st.markdown("""
        **Collaborative Filtering** recommends items based on similarity patterns.
        
        **Two main approaches:**
        - **User-User**: Finds similar users and recommends what they liked
        - **Item-Item**: Finds similar items to those a user already liked
        
        The algorithm assumes that users with similar past preferences will have similar future preferences.
        """)
    
    # Calculate similarity based on the selected filtering type
    def calculate_similarity(matrix, type='user'):
        if type == 'user':
            return 1 - distance.cdist(matrix, matrix, 'cosine')
        else:
            return 1 - distance.cdist(matrix.T, matrix.T, 'cosine')

    if filtering_type == 'User-User':
        similarity_matrix = calculate_similarity(user_item_matrix, type='user')
    else:
        similarity_matrix = calculate_similarity(user_item_matrix, type='item')

    # Display the similarity matrix as a heatmap
    st.markdown(f"<h3 class='section-header'>{filtering_type} Similarity Matrix</h3>", unsafe_allow_html=True)
    fig_heatmap = px.imshow(
        similarity_matrix, 
        text_auto='.2f', 
        aspect="auto", 
        color_continuous_scale='RdBu_r',
        labels=dict(color="Similarity")
    )
    
    if filtering_type == 'User-User':
        fig_heatmap.update_layout(
            xaxis_title='Users',
            yaxis_title='Users',
            xaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'{i+1}' for i in range(num_users)]),
            yaxis=dict(tickmode='array', tickvals=list(range(num_users)), ticktext=[f'{i+1}' for i in range(num_users)])
        )
    else:
        fig_heatmap.update_layout(
            xaxis_title='Items',
            yaxis_title='Items',
            xaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'{i+1}' for i in range(num_items)]),
            yaxis=dict(tickmode='array', tickvals=list(range(num_items)), ticktext=[f'{i+1}' for i in range(num_items)])
        )
    
    fig_heatmap.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Select a random user/item to demonstrate the recommendation
    if filtering_type == 'User-User':
        random_index = np.random.randint(num_users)
        
        # Find similar users
        similar_users_indices = np.argsort(-similarity_matrix[random_index])[1:k_value + 1]  # Exclude self
        similar_users_scores = similarity_matrix[random_index][similar_users_indices]
        
        # Recommend items that similar users have interacted with
        recommended_items = np.zeros(num_items, dtype=int)
        for user in similar_users_indices:
            recommended_items += user_item_matrix[user]
        recommended_items = np.where(recommended_items > 0, 1, 0)
        recommended_items = np.where((recommended_items - user_item_matrix[random_index]) > 0)[0]
        
        # Results display
        results_col1, results_col2 = st.columns(2)
        
        with results_col1:
            st.markdown(f"<div class='explanation'><span class='highlight'>For User {random_index + 1}:</span><br>", unsafe_allow_html=True)
            
            # Display similar users in a clean table
            similar_data = []
            for i, (user, score) in enumerate(zip(similar_users_indices, similar_users_scores)):
                similar_data.append({
                    "Rank": i+1,
                    "Similar User": f"User {user + 1}",
                    "Similarity": f"{score:.2f}"
                })
            st.markdown("<span class='highlight'>Similar Users:</span>", unsafe_allow_html=True)
            st.table(similar_data)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with results_col2:
            st.markdown("<div class='explanation'>", unsafe_allow_html=True)
            if len(recommended_items) > 0:
                st.markdown(f"<span class='highlight'>Recommended Items:</span><br>{', '.join([f'Item {item + 1}' for item in recommended_items])}", unsafe_allow_html=True)
            else:
                st.markdown("<span class='highlight'>No new items to recommend</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        random_index = np.random.randint(num_items)
        
        # Find similar items
        similar_items_indices = np.argsort(-similarity_matrix[random_index])[1:k_value + 1]  # Exclude self
        similar_items_scores = similarity_matrix[random_index][similar_items_indices]
        
        # Recommend to users who have interacted with similar items
        recommended_users = np.zeros(num_users, dtype=int)
        for item in similar_items_indices:
            recommended_users += user_item_matrix[:, item]
        recommended_users = np.where(recommended_users > 0, 1, 0)
        recommended_users = np.where((recommended_users - user_item_matrix[:, random_index]) > 0)[0]
        
        # Results display
        results_col1, results_col2 = st.columns(2)
        
        with results_col1:
            st.markdown(f"<div class='explanation'><span class='highlight'>For Item {random_index + 1}:</span><br>", unsafe_allow_html=True)
            
            # Display similar items in a clean table
            similar_data = []
            for i, (item, score) in enumerate(zip(similar_items_indices, similar_items_scores)):
                similar_data.append({
                    "Rank": i+1,
                    "Similar Item": f"Item {item + 1}",
                    "Similarity": f"{score:.2f}"
                })
            st.markdown("<span class='highlight'>Similar Items:</span>", unsafe_allow_html=True)
            st.table(similar_data)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with results_col2:
            st.markdown("<div class='explanation'>", unsafe_allow_html=True)
            if len(recommended_users) > 0:
                st.markdown(f"<span class='highlight'>Recommend to Users:</span><br>{', '.join([f'User {user + 1}' for user in recommended_users])}", unsafe_allow_html=True)
            else:
                st.markdown("<span class='highlight'>No new users to recommend to</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Visualize the recommendations with improved styling
    fig = go.Figure()

    # Create a better visualization grid
    for i in range(num_users):
        for j in range(num_items):
            marker_color = '#3366CC' if user_item_matrix[i, j] == 1 else '#E0E0E0'
            marker_size = 12 if user_item_matrix[i, j] == 1 else 8
            
            fig.add_trace(go.Scatter(
                x=[j + 1],
                y=[i + 1],
                mode='markers',
                marker=dict(color=marker_color, size=marker_size),
                hoverinfo='text',
                hovertext=f"User {i + 1}, Item {j + 1}: {'Interaction' if user_item_matrix[i, j] == 1 else 'No interaction'}"
            ))

    # Highlight recommendations
    if filtering_type == 'User-User':
        for item in recommended_items:
            fig.add_trace(go.Scatter(
                x=[item + 1],
                y=[random_index + 1],
                mode='markers',
                marker=dict(
                    color='#FF5733',
                    size=15,
                    line=dict(color='black', width=1),
                    symbol='star'
                ),
                hoverinfo='text',
                hovertext=f"Recommended: Item {item + 1} for User {random_index + 1}"
            ))
    else:
        for user in recommended_users:
            fig.add_trace(go.Scatter(
                x=[random_index + 1],
                y=[user + 1],
                mode='markers',
                marker=dict(
                    color='#FF5733',
                    size=15,
                    line=dict(color='black', width=1),
                    symbol='star'
                ),
                hoverinfo='text',
                hovertext=f"Recommended: Item {random_index + 1} for User {user + 1}"
            ))

    fig.update_layout(
        title='Recommendation Visualization',
        xaxis=dict(
            title='Items',
            tickmode='array',
            tickvals=list(range(1, num_items+1)),
            ticktext=[f'{i}' for i in range(1, num_items+1)]
        ),
        yaxis=dict(
            title='Users',
            tickmode='array',
            tickvals=list(range(1, num_users+1)),
            ticktext=[f'{i}' for i in range(1, num_users+1)]
        ),
        showlegend=False,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#F8F9FA'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Compact legend
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: -15px;">
        <div class="legend-item"><div class="legend-color" style="background-color: #3366CC;"></div>Existing interaction</div>
        <div class="legend-item" style="margin-left: 20px;"><div class="legend-color" style="background-color: #E0E0E0;"></div>No interaction</div>
        <div class="legend-item" style="margin-left: 20px;"><div class="legend-color" style="background-color: #FF5733;"></div>Recommendation</div>
    </div>
    """, unsafe_allow_html=True)
