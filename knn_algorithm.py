import streamlit as st
import numpy as np
import plotly.graph_objs as go
from scipy.spatial import distance

# Page configuration
st.set_page_config(page_title="Nearest Neighbors Algorithm", layout="wide")

# Title with custom styling
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Nearest Neighbors Algorithm</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #757575;'>Developed by: Venugopal Adep</h4>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Parameters")
    dimension = st.radio("Dimensions", ["2D", "3D"])
    # Fixed distance metric without dropdown
    distance_metric = "euclidean"
    num_points = st.slider("Number of Data Points", 10, 50, 20)
    k_value = st.slider("Value of k", 1, 10, 5)
    regenerate_data = st.button("Regenerate Data")

with col1:
    # Algorithm explanation in a cleaner format
    with st.expander("Algorithm Explanation"):
        st.markdown("""
        This algorithm finds the top k nearest items/users based on similarity.
        
        **Steps:**
        1. Calculate the distance between test item and each training item
        2. Sort items by distance in ascending order
        3. Select the top k items as recommendations
        
        Currently using **Euclidean distance** metric.
        """)
    
    # Initialize or regenerate data
    if regenerate_data or 'x_values' not in st.session_state:
        st.session_state.x_values = np.random.uniform(-10, 10, num_points)
        st.session_state.y_values = np.random.uniform(-10, 10, num_points)
        if dimension == "3D":
            st.session_state.z_values = np.random.uniform(-10, 10, num_points)
        else:
            st.session_state.z_values = None

    x_values = st.session_state.x_values
    y_values = st.session_state.y_values
    z_values = st.session_state.z_values

    # Combine points into an array
    if dimension == "2D":
        points = np.column_stack((x_values, y_values))
    else:
        points = np.column_stack((x_values, y_values, z_values))

    # Select a random test point
    test_point = np.random.uniform(-10, 10, 3 if dimension == "3D" else 2)

    # Calculate distances
    distances = distance.cdist([test_point], points, metric=distance_metric)[0]

    # Get the indices of the k nearest neighbors
    nearest_indices = distances.argsort()[:k_value]

    # Plotting with improved styling
    if dimension == "2D":
        trace_points = go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers',
            marker=dict(color='#3366CC', size=10, opacity=0.7),
            name='Data Points'
        )

        trace_test_point = go.Scatter(
            x=[test_point[0]],
            y=[test_point[1]],
            mode='markers',
            marker=dict(color='#FF5733', size=14, symbol='star'),
            name='Test Point'
        )

        layout = go.Layout(
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(title='X Values', showgrid=True, gridcolor='#E0E0E0'),
            yaxis=dict(title='Y Values', showgrid=True, gridcolor='#E0E0E0'),
            plot_bgcolor='#F8F9FA',
            height=500
        )

        fig = go.Figure(data=[trace_points, trace_test_point], layout=layout)

        # Add lines for nearest neighbors
        for idx in nearest_indices:
            fig.add_trace(go.Scatter(
                x=[test_point[0], x_values[idx]],
                y=[test_point[1], y_values[idx]],
                mode='lines',
                line=dict(color='#FF5733', width=2, dash='dot'),
                showlegend=False
            ))

    else:
        trace_points = go.Scatter3d(
            x=x_values,
            y=y_values,
            z=z_values,
            mode='markers',
            marker=dict(color='#3366CC', size=6, opacity=0.7),
            name='Data Points'
        )

        trace_test_point = go.Scatter3d(
            x=[test_point[0]],
            y=[test_point[1]],
            z=[test_point[2]],
            mode='markers',
            marker=dict(color='#FF5733', size=10, symbol='diamond'),
            name='Test Point'
        )

        layout = go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            scene=dict(
                xaxis=dict(title='X Values', showgrid=True, gridcolor='#E0E0E0'),
                yaxis=dict(title='Y Values', showgrid=True, gridcolor='#E0E0E0'),
                zaxis=dict(title='Z Values', showgrid=True, gridcolor='#E0E0E0'),
                bgcolor='#F8F9FA'
            ),
            height=500
        )

        fig = go.Figure(data=[trace_points, trace_test_point], layout=layout)

        # Add lines for nearest neighbors
        for idx in nearest_indices:
            fig.add_trace(go.Scatter3d(
                x=[test_point[0], x_values[idx]],
                y=[test_point[1], y_values[idx]],
                z=[test_point[2], z_values[idx]],
                mode='lines',
                line=dict(color='#FF5733', width=3),
                showlegend=False
            ))

    st.plotly_chart(fig, use_container_width=True)

    # Results in a cleaner format
    st.markdown(f"""
    <div style='background-color: #F0F7FF; padding: 15px; border-radius: 5px;'>
        <h4>Results</h4>
        <p><strong>Test Point:</strong> [{', '.join([f'{x:.2f}' for x in test_point])}]</p>
        <p><strong>Nearest {k_value} Neighbors:</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display nearest neighbors in a clean table
    neighbor_data = []
    for i, idx in enumerate(nearest_indices):
        neighbor = points[idx]
        dist = distances[idx]
        neighbor_data.append({
            "Neighbor": i+1,
            "Coordinates": f"[{', '.join([f'{x:.2f}' for x in neighbor])}]",
            "Distance": f"{dist:.4f}"
        })
    
    st.table(neighbor_data)
