import random
import pandas as pd
import numpy as np
import io

"""
TODO:
* Look at activation function and global threshold variable usage
* Add comments and docstrings
"""

def Feed_Forward_Neural_Network(input_vector, output_vector, training_sequence, perceptrons, num_hidden_layers, bias, max_epochs, adjustment_threshold, learning_rate, activation_threshold):
    input_sequence = training_sequence[0]
    output_sequence = training_sequence[1]
    input_hidden_matrix = create_random_matrix(len(input_sequence), perceptrons)
    hidden_output_matrix = create_random_matrix(perceptrons, len(output_sequence))
    
    for i in range(num_hidden_layers - 1):
        hidden_hidden_matricies = create_random_matrix(perceptrons, perceptrons)
    input_bias_vector = np.full(len(input_sequence), bias)
    hidden_bias_vector = np.full(perceptrons, bias)
    output_bias_vector = np.full(len(output_sequence), bias)
    
    iteration = 1
    adjusted = False
    while iteration <= max_epochs and not adjusted:
        for feature in input_sequence:
            input_vector[i] = 
    

def create_random_matrix(num_rows, num_columns):
    lower_bound = -1.0
    upper_bound = 1.0
    matrix = np.random.uniform(lower_bound, upper_bound, (num_rows, num_columns))
    return matrix

def adjust_weight(target_sequence, computed_sequence, matricies, maximum_count, error_threshold, learning_rate, hidden_vector_size, num_hidden_layers, num_output_perceptrons, hidden_bias_vector, output_bias_vector, activation_threshold):
    current_layer = num_hidden_layers - 1
    prev_error = 9999999
    count = 1
    epsilon = 0.00001
    while current_layer >= 0 and count <= maximum_count:
        value_differences = computed_sequence - target_sequence
        input_difference_values = []
        m = len(value_differences)
        for i in range(m):
            if value_differences[i] > error_threshold:
                input_difference_values.append((i, value_differences[i]))
        set_of_edges = get_edges(num_hidden_layers, current_layer, input_difference_values, matricies, epsilon)
        modified_edges = modify_edge_weights(set_of_edges, current_layer, value_differences, learning_rate)
        modified_matrix = insert_modified_edges(modified_edges, current_layer, matricies)
        computed_sequence = process_hidden_layers(current_layer, 0, num_hidden_layers - 1, hidden_bias_vector, output_bias_vector, modified_matrix, activation_threshold)
        error = np.sqrt(np.sum((computed_sequence - target_sequence) ** 2))
        if error < prev_error or error < error_threshold:
            updated_matrix = modified_matrix
            if error < error_threshold:
                adjusted = True
                break
            else:
                prev_error = error
        count += 1
    if adjusted or count >= maximum_count:
        return
    else:
        current_layer -= 1


def threshold_fire(cumulative_vector, activation_threshold):
    output_vector = np.zeros(len(cumulative_vector))
    for i in range(len(cumulative_vector)):
        if cumulative_vector[i] > activation_threshold:
            output_vector[i] = 1 / (1 + np.exp(-cumulative_vector[i]))
        else:
            output_vector[i] = 0
    return output_vector

def process_hidden_layers(initial_output_vector, start_hidden_layer, last_hidden_layer, hidden_bias_vector, output_bias_vector, matricies, activation_threshold):
    output_vector = initial_output_vector
    for hidden_layer in range(start_hidden_layer, last_hidden_layer):
        input_vector = np.dot(matricies[hidden_layer], output_vector) + hidden_bias_vector
        output_vector = threshold_fire(input_vector, activation_threshold)
    final_input_vector = np.dot(matricies[last_hidden_layer], output_vector) + output_bias_vector
    final_output_vector = threshold_fire(final_input_vector, activation_threshold)
    return final_output_vector

def get_edges(hidden_layer, current_layer, edges, matricies, epsilon=0.00001):
    if current_layer == hidden_layer:
        return edges
    else:
        source_nodes = edges[hidden_layer - 1]
        destination_nodes = edges[hidden_layer + 1]
        current_matrix = matricies[current_layer - 1]
        current_edges = []
        for row in source_nodes:
            for column in destination_nodes:
                weight = current_matrix[row][column]
                if abs(weight) > epsilon:
                    current_edges.append((row, column, weight))
        current_layer -= 1
        get_edges(hidden_layer, current_layer, current_edges, matricies, epsilon)
            

def modify_edge_weights(edges, hidden_layer, value_difference, learning_rate):
    updated_weights = []
    for row, column, weight in edges:
        new_weight = weight * (1 + learning_rate * value_difference[row])
        updated_weights.append((row, column, new_weight))
    return updated_weights

def insert_modified_edges(modified_edges, hidden_layer_index, matricies):
    modified_matrix = []
    sorted_modified_edges = sorted(modified_edges, key=lambda x: (x[0], x[1]))
    for edge in sorted_modified_edges:
        row = edge[0]
        column = edge[1]
        weight = edge[2]
        modified_matrix[row][column] = weight
    matricies[hidden_layer_index] = modified_matrix
    return matricies

if __name__ == "__main__":
    perceptrons = input("Enter the number of perceptrons in each hidden layer: ")
    num_hidden_layers = input("Enter the number of hidden layers: ")
    bias = input("Enter the perceptron bias value: ")
    max_epochs = input("Enter the maximum number of trainins epochs: ")
    adjustment_threshold = input("Enter the threshold for neural netwrok adjustments: ")
    learning_rate = input("Enter the learning rate: ")
    