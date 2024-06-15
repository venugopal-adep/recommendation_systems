import streamlit as st
import numpy as np
import plotly.graph_objs as go
from scipy.spatial import distance

st.title("Euclidean Distance Explained")

st.markdown(r"""
**Euclidean Distance** is a measure of the true straight line distance between two points in Euclidean space. 

The formula for Euclidean Distance between two points \(A(x_1, y_1)\) and \(B(x_2, y_2)\) is:

$$d(A, B) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

In 3D space, the formula extends to:

$$d(A, B) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$

Where \(d(A, B)\) is the Euclidean distance between points A and B.
""")

# Sidebar controls
st.sidebar.subheader("Controls")
dimension = st.sidebar.selectbox("Dimensions", ["2D", "3D"])
num_points = st.sidebar.slider("Number of Data Points", 5, 50, 10)
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

# Calculate Euclidean Distances
if dimension == "2D":
    points = np.column_stack((x_values, y_values))
else:
    points = np.column_stack((x_values, y_values, z_values))

distances = distance.cdist(points, points, 'euclidean')

# Display values on the sidebar
st.sidebar.subheader("Data Points")
st.sidebar.write("X Values:", x_values)
st.sidebar.write("Y Values:", y_values)
if dimension == "3D":
    st.sidebar.write("Z Values:", z_values)

st.sidebar.subheader("Euclidean Distance Matrix")
st.sidebar.write(distances)

# Plotting the data
if dimension == "2D":
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Data Points'
    )
    layout = go.Layout(
        title='Euclidean Distance Visualization (2D)',
        xaxis=dict(title='X Values'),
        yaxis=dict(title='Y Values'),
        width=800,
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)

    # Add lines for Euclidean distances
    for i in range(len(x_values)):
        for j in range(i + 1, len(x_values)):
            fig.add_trace(go.Scatter(
                x=[x_values[i], x_values[j]],
                y=[y_values[i], y_values[j]],
                mode='lines',
                line=dict(color='lightgrey', width=1),
                showlegend=False
            ))

else:
    trace = go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Data Points'
    )
    layout = go.Layout(
        title='Euclidean Distance Visualization (3D)',
        scene=dict(
            xaxis=dict(title='X Values'),
            yaxis=dict(title='Y Values'),
            zaxis=dict(title='Z Values')
        ),
        width=800,
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)

    # Add lines for Euclidean distances
    for i in range(len(x_values)):
        for j in range(i + 1, len(x_values)):
            fig.add_trace(go.Scatter3d(
                x=[x_values[i], x_values[j]],
                y=[y_values[i], y_values[j]],
                z=[z_values[i], z_values[j]],
                mode='lines',
                line=dict(color='lightgrey', width=1),
                showlegend=False
            ))

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The interactive visualization above shows the data points plotted on a scatter plot (2D or 3D) along with lines representing the Euclidean distances between them.

Use the "Number of Data Points" slider in the sidebar to adjust the number of data points and observe the changes in the Euclidean distances and the visualization. Use the "Regenerate Data" button to generate a new random dataset.
""")
