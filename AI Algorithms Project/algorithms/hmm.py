import itertools
import pandas as pd
import numpy as np
import io

"""
TODO:
* Fix the input style to accept reading data from a file & Command line inputs
* Optimize algorithm a little bit and skim any unused variables
* THE CODE IS OUTPUTTING CORRECT RESULTS BUT COULD BE MADE MORE EFFICIENT
* Add comments and docustrings
* Pseudocode contains a while loop in the HMM function that reads emission sequence as input
    Will have to modify the HMM parameter to remove the emission as a parameter and read it inside the function
    Could move the iteration logic inside the init function for better structure to implement with WebGUI later for bonus
    ...reference "HMM Code Debugging" --> Homework...
"""



epsilon = 0.00001

def index(state, set_of_states):
    return set_of_states.index(state)

def cartesian_product_of_sets(sets):
    return list(itertools.product(*sets))

def Hidden_Markov_Model_Path(set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector, emission_sequence):
    number_of_states = len(set_of_states)
    number_of_emissions = len(emission_sequence)
    get_path = True
    while get_path:
        if (valid_emission(emission_sequence, set_of_emissions)):
            transition_sets = []
            i = 1
            while (i <= number_of_emissions):
                x = emission_sequence[i - 1]
                possible_set = emission_set(x, emission_matrix, set_of_emissions, number_of_states, set_of_states)
                transition_sets.append(possible_set)
                i += 1
            cartesian_product = cartesian_product_of_sets(transition_sets)
            set_of_potential_paths = []
            for path in cartesian_product:
                if (valid_transition(path, transition_matrix, set_of_states, initial_probability_vector)):
                    set_of_potential_paths.append(path)
            #probability_score_sequence = []
            max_path = ("", 0.0)
            for path in set_of_potential_paths:
                probability = calculate_probability(path, emission_sequence, set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector)
                #probability_score_sequence.append((path, probability))
                print("The next probable sequence is: ", path, " with a probability of: ", probability)
                if (probability > max_path[1]):
                    max_path = (path, probability)
            return max_path
                
            
            

def valid_emission(emission_sequence, set_of_emissions):
    for emission in emission_sequence:
        if emission not in set_of_emissions:
            return False
    return True

def valid_transition(possible_transition_sequence, transition_matrix, set_of_states, initial_probability_vector):
    n = len(possible_transition_sequence)
    m = 1
    path_possible = True
    j = index(possible_transition_sequence[0], set_of_states)
    
    if (abs(initial_probability_vector[j]) < epsilon): 
        path_possible = False
    while (m < n and path_possible):
        i = index(possible_transition_sequence[m - 1], set_of_states)
        j = index(possible_transition_sequence[m], set_of_states)
        if (abs(transition_matrix[i][j]) < epsilon):
            path_possible = False
        m += 1
    if path_possible:
        return True
    else:
        return False

def emission_set(emission, emission_matrix, set_of_emissions, number_of_states, set_of_states):
    j = index(emission, set_of_emissions)
    possible_states = []
    for i in range(number_of_states):
        if (abs(emission_matrix[i][j]) >= epsilon):
            possible_states.append(set_of_states[i])
    return possible_states
    

def calculate_probability(state_sequence, emission_sequence, set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector):
    n = len(state_sequence)
    row_emissions = index(state_sequence[0], set_of_states)
    col_emissions = index(emission_sequence[0], set_of_emissions)
    path_probability = initial_probability_vector[row_emissions] * emission_matrix[row_emissions][col_emissions]
    i = 1
    while (i < n):
        j = i
        row_transmission = index(state_sequence[i - 1], set_of_states)
        col_transmission = index(state_sequence[j], set_of_states)
        row_emission = col_transmission
        col_emission = index(emission_sequence[j], set_of_emissions)
        transmission_probability = transition_matrix[row_transmission][col_transmission]
        emission_probability = emission_matrix[row_emission][col_emission]
        path_probability = path_probability * transmission_probability * emission_probability
        i += 1
    return path_probability

if __name__ == "__main__":
    set_of_states    = ['S1','S2','S3','S4']
    set_of_emissions = ['A','B','C','D']

    transition_matrix = [
        [0.2, 0.6, 0.0, 0.2],
        [0.0, 0.2, 0.3, 0.5],
        [0.3, 0.2, 0.0, 0.5],
        [0.0, 0.6, 0.4, 0.0],
    ]
    emission_matrix = [
        [0.6, 0.4, 0.0, 0.0],
        [0.3, 0.2, 0.4, 0.1],
        [0.0, 0.0, 0.2, 0.8],
        [0.3, 0.4, 0.1, 0.3],
    ]
    initial_probability_vector = [0.4, 0.0, 0.5, 0.1]
    
    emission_sequence = ['A', 'C', 'B', 'D']

    best = Hidden_Markov_Model_Path(
        set_of_states,
        set_of_emissions,
        transition_matrix,
        emission_matrix,
        initial_probability_vector,
        emission_sequence
    )
    print("The most probable sequence is: ", best[0], " with a probability of: ", best[1])