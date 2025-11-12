import numpy as np
import io

# Activation Functions:
def sigmoid(x):
    """This is the activation function used in the nerual network"""
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    """Derivative of the sigmoid used for weight adjustment during backpropagation."""
    return x * (1 - x)

# Initialization Function:
def create_random_matrix(rows, cols):
    """Creates random weight matrices between -1 and 1."""
    return np.random.uniform(-1.0, 1.0, (rows, cols))


# Neural Network Functions:
def initialize_network(num_inputs, hidden_layers, num_outputs, bias_value):
    """Sets up initial weights and bias vectors for all layers."""
    # Initializes the structure of the network with input, hidden, and output layers
    layer_structure = [num_inputs] + hidden_layers + [num_outputs]

    # Creates a list of random weight matricies for each layer between the intput and output layers
    weights = [create_random_matrix(layer_structure[i], layer_structure[i + 1]) for i in range(len(layer_structure) - 1)]

    # Creates a list of bias vectors for each layer initialized to bias_value
    biases = [np.full((1, layer_structure[i + 1]), bias_value) for i in range(len(layer_structure) - 1)]

    # Returns the initialized weights and biases
    return weights, biases


def forward_pass(X, weights, biases):
    """Performs forward propagation through all layers."""
    # Creates a list to hold activations for each layer
    activations = [X]
    
    # Propagates input values through each of the layers with thier respective weights and biases
    for i in range(len(weights)):
        
        # Calculates the weighted sum plus bias
        z = np.dot(activations[-1], weights[i]) + biases[i]
        
        # Apply activation function & store activations for the layer
        a = sigmoid(z)
        activations.append(a)
        
    # Returns the list of activations for all of the layers
    return activations


def backpropagate(weights, biases, activations, y, learning_rate):
    """Updates weights and biases based on error."""
    # Calculate deltas (error terms)
    error = y - activations[-1] # Actual vs Predicted
    
    # Calculate the delta for the output layer
    delta = error * sigmoid_derivative(activations[-1]) # Output Layer Delta
    deltas = [delta] # List to hold deltas for each layer

    # Calculate the deltas for the hidden layers starting from the last hidden layer
    for i in reversed(range(len(weights) - 1)):
        
        # Calculate the delta for the current layer by transposing the weights of the next layer i.e. [x,y] --> [y,x]
        delta = np.dot(deltas[-1], weights[i + 1].T) * sigmoid_derivative(activations[i + 1])
        deltas.append(delta) # Append the delta to the list
    
    # Reverse to match the correct layer order
    deltas.reverse()

    # Update weights and biases
    for i in range(len(weights)): # Iterating forward through the layers? See comment below...
        # 1. Update the weights by calculating the gradient of the loss between activations and deltas
        # 2. Adjust by the learning rate to get the distance to move in the weight space
        # 3. Update the current weights by the calculated adjustment
        weights[i] += learning_rate * np.dot(activations[i].T, deltas[i])
        
        # 1. Update the bias by taking the total bias gradient across all samples in the batch
        # 2. Adjust by the learning rate to get the distance to move in the bias space
        # 3. Update the current biases by the calculated adjustment
        biases[i] += learning_rate * np.sum(deltas[i], axis=0, keepdims=True)

    # Return mean squared error to monitor training progress if below the threshold & updated weights and biases
    return np.mean(np.square(error)), weights, biases


def train_network(X, y, hidden_layers, num_outputs, learning_rate=0.1, bias_value=0.1, max_epochs=1000, error_threshold=0.01):
    """Trains a feedforward neural network."""
    log = [] # Used for logging outputs to the GUI
    # Get the number of variable input features from the training data & initialize the neural network
    num_inputs = X.shape[1]
    weights, biases = initialize_network(num_inputs, hidden_layers, num_outputs, bias_value)

    # Training loop
    for epoch in range(max_epochs):
        # Forward pass through the network
        activations = forward_pass(X, weights, biases)
        
        # Back propagate the error and update weights & biases
        mse, weights, biases = backpropagate(weights, biases, activations, y, learning_rate)

        # Print progress every 100 epochs or if the error is below the threshold
        if epoch % 100 == 0 or mse < error_threshold:
            log.append(f"Epoch {epoch+1}/{max_epochs} - Error: {mse:.6f}")

        # Stop training if the error is below the threshold
        if mse < error_threshold:
            break
    
    # Return the trained weights and biases
    return weights, biases, log

# Prediction Function:
def predict(X, weights, biases):
    """Runs the network in forward mode for new data."""
    # Perform a forward pass of the information through the network to get the output
    output = forward_pass(X, weights, biases)[-1] # Get the final output layer activations
    return np.round(output, 3) # Return rounded predictions for clarity


# Main Function for CLI:
if __name__ == "__main__":
    # Generate a simple binary dataset: 1 if x1 + x2 > 1, else 0
    X = np.random.rand(10, 2)
    y = np.array([[1] if sum(x) > 1 else [0] for x in X])

    print("Training Data:")
    for x_row, y_row in zip(X, y):
        print(f"Input: {x_row}, Target: {y_row}")

    # Network structure (2 inputs → 2 hidden layers → 1 output)
    hidden_layers = [3, 3]
    num_outputs = 1
    learning_rate = 0.5
    bias_value = 0.1
    max_epochs = 5000
    error_threshold = 0.01

    # Train
    weights, biases = train_network(
        X, y,
        hidden_layers=hidden_layers,
        num_outputs=num_outputs,
        learning_rate=learning_rate,
        bias_value=bias_value,
        max_epochs=max_epochs,
        error_threshold=error_threshold
    )

    # Predict on training data
    print("\nFinal Predictions:")
    predictions = predict(X, weights, biases)
    for x_row, pred, target in zip(X, predictions, y):
        print(f"Input: {x_row}, Predicted: {pred}, Target: {target}")