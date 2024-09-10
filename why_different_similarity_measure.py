import streamlit as st
import plotly.express as px
import numpy as np

# Define functions for each similarity measure
def cosine_similarity(v1, v2):
    dot_product = sum(x * y for x, y in zip(v1, v2))
    mag_v1 = sum(x ** 2 for x in v1) ** 0.5
    mag_v2 = sum(y ** 2 for y in v2) ** 0.5
    if mag_v1 == 0 or mag_v2 == 0:  # Handle zero magnitude
        return 0
    return dot_product / (mag_v1 * mag_v2)

def pearson_correlation(v1, v2):
    mean_v1 = sum(v1) / len(v1)
    mean_v2 = sum(v2) / len(v2)
    centered_v1 = [x - mean_v1 for x in v1]
    centered_v2 = [y - mean_v2 for y in v2]
    numerator = sum(x * y for x, y in zip(centered_v1, centered_v2))
    denominator = (sum(x ** 2 for x in centered_v1) ** 0.5) * (
        sum(y ** 2 for y in centered_v2) ** 0.5
    )
    if denominator == 0:  # Handle zero denominator
        return 0
    return numerator / denominator

def euclidean_distance(v1, v2):
    return sum((x - y) ** 2 for x, y in zip(v1, v2)) ** 0.5

st.title("Choosing the Right Similarity Measure: An Interactive Guide")
st.markdown(
    """
Similarity measures are used in countless applications, from recommending movies to comparing user behavior. 

**But which similarity measure should you use?**  It depends on what you want to emphasize in your comparison.  

Let's explore some common measures and when they shine.
"""
)

# Interactive Example Section
with st.expander("Interactive Example: Shopping Lists"):

    st.subheader("Grocery Shopping: Cosine Similarity")
    st.write("Imagine two shoppers at a grocery store. We represent their purchases as vectors, where each item is a dimension and its value is the quantity purchased.")

    list1 = st.multiselect("Shopper A's List", ["Apples", "Bananas", "Oranges"])
    list1_quantities = []
    for item in list1:
        quantity = st.number_input(f"Quantity of {item} for Shopper A", min_value=0, value=1)
        list1_quantities.append(quantity)

    list2 = st.multiselect("Shopper B's List", ["Apples", "Bananas", "Oranges"])
    list2_quantities = []
    for item in list2:
        quantity = st.number_input(f"Quantity of {item} for Shopper B", min_value=0, value=1)
        list2_quantities.append(quantity)

    # Convert lists to vectors with zero padding for missing items (more efficient)
    all_items = sorted(set(list1 + list2))
    vec1 = [list1_quantities[list1.index(item)] if item in list1 else 0 for item in all_items]
    vec2 = [list2_quantities[list2.index(item)] if item in list2 else 0 for item in all_items]

    # Plot vectors and cosine similarity
    fig = px.scatter(x=[0, vec1[0]], y=[0, vec1[1]], title="Shopper A vs Shopper B")
    fig.add_scatter(x=[0, vec2[0]], y=[0, vec2[1]], name="Shopper B")
    if len(all_items) > 2:  # Add third dimension if it exists
        fig.add_scatter3d(
            x=[0, vec1[0]],
            y=[0, vec1[1]],
            z=[0, vec1[2]],
            name="Shopper A (3D)",
        )
        fig.add_scatter3d(
            x=[0, vec2[0]],
            y=[0, vec2[1]],
            z=[0, vec2[2]],
            name="Shopper B (3D)",
        )
    st.plotly_chart(fig)


    st.write(
        f"**Cosine Similarity:** {cosine_similarity(vec1, vec2):.2f}"
    )
    st.write(
        """
        Cosine similarity focuses on the **angle between vectors**, ignoring the magnitude (quantity).  
        Even if one shopper bought very little, as long as they bought similar items, the cosine similarity will be high. 
        """
    )

# Movie Rating Example
with st.expander("Interactive Example: Movie Ratings"):
    st.subheader("Movie Ratings: Pearson Correlation")
    st.write("Imagine you're comparing movie ratings between two friends.")

    movies = ["Movie A", "Movie B", "Movie C", "Movie D"]

    # Get individual movie ratings for Person 1
    ratings_person1 = []
    for movie in movies:
        rating = st.number_input(f"Person 1 rating for {movie}:", min_value=1, max_value=5, value=3)
        ratings_person1.append(rating)

    # Get individual movie ratings for Person 2
    ratings_person2 = []
    for movie in movies:
        rating = st.number_input(f"Person 2 rating for {movie}:", min_value=1, max_value=5, value=3)
        ratings_person2.append(rating)

    # Visualization with Plotly
    fig = px.scatter(
        x=ratings_person1,
        y=ratings_person2,
        labels={"x": "Person 1 Ratings", "y": "Person 2 Ratings"},
    )
    fig.update_traces(marker=dict(size=12))  # Increase marker size for clarity
    st.plotly_chart(fig)

    cosine_sim_movies = cosine_similarity(ratings_person1, ratings_person2)
    pearson_corr_movies = pearson_correlation(ratings_person1, ratings_person2)
    euclidean_dist_movies = euclidean_distance(ratings_person1, ratings_person2)

    st.write("Cosine Similarity:", cosine_sim_movies)
    st.write("Pearson Correlation:", pearson_corr_movies)
    st.write("Euclidean Distance (Dissimilarity):", euclidean_dist_movies)

    st.write(
        "In this case, **Pearson correlation** is often the preferred similarity measure for movie ratings as it accounts for linear relationships and the overall trend in preferences."
    )

# House Size Example
with st.expander("Interactive Example: House Sizes"):
    st.subheader("House Sizes: Euclidean Distance")
    st.write("Imagine you're comparing the size of houses based on area and number of bedrooms.")

    house_a_area = st.slider("House A Area (sq ft)", 500, 5000, 1500)
    house_b_area = st.slider("House B Area (sq ft)", 500, 5000, 2000)
    house_a_bedrooms = st.slider("House A Bedrooms", 1, 10, 3)
    house_b_bedrooms = st.slider("House B Bedrooms", 1, 10, 4)

    # Plot houses and Euclidean distance
    fig = px.scatter(x=[house_a_area], y=[house_a_bedrooms], title="House A vs House B")
    fig.add_scatter(x=[house_b_area], y=[house_b_bedrooms], name="House B")
    st.plotly_chart(fig)

    st.write(
        f"**Euclidean Distance (Dissimilarity):** {euclidean_distance([house_a_area, house_a_bedrooms], [house_b_area, house_b_bedrooms]):.2f}"
    )
    st.write(
        """
        Euclidean distance calculates the straight-line distance between points, 
        considering both the magnitude (area, bedrooms) and direction.
        """
    )
