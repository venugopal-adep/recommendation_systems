import streamlit as st
import pandas as pd
import json
import gzip
import plotly.express as px
from collections import Counter
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Amazon Fashion Insights", page_icon="👗", layout="wide")

# Custom CSS to improve aesthetics
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 20px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    url = "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/categoryFiles/AMAZON_FASHION.json.gz"
    
    # Download the file
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to download the file. Status code: {response.status_code}")
        return pd.DataFrame()

    # Read the gzipped JSON data
    with gzip.open(BytesIO(response.content)) as f:
        data = [json.loads(line) for line in f]

    return pd.DataFrame(data)

# Load and preprocess the data
with st.spinner("Loading data... This may take a few moments."):
    df = load_data()

if df.empty:
    st.error("Failed to load the data. Please check your internet connection and try again.")
    st.stop()

df = df[['overall', 'verified', 'reviewerID', 'asin', 'style', 'reviewerName', 'reviewText', 'summary', 'reviewTime']]
df['reviewTime'] = pd.to_datetime(df['reviewTime'])
filtered_df = df[(df['verified'] == True) & (~df['overall'].isnull())]

# Streamlit app
st.title("🛍️ Amazon Fashion Insights Dashboard")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "⭐ Ratings", "👥 Reviewers", "📈 Trends", "🔍 Product Search"])

with tab1:
    st.header("Dataset Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reviews", f"{len(filtered_df):,}")
    with col2:
        st.metric("Unique Products", f"{filtered_df['asin'].nunique():,}")
    with col3:
        st.metric("Unique Reviewers", f"{filtered_df['reviewerID'].nunique():,}")
    
    st.subheader("Most Common Words in Reviews")
    def get_top_words(text, n=100):
        words = text.str.cat(sep=' ').lower().split()
        return Counter(words).most_common(n)

    top_words = get_top_words(filtered_df['reviewText'].dropna(), n=100)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_words))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

with tab2:
    st.header("Rating Distribution")
    rating_counts = filtered_df['overall'].value_counts().sort_index()
    fig_ratings = px.bar(x=rating_counts.index, y=rating_counts.values, 
                         labels={'x': 'Rating', 'y': 'Count'},
                         color=rating_counts.values,
                         color_continuous_scale=px.colors.sequential.Viridis)
    fig_ratings.update_layout(title='Distribution of Ratings')
    st.plotly_chart(fig_ratings, use_container_width=True)

    # Average rating over time
    filtered_df['year_month'] = filtered_df['reviewTime'].dt.to_period('M')
    avg_rating_over_time = filtered_df.groupby('year_month')['overall'].mean().reset_index()
    avg_rating_over_time['year_month'] = avg_rating_over_time['year_month'].astype(str)
    
    fig_avg_rating = px.line(avg_rating_over_time, x='year_month', y='overall', 
                             labels={'year_month': 'Date', 'overall': 'Average Rating'},
                             title='Average Rating Over Time')
    st.plotly_chart(fig_avg_rating, use_container_width=True)

with tab3:
    st.header("Top Reviewers")
    top_reviewers = filtered_df['reviewerID'].value_counts().head(10)
    fig_top_reviewers = px.bar(x=top_reviewers.index, y=top_reviewers.values, 
                               labels={'x': 'Reviewer ID', 'y': 'Number of Reviews'},
                               color=top_reviewers.values,
                               color_continuous_scale=px.colors.sequential.Plasma)
    fig_top_reviewers.update_layout(title='Top 10 Reviewers')
    st.plotly_chart(fig_top_reviewers, use_container_width=True)

    # Reviewer activity heatmap
    filtered_df['year_month'] = filtered_df['reviewTime'].dt.to_period('M').astype(str)
    reviewer_activity = filtered_df.groupby(['reviewerID', 'year_month']).size().reset_index(name='count')
    reviewer_activity_pivot = reviewer_activity.pivot(index='reviewerID', columns='year_month', values='count').fillna(0)
    
    fig_heatmap = px.imshow(reviewer_activity_pivot, 
                            labels=dict(x="Date", y="Reviewer ID", color="Number of Reviews"),
                            title="Reviewer Activity Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab4:
    st.header("Review Trends")
    filtered_df['year_month'] = filtered_df['reviewTime'].dt.to_period('M').astype(str)
    reviews_over_time = filtered_df.groupby('year_month').size().reset_index(name='count')
    
    fig_time = px.line(reviews_over_time, x='year_month', y='count', 
                       labels={'year_month': 'Date', 'count': 'Number of Reviews'},
                       title='Number of Reviews Over Time')
    st.plotly_chart(fig_time, use_container_width=True)

    # Seasonal trends
    filtered_df['month'] = filtered_df['reviewTime'].dt.month
    monthly_trends = filtered_df.groupby('month')['overall'].agg(['mean', 'count']).reset_index()
    monthly_trends['month'] = pd.to_datetime(monthly_trends['month'], format='%m').dt.strftime('%B')
    
    fig_seasonal = px.line(monthly_trends, x='month', y=['mean', 'count'], 
                           labels={'value': 'Value', 'variable': 'Metric'},
                           title='Seasonal Trends in Ratings and Review Count')
    fig_seasonal.update_layout(xaxis={'categoryorder':'array', 'categoryarray':monthly_trends['month']})
    st.plotly_chart(fig_seasonal, use_container_width=True)

with tab5:
    st.header("Search for a Product")
    search_asin = st.text_input("Enter product ASIN:")
    if search_asin:
        product_reviews = filtered_df[filtered_df['asin'] == search_asin]
        if not product_reviews.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Number of Reviews", len(product_reviews))
            with col2:
                st.metric("Average Rating", f"{product_reviews['overall'].mean():.2f}")
            
            # Rating distribution for the product
            product_rating_counts = product_reviews['overall'].value_counts().sort_index()
            fig_product_ratings = px.bar(x=product_rating_counts.index, y=product_rating_counts.values, 
                                         labels={'x': 'Rating', 'y': 'Count'},
                                         title='Rating Distribution for This Product',
                                         color=product_rating_counts.values,
                                         color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig_product_ratings, use_container_width=True)
            
            # Display a sample of reviews
            st.subheader("Sample Reviews")
            sample_reviews = product_reviews.sample(min(5, len(product_reviews)))
            for _, review in sample_reviews.iterrows():
                st.write(f"Rating: {'⭐' * int(review['overall'])}")
                st.write(f"Review: {review['reviewText']}")
                st.write("---")
        else:
            st.warning("No reviews found for this product.")

st.sidebar.header("About the Dataset")
st.sidebar.write("""
This dataset contains Amazon Fashion product reviews. It includes information such as:
- Overall rating
- Verified purchase status
- Reviewer ID
- Product ASIN (Amazon Standard Identification Number)
- Review text and summary
- Review timestamp

The analysis provides insights into rating distributions, top reviewers, review trends over time, and common words used in reviews.
""")

st.sidebar.header("How to Use")
st.sidebar.write("""
1. Navigate through the tabs to explore different aspects of the data.
2. Use the Product Search tab to look up specific products by their ASIN.
3. Hover over charts for more detailed information.
4. Enjoy exploring Amazon Fashion insights!
""")
