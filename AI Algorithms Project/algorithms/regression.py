# This is the regression algorithmn
from data.data_parser import parse_data

def regression_analysis(total_points, data_points):
    sum_x = 0
    sum_y = 0
    i = 0
    for x, y in data_points:
        sum_x += x
        sum_y += y
        i += 1
    x_avg = sum_x / total_points
    y_avg = sum_y / total_points
    variance_x = 0
    for x, y in data_points:
        i = ((x - x_avg) ** 2)
        variance_x += i
    variance_x = variance_x / (total_points - 1)
    covariance_xy = 0
    for x, y in data_points:
        xi = (x - x_avg)
        yi = (y - y_avg)
        i = (xi * yi)
        covariance_xy += i
    covariance_xy = covariance_xy / (total_points - 1)
    slope = covariance_xy / variance_x
    intercept = y_avg - slope * x_avg
    return slope, intercept

if __name__ == "__main__":
    mode = input("Please select a mode:\n1. File Input\n2. Manual Input\n")
    if mode == "1":
        path = input("Enter the file path: ").replace('\\', '\\\\')
        with open(path, "r") as file:
            data_points = parse_data(file)
        slope, intercept = regression_analysis(len(data_points), data_points)
        print(f"Slope: {slope}, Intercept: {intercept}")
    elif mode == "2":
        values = input("Enter the x and y values separated by a comma (e.g., 1,2 2,3 3,4): ")
        data_points = parse_data(values)
        slope, intercept = regression_analysis(len(data_points), data_points)
        print(f"Slope: {slope}, Intercept: {intercept}")
    input("Press Enter to exit...")