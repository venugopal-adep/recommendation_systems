import streamlit as st
import numpy as np
import plotly.graph_objs as go
from scipy.spatial import distance

st.title("Nearest Neighbors Algorithm")

st.markdown(r"""
This algorithm finds the top k nearest items/users based on similarity between the items/users, which means the new item will be recommended based on the similarity between the two items/users.

### Steps:
1. For each point in the data do the following:
    - Calculate the distance between the test item and each training item with the help of any of the distance methods, namely: Euclidean, Manhattan, cosine, etc. The most commonly used method to calculate this distance is the cosine method in recommendation systems.
    - Now, based on the distance value, sort them in ascending order.
2. We need to choose the value of k, i.e., the nearest k items/movies you want to recommend.
    - Next, it will choose the top k rows from the sorted array.
    - Print the top k items, which are similar to a particular item.
""")

# Sidebar controls
st.sidebar.subheader("Controls")
dimension = st.sidebar.selectbox("Dimensions", ["2D", "3D"])
distance_metric = st.sidebar.selectbox("Distance Metric", ["euclidean", "cityblock", "cosine"])
num_points = st.sidebar.slider("Number of Data Points", 10, 50, 20)
k_value = st.sidebar.slider("Value of k", 1, 10, 5)
regenerate_data = st.sidebar.button("Regenerate Data")

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

# Plotting the data
if dimension == "2D":
    trace_points = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Data Points'
    )

    trace_test_point = go.Scatter(
        x=[test_point[0]],
        y=[test_point[1]],
        mode='markers',
        marker=dict(color='red', size=12),
        name='Test Point'
    )

    layout = go.Layout(
        title=f'Nearest Neighbors Visualization (2D) - Metric: {distance_metric}',
        xaxis=dict(title='X Values'),
        yaxis=dict(title='Y Values'),
        width=800,
        height=600
    )

    fig = go.Figure(data=[trace_points, trace_test_point], layout=layout)

    # Add lines for nearest neighbors
    for idx in nearest_indices:
        fig.add_trace(go.Scatter(
            x=[test_point[0], x_values[idx]],
            y=[test_point[1], y_values[idx]],
            mode='lines',
            line=dict(color='lightgrey', width=1),
            showlegend=False
        ))

else:
    trace_points = go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Data Points'
    )

    trace_test_point = go.Scatter3d(
        x=[test_point[0]],
        y=[test_point[1]],
        z=[test_point[2]],
        mode='markers',
        marker=dict(color='red', size=12),
        name='Test Point'
    )

    layout = go.Layout(
        title=f'Nearest Neighbors Visualization (3D) - Metric: {distance_metric}',
        scene=dict(
            xaxis=dict(title='X Values'),
            yaxis=dict(title='Y Values'),
            zaxis=dict(title='Z Values')
        ),
        width=800,
        height=600
    )

    fig = go.Figure(data=[trace_points, trace_test_point], layout=layout)

    # Add lines for nearest neighbors
    for idx in nearest_indices:
        fig.add_trace(go.Scatter3d(
            x=[test_point[0], x_values[idx]],
            y=[test_point[1], y_values[idx]],
            z=[test_point[2], z_values[idx]],
            mode='lines',
            line=dict(color='lightgrey', width=1),
            showlegend=False
        ))

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
**Test Point:** {test_point}

**Nearest Neighbors (k={k_value}):**
{points[nearest_indices]}
""")
