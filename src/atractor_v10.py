import os
import math
import nolds
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors

def read_data_from_file(file_path):
    """
    Reads data from a specified file and returns a NumPy array of values.

    The file is expected to have lines formatted as 'timestamp : value',
    where 'timestamp' is a string and 'value' is a float.

    :param file_path: Path to the file for reading data.
    :return: NumPy array of data values.
    """
    # Initialize an empty dictionary to store the data
    data = {}

    # Open the file in read mode
    with open(file_path, "r") as file:

        # Iterate over each line in the file
        for line in file:

            # Split the line into timestamp and value, removing whitespace
            timestamp, value = line.strip().split(" : ")

            # Convert the value to float and store it in the dictionary with the timestamp as the key
            data[timestamp] = float(value)

    # Convert the values of the dictionary to a NumPy array and return
    return np.array(list(data.values()))

def calculate_auto_mutual_information(time_series_data, maximum_delay, number_of_partitions):
    """
    Calculates the auto mutual information for a given time series. The time series
    data is first normalized, and then mutual information is calculated.

    :param time_series_data: The input time series data.
    :param maximum_delay: The maximum delay to consider for mutual information calculation.
    :param number_of_partitions: The number of partitions to use in the mutual information calculation.
    :return: A tuple containing the array of mutual information values and the optimal delay value.
    """
    # Normalizing the time series data
    normalized_time_series = (time_series_data - np.min(time_series_data)) / (np.max(time_series_data) - np.min(time_series_data))
    
    # Determine the length of the normalized series
    length_of_series = len(normalized_time_series)

    # Calculate mutual information and the optimal delay
    mutual_information_values, optimal_delay_value = calculate_pim(normalized_time_series, maximum_delay, number_of_partitions, length_of_series)

    return mutual_information_values, optimal_delay_value

def calculate_mutual_information(time_series_data, tau_values, number_of_partitions, time_series_length):
    """
    Calculates mutual information for a time series for a given set of Tau values and 
    a specified number of partitions. The mutual information is calculated for each 
    Tau value and stored in an array.

    :param time_series_data: The time series data for which to calculate mutual information.
    :param tau_values: A range of Tau values to consider in the calculation.
    :param number_of_partitions: The number of partitions for histogram calculation.
    :param time_series_length: The length of the time series data.
    :return: An array of mutual information values corresponding to each Tau value.
    """
    mutual_information_values = []

    for tau in tau_values:

        mutual_info_for_current_tau = 0

        for partition1 in range(1, number_of_partitions + 1):

            for partition2 in range(1, number_of_partitions + 1):

                # Calculate unidimensional histograms for each partition
                indices_px = np.where(((partition1 - 1) / number_of_partitions < time_series_data[:time_series_length - tau]) &
                                      (time_series_data[:time_series_length - tau] <= partition1 / number_of_partitions))[0]
                
                indices_py = np.where(((partition2 - 1) / number_of_partitions < time_series_data[tau:time_series_length]) &
                                      (time_series_data[tau:time_series_length] <= partition2 / number_of_partitions))[0]

                # Calculate bidimensional histogram
                indices_pxy = np.where(((partition1 - 1) / number_of_partitions < time_series_data[:time_series_length - tau]) &
                                       (time_series_data[:time_series_length - tau] <= partition1 / number_of_partitions) &
                                       ((partition2 - 1) / number_of_partitions < time_series_data[tau:time_series_length]) &
                                       (time_series_data[tau:time_series_length] <= partition2 / number_of_partitions))[0]

                probability_pxy = len(indices_pxy) / (time_series_length - tau)
                
                # Calculate probabilities and mutual information for current Tau
                if probability_pxy > 0:

                    probability_px = len(indices_px) / (time_series_length - tau)
                    probability_py = len(indices_py) / (time_series_length - tau)
                    mutual_info_for_current_tau += probability_pxy * math.log(probability_pxy / (probability_px * probability_py), 2)

        mutual_information_values.append(mutual_info_for_current_tau)

    return mutual_information_values

