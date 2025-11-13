import itertools
import io

epsilon = 0.00001

def index(state, set_of_states):
    return set_of_states.index(state) # Return the position of a state in a list of states

def cartesian_product_of_sets(sets):
    return list(itertools.product(*sets)) # Get the cartesian product of a list of sets

def Hidden_Markov_Model_Path(set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector, emission_sequence):
    number_of_states = len(set_of_states) # Total number of states
    number_of_emissions = len(emission_sequence) # Total number of emissions
    get_path = True
    while get_path:
        # Ensure all emissions are valid before attempting to compute path
        if (valid_emission(emission_sequence, set_of_emissions)):
            transition_sets = [] # Build a list of possible states that could have produced each emission
            i = 1
            # For each emission in the sequence, find all candidate states
            while (i <= number_of_emissions):
                x = emission_sequence[i - 1]
                # Retrieve the set of states with non-zero probability of emitting x
                possible_set = emission_set(x, emission_matrix, set_of_emissions, number_of_states, set_of_states)
                transition_sets.append(possible_set)
                i += 1
            
            # Compute the cartesian product of all state sets
            cartesian_product = cartesian_product_of_sets(transition_sets)
            
            # Filter paths down to only those allowed by the transition probabilities
            set_of_potential_paths = []
            for path in cartesian_product:
                if (valid_transition(path, transition_matrix, set_of_states, initial_probability_vector)):
                    set_of_potential_paths.append(path)
            
            # Keep track of the highest probability state sequence
            log = []
            max_path = ("", 0.0)
            for path in set_of_potential_paths:
                probability = calculate_probability(path, emission_sequence, set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector)
                #probability_score_sequence.append((path, probability))
                log.append(f"The next probable sequence is: {path} with a probability of: {probability}")
                # Update the maximum if this path is the most likely so far
                if (probability > max_path[1]):
                    max_path = (path, probability)
            return max_path, log # Return the best sequence and all log lines

def valid_emission(emission_sequence, set_of_emissions):
    # Check every emission symbol in the input sequence
    for emission in emission_sequence:
        # If any emission is not part of the model's emission set, sequence is not valid
        if emission not in set_of_emissions:
            return False
    return True

def valid_transition(possible_transition_sequence, transition_matrix, set_of_states, initial_probability_vector):
    n = len(possible_transition_sequence) # Length of the proposed state path
    m = 1 # Start checking from the second state onward
    path_possible = True # Assume the path is valid until proven otherwise
    j = index(possible_transition_sequence[0], set_of_states) # Index of the initial state in the model
    
    # If the initial probability is nearly zero, path is impossible
    if (abs(initial_probability_vector[j]) < epsilon): 
        path_possible = False
    # Walk through the transition sequence from 0 ... n
    while (m < n and path_possible):
        # Previous state index
        i = index(possible_transition_sequence[m - 1], set_of_states)
        # Current state index
        j = index(possible_transition_sequence[m], set_of_states)
        # If transition probability from prev -> current is nearly zero, reject the path
        if (abs(transition_matrix[i][j]) < epsilon):
            path_possible = False
        m += 1 # Step to the next transition
    if path_possible:
        return True
    else:
        return False

def emission_set(emission, emission_matrix, set_of_emissions, number_of_states, set_of_states):
    j = index(emission, set_of_emissions) # Get column index for emission passed in
    possible_states = [] # List of states that can produce given emission
    
    # Check each state to see if it can emit the symbol
    for i in range(number_of_states):
        # If the probability of the emission is a valid possible state, append it to the list
        if (abs(emission_matrix[i][j]) >= epsilon):
            possible_states.append(set_of_states[i])
    return possible_states # Return all possible states
    

def calculate_probability(state_sequence, emission_sequence, set_of_states, set_of_emissions, transition_matrix, emission_matrix, initial_probability_vector):
    n = len(state_sequence) # Total number of steps in the sequence
    row_emissions = index(state_sequence[0], set_of_states) # Index of first state and first emission
    col_emissions = index(emission_sequence[0], set_of_emissions)
    
    # Initial probability when starting the sequence
    path_probability = initial_probability_vector[row_emissions] * emission_matrix[row_emissions][col_emissions]
    i = 1 # Start running from the second element onward
    # While the end of the path length has not been met
    while (i < n):
        j = i
        row_transmission = index(state_sequence[i - 1], set_of_states) # Previous state index
        col_transmission = index(state_sequence[j], set_of_states) # Current state index
        row_emission = col_transmission # Emission row corresponds to the current state
        col_emission = index(emission_sequence[j], set_of_emissions) # Index of the emission at position j
        transmission_probability = transition_matrix[row_transmission][col_transmission] # Transition probability
        emission_probability = emission_matrix[row_emission][col_emission] # Emission probability
        path_probability = path_probability * transmission_probability * emission_probability # Multiply into running path probability
        i += 1 # Next step
    return path_probability # Return the probability of the path

if __name__ == "__main__": # Hardcoded values for testing and debugging
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