# AI Algorithms Project – Streamlit Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import regression
import hmm
import ann
import kmeans

# Write the header of the page
st.set_page_config(page_title="AI Algorithms Project", page_icon="🤖", layout="wide")
st.title("🤖 AI Algorithms Project – Fall 2025")
st.write("This interactive app demonstrates four key AI algorithms: Regression, K-Means Clustering, Hidden Markov Models, and Neural Networks.")

# Sidebar navigation
algo = st.sidebar.radio(
    "🧠 Choose an Algorithm",
    ["Regression", "K-Means Clustering", "Hidden Markov Model", "Neural Network"]
)


# LINEAR REGRESSION
if algo == "Regression":
    st.header("📊 Linear Regression Analysis")

    upload = st.file_uploader("Upload CSV or Excel (must contain `x` and `y` columns)", type=["csv", "xlsx"])
    manual_input = st.text_area("Or manually enter data (format: 1,2 2,3 3,4)", "")

    x_pred = st.number_input("Enter X value to predict Y (optional)", value=0.0)

    if st.button("Run Regression"):
        try:
            if upload:
                data_points = regression.parse_data(upload)
            elif manual_input:
                data_points = regression.parse_data(manual_input)
            else:
                st.warning("Please upload a file or enter data manually.")
                st.stop()

            slope, intercept, log = regression.regression_analysis(data_points)
            st.code(log)
            st.success(f"Slope: `{slope:.3f}`, Intercept: `{intercept:.3f}`")

            if x_pred:
                y_pred = slope * x_pred + intercept
                st.info(f"Predicted Y for X={x_pred}: **{y_pred:.3f}**")

            df = pd.DataFrame(data_points, columns=["x", "y"])
            fig, ax = plt.subplots()
            ax.scatter(df["x"], df["y"], color="blue", label="Data")
            ax.plot(df["x"], slope * df["x"] + intercept, color="red", label="Best Fit Line")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")


# K-MEANS CLUSTERING
elif algo == "K-Means Clustering":
    st.header("፨ K-Means Clustering")

    mode = st.radio("Input Mode", ["Upload Data", "Manual Input", "Random Data"])
    num_clusters = st.number_input("Number of Clusters (k)", 1, 10, 3)
    max_iterations = st.number_input("Max Iterations", 10, 1000, 100)
    tolerance = st.number_input("Convergence Tolerance", 0.0001, 1.0, 0.01, format="%.4f")

    if mode == "Upload Data":
        upload = st.file_uploader("Upload CSV or Excel (must have two columns for x,y)", type=["csv", "xlsx"])
    elif mode == "Manual Input":
        manual = st.text_area("Enter data points (format: 1,2 2,3 3,4)")
    else:
        num_points = st.slider("Number of random data points", 10, 200, 30)

    if st.button("Run K-Means"):
        try:
            if mode == "Upload Data" and upload:
                data_points = kmeans.parse_data(upload)
            elif mode == "Manual Input" and manual:
                data_points = kmeans.parse_data(manual)
            elif mode == "Random Data":
                x, y = np.random.uniform(0, 20, num_points), np.random.uniform(0, 20, num_points)
                data_points = list(zip(x, y))
            else:
                st.warning("Please provide valid data.")
                st.stop()

            # Run algorithm
            log = kmeans.kmeans(data_points, num_clusters, max_iterations, tolerance)
            st.text_area("K-Means Progress", "\n".join(log), height=400)

            # Graph data points
            df = pd.DataFrame(data_points, columns=["x", "y"])
            st.scatter_chart(df)

        except Exception as e:
            st.error(f"Error: {e}")


# HIDDEN MARKOV MODEL
elif algo == "Hidden Markov Model":
    st.header("🔁 Hidden Markov Model (HMM)")

    st.write("Enter parameters below or use defaults to test:")
    states = st.text_input("States (comma-separated)", "S1,S2,S3,S4").split(",")
    emissions = st.text_input("Emissions (comma-separated)", "A,B,C,D").split(",")
    emission_sequence = st.text_input("Emission Sequence (comma-separated)", "A,C,B,D").split(",")

    st.markdown("#### Matrices (comma-separated rows, semicolon-separated lines)")
    transition_input = st.text_area("Transition Matrix", "0.2,0.6,0.0,0.2;0.0,0.2,0.3,0.5;0.3,0.2,0.0,0.5;0.0,0.6,0.4,0.0")
    emission_input = st.text_area("Emission Matrix", "0.6,0.4,0.0,0.0;0.3,0.2,0.4,0.1;0.0,0.0,0.2,0.8;0.3,0.4,0.1,0.3")
    initial_input = st.text_input("Initial Probabilities", "0.4,0.0,0.5,0.1")

    if st.button("Run HMM"):
        try:
            transition = [list(map(float, row.split(","))) for row in transition_input.split(";")]
            emission = [list(map(float, row.split(","))) for row in emission_input.split(";")]
            initial = list(map(float, initial_input.split(",")))

            best, log = hmm.Hidden_Markov_Model_Path(states, emissions, transition, emission, initial, emission_sequence)
            st.text_area("Probable Sequences", "\n".join(log), height=300)
            st.success(f"Most probable path: {best[0]} with probability {best[1]:.5f}")

        except Exception as e:
            st.error(f"Error: {e}")


# ARTIFICIAL NEURAL NETWORK
elif algo == "Neural Network":
    st.header("🧬 Feedforward Neural Network (ANN)")

    st.write("This example uses simple binary classification (1 if x1+x2 > 1 else 0).")
    num_samples = st.slider("Number of training samples", 5, 100, 10)
    hidden_layers_input = st.text_input("Hidden Layers (comma-separated)", "3,3")
    learning_rate = st.number_input("Learning Rate", 0.01, 1.0, 0.5, step=0.01)
    bias_value = st.number_input("Bias Value", -1.0, 1.0, 0.1, step=0.1)
    max_epochs = st.number_input("Max Epochs", 100, 10000, 5000)
    error_threshold = st.number_input("Error Threshold", 0.0001, 1.0, 0.01)

    if st.button("Train Network"):
        try:
            X = np.random.rand(num_samples, 2)
            y = np.array([[1] if sum(x) > 1 else [0] for x in X])
            hidden_layers = [int(n) for n in hidden_layers_input.split(",")]

            st.info("Training network... (check logs for progress)")
            weights, biases, log = ann.train_network(
                X, y,
                hidden_layers=hidden_layers,
                num_outputs=1,
                learning_rate=learning_rate,
                bias_value=bias_value,
                max_epochs=max_epochs,
                error_threshold=error_threshold
            )
            st.text_area("Training Progress", "\n".join(log), height=300)
            st.success("Neural Network Training Success!")

            preds = ann.predict(X, weights, biases)
            results = pd.DataFrame({
                "x1": X[:,0], "x2": X[:,1],
                "Predicted": preds.flatten(),
                "Target": y.flatten()
            })
            st.dataframe(results)

            st.line_chart(preds.flatten())

        except Exception as e:
            st.error(f"Error: {e}")