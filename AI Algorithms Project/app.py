# Use this link for reference https://docs.streamlit.io/develop/quick-reference/cheat-sheet
import streamlit as st

st.set_page_config(
    page_title="AI Algorithms Project",
    page_icon="🤖",
    layout="wide"     
)

st.title("AI Algorithms Project – Fall 2025")

# Sidebar navigation
algo = st.sidebar.radio(
    "Choose an Algorithm",
    ["Regression", "K-means Clustering", "Hidden Markov Model", "Neural Network"]
)

# Regression tab
if algo == "Regression":
    st.set_page_config(
    page_title="Regression Analysis",
    page_icon="📊",
    layout="wide"     
    )
    st.header("Linear Regression Analysis")
    x_vals = st.text_input("Enter X values (comma separated)", "1,2,3,4,5")
    y_vals = st.text_input("Enter Y values (comma separated)", "2,4,5,4,5")
    if st.button("Run Regression"):
        xs = [float(x) for x in x_vals.split(",")]
        ys = [float(y) for y in y_vals.split(",")]
        # TODO: Call your regression function here
        slope, intercept = 0.5, 1.2  # placeholder
        st.success(f"Slope: {xs}, Intercept: {ys}")
        st.line_chart({"data": ys})  # quick visualization

# K-means tab
elif algo == "K-means Clustering":
    st.set_page_config(
    page_title="K-means Clustering",
    page_icon="፨",
    layout="wide"     
    )
    st.header("K-means Clustering")
    st.write("Upload dataset or generate random points, then cluster...")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.file_uploader("Upload a CSV")
        if st.button("Run K-means"):
            st.success(f"Hidden Layers: {hidden_layers}, Temperature: {temperature}")
    with col2:
        hidden_layers = st.slider("Hidden Layers", min_value=1, max_value=10, value=3, step=1)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.01)
       
       
        
    st.line_chart({"data": [1, 2, 3, 4, 5]})  # placeholder for clustering result

# HMM tab
elif algo == "Hidden Markov Model":
    st.header("Hidden Markov Model")
    st.write("Upload transition/emission matrices, enter sequence...")

# Neural Network tab
elif algo == "Neural Network":
    st.header("Feedforward Neural Network")
    st.write("Configure layers, train, and show results...")