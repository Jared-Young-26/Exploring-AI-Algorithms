import pandas as pd

def parse_data(content):
    data_points = []
    
    if hasattr(content, 'read'):
        if content.endswith('.csv'):
            df = pd.read_csv(content)
        elif content.endswith('.xlsx'):
            df = pd.read_excel(content)
        else:
            raise ValueError("Please provide a valid CSV or Excel file.")

        if {'x', 'y'}.issubset(df.columns):
            x, y = df['x'], df['y']
        else:
            raise ValueError("File must contain 'x' and 'y' columns.")
        data_points = list(zip(x, y))
        return data_points

    if isinstance(content, str):
        