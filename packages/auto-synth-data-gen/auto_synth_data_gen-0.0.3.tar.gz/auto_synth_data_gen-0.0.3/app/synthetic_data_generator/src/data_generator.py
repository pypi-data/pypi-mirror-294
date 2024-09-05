import numpy as np  # Import numpy for numerical operations and random number generation
import pandas as pd  # Import pandas to create and manage the dataset

class SyntheticDataGenerator:
    def __init__(self, seed=None):
        """
        Initialize the synthetic data generator with an optional seed for reproducibility.
        
        Parameters:
        seed (int or None): If provided, it sets the seed for NumPy's random number generator
                            to ensure that the results are reproducible.
        """
        self.seed = seed  # Store the seed value
        if seed:
            np.random.seed(seed)  # Set the random seed if provided
    
    def generate_continuous(self, num_samples=1000, mean=0, std=1):
        """
        Generate continuous data with a normal (Gaussian) distribution.
        
        Parameters:
        num_samples (int): Number of samples to generate.
        mean (float): Mean of the normal distribution.
        std (float): Standard deviation of the normal distribution.
        
        Returns:
        numpy.ndarray: Array of generated continuous data.
        """
        return np.random.normal(loc=mean, scale=std, size=num_samples)  # Generate continuous data

    def generate_categorical(self, num_samples=1000, categories=None):
        """
        Generate categorical data by randomly selecting from a set of categories.
        
        Parameters:
        num_samples (int): Number of samples to generate.
        categories (list): List of category labels to randomly choose from.
        
        Returns:
        numpy.ndarray: Array of generated categorical data.
        """
        if categories is None:
            categories = ['A', 'B', 'C']  # Default categories if none are provided
        return np.random.choice(categories, size=num_samples)  # Randomly select category values
    
    def generate_time_series(self, start_date='2022-01-01', periods=1000, freq='D'):
        """
        Generate a time-series feature based on a specified start date and frequency.
        
        Parameters:
        start_date (str): Starting date for the time-series.
        periods (int): Number of time periods (data points).
        freq (str): Frequency of the time-series ('D' for daily, 'H' for hourly, etc.).
        
        Returns:
        pandas.DatetimeIndex: A date range for the time-series data.
        """
        return pd.date_range(start=start_date, periods=periods, freq=freq)  # Generate time-series data
    
    def create_synthetic_dataset(self, continuous_features=1, categorical_features=1, num_samples=1000, include_time_series=False, start_date='2022-01-01', periods=None, freq='D'):
        """
        Create a synthetic dataset containing continuous, categorical, and optional time-series features.
        
        Parameters:
        continuous_features (int): Number of continuous (numeric) features to generate.
        categorical_features (int): Number of categorical features to generate.
        num_samples (int): Total number of samples (rows) in the dataset.
        include_time_series (bool): Whether to include a time-series feature.
        start_date (str): Starting date for the time-series feature.
        periods (int): Number of periods for the time-series feature (optional).
        freq (str): Frequency of the time-series data.
        
        Returns:
        pandas.DataFrame: A DataFrame containing the generated synthetic dataset.
        """
        data = {}  # Initialize an empty dictionary to store the data
        
        # Generate continuous data for the specified number of features
        for i in range(continuous_features):
            data[f'continuous_feature_{i+1}'] = self.generate_continuous(num_samples)
        
        # Generate categorical data for the specified number of features
        for i in range(categorical_features):
            data[f'categorical_feature_{i+1}'] = self.generate_categorical(num_samples)
        
        # Optionally generate time-series data, matching the number of samples
        if include_time_series:
            if periods is None:
                periods = num_samples  # Use num_samples if periods are not explicitly provided
            data['time_series'] = self.generate_time_series(start_date=start_date, periods=periods, freq=freq)
        
        # Return the data as a pandas DataFrame
        return pd.DataFrame(data)
    
    def add_noise(self, df, continuous_noise_level=0.01, categorical_noise_level=0.01):
        """
        Add noise to the synthetic dataset.
        
        Parameters:
        df (pandas.DataFrame): The original dataset to which noise will be added.
        continuous_noise_level (float): Proportion of noise to add to continuous features (0.01 = 1%).
        categorical_noise_level (float): Proportion of noise to add to categorical features (0.01 = 1%).
        
        Returns:
        pandas.DataFrame: A new DataFrame with noise added to the original dataset.
        """
        noisy_df = df.copy()  # Create a copy of the original dataset to avoid modifying it
        
        # Add noise to continuous features
        continuous_cols = [col for col in df.columns if 'continuous_feature' in col]  # Identify continuous columns
        for col in continuous_cols:
            noise = np.random.normal(0, continuous_noise_level * df[col].std(), size=len(df))  # Generate Gaussian noise
            noisy_df[col] += noise  # Add noise to each continuous feature
        
        # Add noise to categorical features
        categorical_cols = [col for col in df.columns if 'categorical_feature' in col]  # Identify categorical columns
        for col in categorical_cols:
            num_noisy = int(categorical_noise_level * len(df))  # Calculate how many values will be replaced with noise
            noisy_indices = np.random.choice(df.index, size=num_noisy, replace=False)  # Select random indices to modify
            original_values = df[col].copy()  # Keep a copy of the original values (for reference)

            # Randomly replace the selected categorical values with other category labels
            noisy_values = np.random.choice(df[col].unique(), size=num_noisy)  # Randomly select replacement values
            noisy_df.loc[noisy_indices, col] = noisy_values  # Apply noise by replacing values in the original column

        return noisy_df  # Return the noisy dataset as a new DataFrame
