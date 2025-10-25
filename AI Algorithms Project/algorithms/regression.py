# Regression analysis using NumPy for efficiency
import numpy as np
import pandas as pd
import io

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

def regression_analysis(data_points):
    """
    Perform linear regression on a list of (x, y) data points using NumPy.
    Returns the slope and intercept of the best fit line.
    """
    data = np.array(data_points, dtype=float)
    # Ensure there are at least two points to compute regression
    if data.size == 0 or data.shape[0] < 2:
        raise ValueError("At least two data points are required for regression.")
    x = data[:, 0]
    y = data[:, 1]
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    # Calculate variance and covariance using sample statistics (ddof=1)
    variance_x = np.var(x, ddof=1)
    covariance_xy = np.cov(x, y, ddof=1)[0, 1]
    slope = covariance_xy / variance_x
    intercept = y_mean - slope * x_mean
    return slope, intercept


if __name__ == "__main__":
    while True:
        mode = input("\n\nPlease select a mode or any other value to quit:\n1. File Input\n2. Manual Input\n")
        if mode == "1":
            path = input("Enter the file path: ").replace("\\", "\\\\")
            # parse_data returns list of (x, y) tuples using pandas for CSV/Excel parsing
            data_points = parse_data(path)
            slope, intercept = regression_analysis(data_points)
            print(f"Slope: {slope}, Intercept: {intercept}")
        elif mode == "2":
            values = input("Enter the x and y values separated by a comma (e.g., 1,2 2,3 3,4): ")
            data_points = parse_data(values)
            slope, intercept = regression_analysis(data_points)
            print(f"Slope: {slope}, Intercept: {intercept}")
        else:
            break
        input("Press Enter to exit...")

