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