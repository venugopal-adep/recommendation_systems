import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.title("Pearson Correlation Explained")

st.markdown(r"""
**Pearson Correlation** is a measure of the linear relationship between two variables. It gives a value between -1 and 1, where 1 indicates a perfect positive linear relationship, 0 indicates no linear relationship, and -1 indicates a perfect negative linear relationship.

The formula for Pearson Correlation is:

$$r = \frac{\sum_{i=1}^{n} (x_i - \overline{x})(y_i - \overline{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \overline{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \overline{y})^2}}$$

Where $x_i$ and $y_i$ are the individual data points, and $\overline{x}$ and $\overline{y}$ are the means of the respective variables.
""")

# Sidebar controls
st.sidebar.subheader("Controls")
linearity_level = st.sidebar.slider("Linearity Level", -1.0, 1.0, 0.0)
regenerate_data = st.sidebar.button("Regenerate Data")

# Initialize or regenerate data
if regenerate_data or 'x_values' not in st.session_state:
    num_points = 50
    st.session_state.x_values = np.random.uniform(-10, 10, num_points)
    st.session_state.y_values = st.session_state.x_values * linearity_level + np.random.uniform(-10, 10 * (1 - abs(linearity_level)), num_points)

x_values = st.session_state.x_values
y_values = st.session_state.y_values

# Calculate Pearson Correlation
x_mean = np.mean(x_values)
y_mean = np.mean(y_values)
numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
denominator_x = np.sqrt(sum((x - x_mean) ** 2 for x in x_values))
denominator_y = np.sqrt(sum((y - y_mean) ** 2 for y in y_values))
denominator = denominator_x * denominator_y
pearson_correlation = numerator / denominator

st.markdown(f"""
**Data Points:**
X Values: {x_values}
Y Values: {y_values}

**Pearson Correlation:** {pearson_correlation:.3f}
""")

# Plotting the data
trace = go.Scatter(
    x=x_values,
    y=y_values,
    mode='markers',
    marker=dict(color='blue', size=10),
    name='Data Points'
)

layout = go.Layout(
    title='Pearson Correlation Visualization',
    xaxis=dict(title='X Values'),
    yaxis=dict(title='Y Values'),
    width=800,
    height=600
)

fig = go.Figure(data=[trace], layout=layout)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The interactive visualization above shows the data points plotted on a scatter plot. The Pearson Correlation value indicates the strength and direction of the linear relationship between the variables.

Use the "Linearity Level" slider in the sidebar to adjust the linearity of the data points and observe the changes in the Pearson Correlation value and the visualization. Use the "Regenerate Data" button to generate a new random dataset.
""")