def find_prime_index(pim_values, time_series_length):
    """
    Finds the prime index in an array of Phase Information Measure (PIM) values.
    The prime index is identified as the first local minimum in the PIM values.

    :param pim_values: Array of Phase Information Measure values.
    :param time_series_length: Length of the time series.
    :return: Prime index value, or 0 if not found.
    """
    # Ensure the loop does not exceed the length of the PIM array
    for index in range(2, len(pim_values)):

        # Calculate first and second derivatives of PIM
        first_derivative = pim_values[index - 1] - pim_values[index - 2]
        second_derivative = pim_values[index] - pim_values[index - 1]

        # Check for the first local minimum
        if first_derivative < 0 and second_derivative > 0:
            return index - 1
        
    return 0

def calculate_pim(time_series_data, maximum_tau, number_of_partitions, time_series_length):
    """
    Calculates the Phase Information Measure (PIM) for a time series. It computes the mutual
    information for a range of Tau values and identifies the optimal Tau value.

    :param time_series_data: The time series data for which PIM is to be calculated.
    :param maximum_tau: The maximum Tau value to consider in the calculation.
    :param number_of_partitions: The number of partitions to use in the mutual information calculation.
    :param time_series_length: The length of the time series data.
    :return: A tuple containing the PIM values array and the optimal Tau value.
    """
    # Calculate mutual information for a range of Tau values
    pim_values = calculate_mutual_information(time_series_data, range(1, maximum_tau + 1), number_of_partitions, time_series_length)
    
    # Determine the optimal Tau value
    optimal_tau_value = find_prime_index(pim_values, time_series_length)
    optimal_tau_value = optimal_tau_value if optimal_tau_value != 0 else maximum_tau
    
    return pim_values, optimal_tau_value

def phase_space_reconstruction(time_series_data, embedding_dimension, delay, number_of_points=None):
    """
    Performs phase space reconstruction on a given time series. The reconstruction 
    involves creating a matrix where each column is a delayed version of the time 
    series, based on the specified embedding dimension and delay.

    :param time_series_data: The time series data to be reconstructed.
    :param embedding_dimension: The embedding dimension for the reconstruction.
    :param delay: The delay to be used in the reconstruction.
    :param number_of_points: Optional; number of points to consider in the reconstruction.
                             If None, calculates automatically based on series length.
    :return: The reconstructed phase space as a 2D numpy array.
    """
    time_series_length = len(time_series_data)

    # Calculate the number of points if not provided
    if number_of_points is None:
        number_of_points = time_series_length - (embedding_dimension - 1) * delay

    # Initialize the reconstructed space array
    reconstructed_space = np.zeros((number_of_points, embedding_dimension))

    # Construct the reconstructed space
    for dimension in range(embedding_dimension):
        reconstructed_space[:, dimension] = time_series_data[dimension * delay : dimension * delay + number_of_points]

    return reconstructed_space

def knn_dimension_estimation(time_series_data, delay, max_embedding_dimension, relative_tolerance, absolute_tolerance):
    """
    Estimates the embedding dimension for a time series using the K-nearest neighbors method.
    The function calculates the fraction of false nearest neighbors (FNN) for dimensions up to the maximum specified,
    and determines the optimal embedding dimension.

    :param time_series_data: The time series data for dimension estimation.
    :param delay: The delay to use in the phase space reconstruction.
    :param max_embedding_dimension: The maximum embedding dimension to consider.
    :param relative_tolerance: The relative tolerance for nearest neighbor search.
    :param absolute_tolerance: The absolute tolerance for nearest neighbor search.
    :return: Tuple containing the FNN array, the estimated embedding dimension, and a list of dimensions considered.
    """
    total_data_points = len(time_series_data)
    standard_deviation_of_data = np.std(time_series_data)
    fnn_values = np.zeros(max_embedding_dimension)
    estimated_embedding_dimension = 0

    for current_dimension in range(1, max_embedding_dimension + 1):
        reconstructed_data = phase_space_reconstruction(time_series_data, current_dimension, delay)
        reconstructed_data_length = len(reconstructed_data)

        # Use NearestNeighbors for efficient neighbor search
        nearest_neighbors_model = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(reconstructed_data)
        distances, indices = nearest_neighbors_model.kneighbors(reconstructed_data)

        for i in range(reconstructed_data_length - current_dimension * delay):
            nearest_neighbor_index = indices[i, 1]

            if i + current_dimension * delay < total_data_points and nearest_neighbor_index + current_dimension * delay < total_data_points:

                distance_ratio = abs(time_series_data[i + current_dimension * delay] - time_series_data[nearest_neighbor_index + current_dimension * delay]) / distances[i, 1]
                combined_distance = np.sqrt(distance_ratio ** 2 + distances[i, 1] ** 2)

                if distance_ratio > relative_tolerance or combined_distance / standard_deviation_of_data > absolute_tolerance:
                    fnn_values[current_dimension - 1] += 1

        fnn_values[current_dimension - 1] /= reconstructed_data_length

        if fnn_values[current_dimension - 1] < 0.15:

            estimated_embedding_dimension = current_dimension
            break

    if estimated_embedding_dimension == 0:
        estimated_embedding_dimension = np.argmin(fnn_values) + 1

    dimensions_considered = list(range(1, max_embedding_dimension + 1))

    return fnn_values, estimated_embedding_dimension, dimensions_considered

