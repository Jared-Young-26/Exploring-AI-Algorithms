import random
import pandas as pd
import numpy as np
import io

    """
    TODO: 
    * Zero Division errors are common; might need some sort of validation step for seed points that are empty to skip over
    """




def parse_data(content):
    data_points = []
    
    # Case 1: Check if the content is a file-life object or a file path
    if hasattr(content, 'read') or (isinstance(content, str) and (content.endswith('.csv') or content.endswith('.xlsx'))):
        try:    
            if hasattr(content, 'name') and content.endswith('.csv'): # Comes from an uploaded CSV file
                df = pd.read_csv(content)
            elif hasattr(content, 'name') and content.endswith('.xlsx'): # Comes from an uploaded Excel file
                df = pd.read_excel(content)
            elif isinstance(content, str) and content.endswith('.csv'): # Comes from a file path to a CSV file
                df = pd.read_csv(content) 
            elif isinstance(content, str) and content.endswith('.xlsx'): # Comes from a file path to an Excel file
                df = pd.read_excel(content) 
            else: 
                raise ValueError("Please provide a valid CSV or Excel file.")
        
        except Exception as e:
            raise ValueError(f"Error reading the file: {e}")
        
        # Check if the DataFrame has the required number of columns
        if {'x', 'y'}.issubset(df.columns):
            x, y = df['x'], df['y'] # Assuming that the label columns for x and y are 'x' and 'y'
        else:
            x, y = df.iloc[:, 0], df.iloc[:, 1] # Assuming that the label columns for x and y are absent
    
    # Case 2: Check if content is a string that was input directly i.e. doesn't match the file path pattern
    elif isinstance(content, str):
        df = pd.read_csv(io.StringIO(content), header=None) # Reads the string input as a CSV without headers
        x, y = df.iloc[:,0], df.iloc[:,1] # Assigns the first column X and the second column Y
    else:
        raise ValueError("Invalid input type. Please provide a file path, upload a file in the GUI, or input data as a string.")   
    
    # Convert string data to numeric, forcing errors to Not a Number
    x = pd.to_numeric(x, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')
    clean_data = pd.DataFrame({'x': x, 'y': y}).dropna() # Remove the rows with Not a Number values
    
    # Create the list of tuples for data points and return the formatted result
    data_points = list(zip(clean_data['x'], clean_data['y']))
    return data_points

def kmeans(data_points, num_clusters, max_iterations, tolerance):
    """
    A placeholder function for K-Means clustering algorithm.
    This function would typically include the implementation of the K-Means algorithm.
    """
    total_points = len(data_points)
    seed_points, radius = generate_seed_points(data_points, num_clusters)
    count = 1 # Initialize the counter used to terminate after max number of iterations
    # Boolean variable, stabilized, is used t check for terminating the execution
    # The variable becomes true when centroids of clusters don't move beyond a threshold
    stabilized = False
    print(seed_points, radius)
    try:
        while((count < max_iterations) and (stabilized != True)):
            outliers = data_points.copy()
            clusters = [[] for _ in range(len(seed_points))]
            new_centroids = []
            for i, centroid in enumerate(seed_points):
                for j, point in enumerate(data_points):
                    d = np.sqrt((centroid[0] - point[0])**2 + (centroid[1] - point[1])**2)
                    if(d < radius):
                        clusters[i].append(point)
                        outliers.remove(point)
                sum_x = sum(point[0] for point in clusters[i])
                sum_y = sum(point[1] for point in clusters[i])
                cx_new = sum_x / len(clusters[i])
                cy_new = sum_y / len(clusters[i])
                print(f"Cluster {i + 1}: Centroid moved from ({float(centroid[0]):.1f}, {float(centroid[1]):.1f}) to ({float(cx_new):.1f}, {float(cy_new):.1f})")
                new_centroids.append((cx_new, cy_new))
            print(f"Current Outliers: {outliers}"); stabilized = True
            for i, new_centroid in enumerate(new_centroids):
                centroid_shift = np.sqrt((seed_points[i][0] - new_centroid[0])**2 + (seed_points[i][1] - new_centroid[1])**2) # Calculate the centroid shift
                if (centroid_shift > tolerance): stabilized = False # If the centroid shift is higher than the tolerance theshold the clusters are unstable
                seed_points = new_centroids # Update the seed points to the new centroid values
            count += 1 # Go to the next iterative loop
        print("Final Clusters and Outliers: ")
        for i, cluster in enumerate(clusters):
            print(f"Cluster {i+1}: {cluster}")
        print(f"Outliers: {outliers}")
    except ZeroDivisionError:
        print(f"Cluster {i+1} is empty. Try reducing the number of clusters or adjusting the dataset size")
        return
    except Exception as e:
        print(f"Error: {e}")
        return    

def generate_seed_points(data_points, clusters):
    pairs = np.array(data_points)
    x_values = pairs[:, 0] # Get the set of x-values
    y_values = pairs[:, 1] # Get the set of y-values
    total_points = len(data_points)
    
    # Calculate the spread of the data set
    x_maximum = max(x_values)
    x_minimum = min(x_values)
    y_maximum = max(y_values)
    y_minimum = min(y_values)
    
    size_x = (x_maximum - x_minimum)/clusters
    size_y = (y_maximum - y_minimum)/clusters
    macro_num = clusters * clusters
    avg_density = total_points / macro_num
    
    high_density = []
    
    for i in range(clusters): # For each macro block in x-division do
        # Calculate the start and end of x-coordinates for the macroblock
        x_low = x_minimum + i * size_x
        x_high = x_low + size_x
        x_mid = (x_low + x_high)/2
        for j in range(clusters): # For each macro block in y-division do
            # Calculate the start and end of y-coordinates for the macroblock
            y_low = y_minimum + j * size_y
            y_high = y_low + size_y
            y_mid = (y_low + y_high)/2
            
            n_points = points_in_macroblocks(data_points, x_low, y_low, x_high, y_high)
            
            # If points are more than the density then mid-point becomes a seed point
            if(n_points > avg_density):
                high_density.append((x_mid, y_mid))
    seeds = [] # Initialize the empty set of seed points
    for j in range(clusters):
        next_seed = random.choice(high_density)
        seeds.append(next_seed)
        high_density.remove(next_seed)
    radius = min(size_x, size_y)/clusters # Initialize the radius
    for j in range(clusters): # For every cluster repeat the following
        x_j, y_j = seeds[j] # Extract the coordinate of the j'th seed
        for k in range(clusters): # Compare distance between two clusters pairwise
            if(j != k):
                x_k, y_k = seeds[k] # Extract the coordinates of the k'th seed
                d = np.sqrt((x_j - x_k)**2 + (y_j - y_k)**2) # Find the distance between two cluster centroids
                
                # Radius is set to half the distance between two smallest clusters
                if(d < 2*radius): radius = d/2
    return (seeds, radius)

def points_in_macroblocks(data_points, x_low, y_low, x_high, y_high):
    macro_count = 0
    for point in data_points:
        if((point[0] >= x_low) and (point[0] < x_high) and (point[1] >= y_low) and (point[1] < y_high)): macro_count += 1
    return macro_count      
        

if __name__ == "__main__":
    while True:
        mode = input("\n\nPlease select a mode or any other value to quit:\n\n1. File Input\n2. Manual Input\n3. Random Data\n\nSelection: ")
        if mode == "1":
            path = input("Enter the file path: ").replace("\\", "\\\\")
            # parse_data returns list of (x, y) tuples using pandas for CSV/Excel parsing
            data_points = parse_data(path)
            num_clusters = int(input("Enter the number of clusters for K-Means: "))
            max_iterations = int(input("Enter the maximum number of iterations for K-Means: "))
            tolerance = float(input("Enter the convergence tolerance threshold for K-Means: "))
            kmeans(data_points, num_clusters, max_iterations, tolerance)
        elif mode == "2":
            values = input("Enter the x and y values separated by a comma (e.g., 1,2 2,3 3,4): ")
            data_points = parse_data(values)
            num_clusters = int(input("Enter the number of clusters for K-Means: "))
            max_iterations = int(input("Enter the maximum number of iterations for K-Means: "))
            tolerance = float(input("Enter the convergence tolerance threshold for K-Means: "))
            kmeans(data_points, num_clusters, max_iterations, tolerance)
        elif mode == "3":
            num_points = int(input("Enter the number of random data points to generate: "))
            # np.random.seed(0)
            x, y = np.random.uniform(0, 20, num_points), np.random.uniform(0, 20, num_points)
            data_points = list(zip(x, y))
            num_clusters = int(input("Enter the number of clusters for K-Means: "))
            max_iterations = int(input("Enter the maximum number of iterations for K-Means: "))
            tolerance = float(input("Enter the convergence tolerance threshold for K-Means: "))
            kmeans(data_points, num_clusters, max_iterations, tolerance)
        else:
            break  
        input("Press Enter to exit...")
    