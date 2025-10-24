# Regression analysis using NumPy for efficiency
import numpy as np
from data.data_parser import parse_data


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
    mode = input("Please select a mode:\n1. File Input\n2. Manual Input\n")
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
    input("Press Enter to exit...")
