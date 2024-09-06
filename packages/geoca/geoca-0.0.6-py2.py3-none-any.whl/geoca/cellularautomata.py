"""
Description:
The cellularautomata module implements a cellularautomata model for analyzing the distribution of population and other resources within a study area based on grid data.
"""

import random

# Define eight directions of movement
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Get coordinates of neighbors in eight directions
def get_neighbors(row_now, col_now, data_list):
    """
    Get neighboring valid coordinates given a row and column index in a 2D data list.

    Args:
        row_now (int): The current row index.
        col_now (int): The current column index.
        data_list (list): A 2D array representing the data converted from raster data.

    Returns:
        list: A list of neighboring valid coordinates.
    """
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row_now + dr, col_now + dc
        if 0 <= new_row < len(data_list) and 0 <= new_col < len(data_list[0]) and data_list[new_row][new_col] is not None:
            neighbors.append((new_row, new_col))
    return neighbors

# Migrate population function
def migrate_population(data_list, population):
    """
    Population migration to the neighborhood with the highest raster pixel value.

    Args:
        data_list (list): A list converted from raster data that elements are raster pixel values.
        population (list): A list storing the initial population count of each pixel.

    Returns:
        list: A 2D list representing the new population distribution after migration.
    """
    new_population = [[0 for _ in range(len(data_list[0]))] for _ in range(len(data_list))]
    
    for row in range(len(data_list)):
        for col in range(len(data_list[0])):
            if not data_list[row][col]:
                continue  # Skip invalid regions
            neighbors = get_neighbors(row, col, data_list)
            if not neighbors:
                continue  # Skip if no valid neighbors
            
            max_value = max([data_list[r][c] for r, c in neighbors])
            highest_neighbors = [(r, c) for r, c in neighbors if data_list[r][c] == max_value]

            target_row, target_col = random.choice(highest_neighbors)
            
            if not population[row][col]:
                continue  # Skip invalid regions
            migrated_population = population[row][col]
            
            new_population[target_row][target_col] += migrated_population
            new_population[row][col] += population[row][col] - migrated_population
    
    return new_population

def run_iterations_num(iterations, data_list, population_num=10):
    """
    Running a cellular automata using a uniform initial population count to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_num (int): The initial population count at each pixel (default: 10).

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """
    population = [[population_num for _ in range(len(data_list[0]))] for _ in range(len(data_list))]

    for i in range(iterations):
        population = migrate_population(data_list, population)
        print(f"Iteration {i + 1} is complete.")

    return population

def run_iterations_pop(iterations, data_list, population_list):
    """
    Running a cellular automata using an initial population size raster to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_list (list): A 2D array converted from an initial population size raster.

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """

    for i in range(iterations):
        population_list = migrate_population(data_list, population_list)
        print(f"Iteration {i + 1} is complete.")

    return population_list
