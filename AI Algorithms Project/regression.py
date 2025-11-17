import math
import pandas as pd
import io

def parse_data(content):
    data_points = []
    
    # Case 1: Check if the content is a file-life object or a file path
    if hasattr(content, 'read') or (isinstance(content, str) and (content.endswith('.csv') or content.endswith('.xlsx'))):
        try:    
            if hasattr(content, "read"):  # i.e., an uploaded file
                filename = content.name.lower()
                if filename.endswith(".csv"):
                    df = pd.read_csv(content)
                elif filename.endswith(".xlsx"):
                    df = pd.read_excel(content)
                else:
                    raise ValueError("Please upload a valid CSV or Excel file.")
        
        except Exception as e:
            raise ValueError(f"Error reading the file: {e}")
        
        # Check if the DataFrame has the required number of columns
        if {'x', 'y'}.issubset(df.columns):
            x, y = df['x'], df['y'] # Assuming that the label columns for x and y are 'x' and 'y'
        else:
            x, y = df.iloc[:, 0], df.iloc[:, 1] # Assuming that the label columns for x and y are absent

        # Convert string data to numeric, forcing errors to Not a Number
        x = pd.to_numeric(x, errors='coerce')
        y = pd.to_numeric(y, errors='coerce')
        clean_data = pd.DataFrame({'x': x, 'y': y}).dropna() # Remove the rows with Not a Number values
        
        # Create the list of tuples for data points and return the formatted result
        data_points = list(zip(clean_data['x'], clean_data['y']))
        return data_points
    # Case 2: Check if content is a string that was input directly i.e. doesn't match the file path pattern
    elif isinstance(content, str):
        points = content.split(" ")
        x, y = [float(point.split(",")[0]) for point in points], [float(point.split(",")[1]) for point in points]
         # Ensure there are at least two points to compute regression
        if len(x) != len(y):
            raise ValueError("At least two data points are required for regression or there is a mismatch between number of x-values and y-values")
        data_points = list(zip(x,y))
        return data_points
   
    else:
        raise ValueError("Invalid input type. Please provide a file path, upload a file in the GUI, or input data as a string.")   
    
    

def mean(values):
    """
    Calculates the mean of a set of values
    """
    n = len(values)
    total_sum = 0.0
    for value in values:
        total_sum += value
    mean = total_sum/n
    return mean

def variance(values, mean):
    """
    Calculates the variance from a set of values and it's mean
    """
    n = len(values)
    total = 0.0
    for point in values:
        distance = (point - mean) ** 2
        total += distance
    variance = total/(n-1)
    return variance

def covariance(x_values, y_values, x_mean, y_mean):
    """
    Calculates the covariance from x and y values and their respective means
    """
    n = len(x_values)
    total = 0.0
    i = 1
    for i in range(n):
        x = x_values[i-1]
        y = y_values[i-1]
        total += (x-x_mean)*(y-y_mean)
    covariance_xy = total/(n-1)
    return covariance_xy

def regression_analysis(data_points):
    """
    Perform linear regression on a list of (x, y) data points.
    Returns the slope and intercept of the best fit line.
    """
    log = io.StringIO() # Used to output the results to the GUI
    x_values = [point[0] for point in data_points]
    y_values = [point[1] for point in data_points]

    # Ensure there are the same number of x-values as y-values
    if len(x_values) != len(y_values):
        raise ValueError("At least two data points are required for regression or there is a mismatch between number of x-values and y-values")
    x_mean = mean(x_values) # Calculate X Mean
    y_mean = mean(y_values) # Calculate Y Mean
    variance_x = variance(x_values, x_mean) # Calculate Variance of X
    covariance_xy = covariance(x_values, y_values, x_mean, y_mean) # Calculate Variance of Y
    slope = covariance_xy / variance_x # Calculate Slope
    intercept = y_mean - slope * x_mean # Calculate Intercept
    
    log.write(f"Equation of Regression Line: y = {slope:.4f}x + {intercept:.4f}")
    log.write(f"\nMean of X: {x_mean:.4f}\nMean of Y: {y_mean:.4f}\n")
    log.write(f"Variance of X: {variance_x:.4f}\nCovariance: {covariance_xy:.4f}\n")
    log.write(f"Slope: {slope:.4f}\nIntercept: {intercept:.4f}\n")
    return slope, intercept, log.getvalue()


if __name__=="__main__":
    points = input("Enter data points manually: ")
    points = parse_data(points)
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    if len(x_values) != len(y_values):
        raise Exception
    else:
        slope, intercept, log = regression_analysis(points)
        print("\n" + log)
        
        