def plot_attractor(reconstructed_data, file_name, save_directory, plot_title="Phase Space Attractor"):
    """
    Plots the phase space attractor for the given reconstructed data. Generates both
    2D and 3D plots if the reconstructed data has more than two dimensions.

    :param reconstructed_data: Reconstructed phase space data.
    :param file_name: Name of the file to save the plot.
    :param save_directory: Directory to save the plot.
    :param plot_title: Title of the plot. Default is 'Phase Space Attractor'.
    """
    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Plotting the 2D attractor
    plt.figure(figsize=(8, 6))
    plt.plot(reconstructed_data[:, 0], reconstructed_data[:, 1], 'b.', markersize=1, alpha=0.7)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title(plot_title)
    plt.grid(True)
    plt.savefig(os.path.join(save_directory, f"ATTR_{file_name}_2D.png"))

    # Plotting the 3D attractor if there are more than 2 dimensions
    if reconstructed_data.shape[1] > 2:

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(reconstructed_data[:, 0], reconstructed_data[:, 1], reconstructed_data[:, 2], markersize=1, alpha=0.7)
        ax.set_xlabel('Dimension 1')
        ax.set_ylabel('Dimension 2')
        ax.set_zlabel('Dimension 3')
        ax.set_title(plot_title)
        plt.savefig(os.path.join(save_directory, f"ATTR_{file_name}_3D.png"))

    plt.show()

def plot_FNN(fnn_values, optimal_embedding_dimension, dimensions, plot_title, save_directory):
    """
    Plots the FNN percentage as a function of embedding dimension and marks the optimal embedding dimension.
    The FNN values are plotted against the given array of embedding dimensions.

    :param fnn_values: Array of FNN percentages.
    :param optimal_embedding_dimension: Optimal embedding dimension identified.
    :param dimensions: Array of embedding dimensions considered.
    :param plot_title: Title for the plot.
    :param save_directory: Directory to save the plot.
    """
    plt.figure()
    plt.plot(dimensions, fnn_values * 100, marker='o')  # Convert to percentage
    plt.axvline(x=optimal_embedding_dimension, color='red', linestyle='--', label=f'Optimal Dimension: {optimal_embedding_dimension}')
    plt.xlabel("Embedding Dimension")
    plt.ylabel("FNN Percentage (%)")
    plt.title(plot_title)
    plt.legend()
    plt.grid(True)

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    plt.savefig(os.path.join(save_directory, f"FNN_{plot_title}.png"))

def plot_data_series(data, plot_title, save_directory):
    """
    Plots a data series and saves the plot to a specified directory. The plot is 
    saved with the provided plot title as the file name.

    :param data: Data to be plotted, typically a time series.
    :param plot_title: Title for the plot.
    :param save_directory: Directory to save the plot.
    """
    # Create a plot with specific size
    fig, ax = plt.subplots(figsize=(36, 4))

    # Plot the data
    ax.plot(data, "#000000", linewidth=1.25)

    # Set up grid lines
    ax.grid(which='major', color='#94a6d1', linewidth=0.5, linestyle='dashed')
    ax.grid(which='minor', color='#d19594', linewidth=0.5, linestyle='dashed')
    ax.minorticks_on()

    # Set labels and title
    plt.xlabel("Time (ms)")
    plt.ylabel("mV")
    plt.title(plot_title)

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Save the plot
    plt.savefig(os.path.join(save_directory, f"{plot_title}.png"))

