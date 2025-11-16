import math
import pandas as pd

def mean(values):
    n = len(values)
    total_sum = 0
    for value in values:
        total_sum += value
    mean = total_sum/n
    return mean

def variance(values, mean):
    n = len(values)
    total = 0
    for point in values:
        distance = (point - mean) ** 2
        total += distance
    variance = total/(n-1)
    return variance

def covariance(x_values, y_values, mean_x, mean_y):
    n = len(x_values)
    


if __name__=="__main__":
    points = input("Enter data points manually: ").split(" ")
    x_values = [int(point.split(",")[0]) for point in points]
    y_values = [int(point.split(",")[1]) for point in points]
    print("X: " + str(x_values) + "\nY: "+ str(y_values))