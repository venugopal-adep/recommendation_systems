import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.title("Cosine Similarity Explained")

st.markdown(r"""
**Cosine Similarity** is a measure of similarity between two non-zero vectors. It calculates the cosine of the angle between them, which gives a value between -1 and 1. A value of 1 means the vectors are maximally similar (pointing in the same direction), while -1 means they are maximally dissimilar (pointing in opposite directions). A value of 0 means the vectors are orthogonal/perpendicular, indicating they are completely different.

The formula for Cosine Similarity is:

$$\cos(\theta) = \frac{A \cdot B}{||A|| ||B||} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

Where $A$ and $B$ are the two vectors, and $\theta$ is the angle between them.
""")

# Create vectors using sliders in the sidebar
st.sidebar.subheader("Create Sample Vectors")
vec1_x = st.sidebar.slider("Vector 1 (X)", 0.0, 5.0, 1.0, key="vec1_x")
vec1_y = st.sidebar.slider("Vector 1 (Y)", 0.0, 5.0, 2.0, key="vec1_y")
vec1_z = st.sidebar.slider("Vector 1 (Z)", 0.0, 5.0, 3.0, key="vec1_z")
vec1 = np.array([vec1_x, vec1_y, vec1_z])

vec2_x = st.sidebar.slider("Vector 2 (X)", 0.0, 5.0, 4.0, key="vec2_x")
vec2_y = st.sidebar.slider("Vector 2 (Y)", 0.0, 5.0, 3.0, key="vec2_y")
vec2_z = st.sidebar.slider("Vector 2 (Z)", 0.0, 5.0, 2.0, key="vec2_z")
vec2 = np.array([vec2_x, vec2_y, vec2_z])

dot_product = np.dot(vec1, vec2)
magnitude1 = np.linalg.norm(vec1)
magnitude2 = np.linalg.norm(vec2)

cosine_similarity = dot_product / (magnitude1 * magnitude2)

st.markdown(f"""
**Vector 1:** {vec1}

**Vector 2:** {vec2}

**Dot Product:** {dot_product}

**Magnitude of Vector 1:** {magnitude1}

**Magnitude of Vector 2:** {magnitude2}

**Cosine Similarity:** {cosine_similarity}
""")

# Option for 2D or 3D visualization
visualization_mode = st.selectbox("Visualization Mode", ["2D", "3D"])

if visualization_mode == "2D":
    trace1 = go.Scatter(
        x=[0, vec1[0]],
        y=[0, vec1[1]],
        mode='lines',
        name='Vector 1',
        line=dict(color='red', width=4)
    )

    trace2 = go.Scatter(
        x=[0, vec2[0]],
        y=[0, vec2[1]],
        mode='lines',
        name='Vector 2',
        line=dict(color='blue', width=4)
    )

    layout = go.Layout(
        title='Cosine Similarity Visualization (2D)',
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        width=800,
        height=600
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

else:
    trace1 = go.Scatter3d(
        x=[0, vec1[0]],
        y=[0, vec1[1]],
        z=[0, vec1[2]],
        mode='lines',
        name='Vector 1',
        line=dict(color='red', width=4)
    )

    trace2 = go.Scatter3d(
        x=[0, vec2[0]],
        y=[0, vec2[1]],
        z=[0, vec2[2]],
        mode='lines',
        name='Vector 2',
        line=dict(color='blue', width=4)
    )

    layout = go.Layout(
        title='Cosine Similarity Visualization (3D)',
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z'),
            aspectratio=dict(x=1, y=1, z=0.7),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=-1.8, y=-1.8, z=1.125)
            )
        ),
        width=800,
        height=600
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The interactive visualization above shows the two vectors originating from the origin (0, 0, 0). The angle between them represents their Cosine Similarity. Vectors pointing in the same direction have a Cosine Similarity of 1, while vectors in opposite directions have a Cosine Similarity of -1. Orthogonal vectors have a Cosine Similarity of 0.

Play around with the sliders in the sidebar to create different vectors and observe how their Cosine Similarity changes based on their angle and magnitudes.
""")