def plot_mutual_information(pim_values, optimal_tau, plot_title, save_directory):
    """
    Plots mutual information graph and saves it to a specified directory. The optimal 
    Tau value is marked with a vertical line.

    :param pim_values: Array of mutual information values.
    :param optimal_tau: Optimal Tau value for mutual information.
    :param plot_title: Title for the plot.
    :param save_directory: Directory to save the plot.
    """
    # Tau values corresponding to the mutual information values
    tau_values = range(1, len(pim_values) + 1)
    # Create the plot
    plt.figure()
    plt.plot(tau_values, pim_values)
    # Mark the optimal Tau value
    plt.axvline(x=optimal_tau, color='red', linestyle='--', label=f'Optimal Tau: {optimal_tau}')
    plt.xlabel("Tau")
    plt.ylabel("Mutual Information")
    plt.title(plot_title)
    plt.legend()

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    # Save the plot
    plt.savefig(os.path.join(save_directory, f"AMI_{plot_title}.png"))

if __name__ == "__main__":

    main_directory = "Data"
    
    # Iterate through the directory tree
    for root, dirs, files in os.walk(main_directory):

        for dir_name in dirs:

            # Check if the directory name is either 'ECG' or 'PPG'
            if dir_name in ["ECG", "PPG"]:

                directory_path = os.path.join(root, dir_name)
                img_directory = os.path.join(directory_path, "Img")

                # Check if the 'Img' directory exists, if not, create it
                if not os.path.exists(img_directory):
                    os.makedirs(img_directory)

                # Loop through each file in the directory
                for file_name in os.listdir(directory_path):

                    if file_name.endswith(".txt"):

                        # Full process for each file
                        data_file_path = os.path.join(directory_path, file_name)

                        # Read data from the provided file path
                        time_series_data = read_data_from_file(data_file_path)

                        # Extract the file name without extension for use in plot titles
                        plot_title = os.path.basename(data_file_path).split('.')[0]

                        # Plotting the initial segment of the time series data
                        plot_data_series(time_series_data[:2400], plot_title, img_directory)

                        # Parameters for auto mutual information calculation
                        max_delay_taumax = 16
                        num_partitions = 2

                        # Calculate and plot auto mutual information
                        mutual_info_values, optimal_delay = calculate_auto_mutual_information(time_series_data, max_delay_taumax, num_partitions)
                        plot_mutual_information(mutual_info_values, optimal_delay, plot_title, img_directory)

                        # Parameters for K-nearest neighbors method
                        max_embedding_dimension = 10
                        relative_tolerance = 10
                        absolute_tolerance = 2

                        # Estimate the embedding dimension and plot results
                        fnn_values, estimated_embedding_dimension, dimension_list = knn_dimension_estimation(time_series_data, optimal_delay, max_embedding_dimension, relative_tolerance, absolute_tolerance)
                        plot_FNN(fnn_values, estimated_embedding_dimension, dimension_list, plot_title, img_directory)

                        # Output the optimal delay and embedding dimension
                        print(plot_title, "--- Optimal Delay T: ", optimal_delay)
                        print(plot_title, "--- Estimated Embedding Dimension D: ", estimated_embedding_dimension)
                        print("")

                        # Perform phase space reconstruction and plot the attractor
                        reconstructed_phase_space = phase_space_reconstruction(time_series_data, estimated_embedding_dimension, optimal_delay)
                        plot_attractor(reconstructed_phase_space, plot_title, img_directory)

                        # Calculate and print complexity measures
                        correlation_dim = nolds.corr_dim(time_series_data, estimated_embedding_dimension)
                        lyapunov_exp = nolds.lyap_r(time_series_data, estimated_embedding_dimension)
                        hurst_exp = nolds.hurst_rs(time_series_data)
                        print(plot_title, "--- Lyapunov Exponent: ", lyapunov_exp)
                        print(plot_title, "--- Correlation Dimension: ", correlation_dim)
                        print(plot_title, "--- Hurst Exponent: ", hurst_exp)