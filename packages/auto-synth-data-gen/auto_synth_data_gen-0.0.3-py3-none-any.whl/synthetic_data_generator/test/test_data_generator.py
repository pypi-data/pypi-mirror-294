import unittest  # Import the unittest framework to create test cases
import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas to handle DataFrame operations
from app.synthetic_data_generator.src.data_generator import SyntheticDataGenerator  # Import the class to be tested

class TestSyntheticDataGenerator(unittest.TestCase):
    """
    A test case class that contains unit tests for the SyntheticDataGenerator.
    """
    
    def setUp(self):
        """
        Method to set up test fixtures before each test case.
        This method will be called before every test.
        """
        # Initialize the generator with a fixed seed for reproducibility of random results
        self.generator = SyntheticDataGenerator(seed=42)
    
    def test_generate_continuous(self):
        """
        Test case for generating continuous data.
        It verifies that the generated data has the correct length, mean, and standard deviation.
        """
        data = self.generator.generate_continuous(num_samples=1000, mean=5, std=2)
        self.assertEqual(len(data), 1000)  # Ensure the correct number of samples is generated
        self.assertAlmostEqual(np.mean(data), 5, delta=0.1)  # Check if the mean is close to 5
        self.assertAlmostEqual(np.std(data), 2, delta=0.1)  # Check if the standard deviation is close to 2
    
    def test_generate_categorical(self):
        """
        Test case for generating categorical data.
        It ensures that the correct number of samples is generated and the values come from the specified categories.
        """
        data = self.generator.generate_categorical(num_samples=1000, categories=['A', 'B', 'C'])
        self.assertEqual(len(data), 1000)  # Ensure the correct number of samples is generated
        self.assertTrue(all(x in ['A', 'B', 'C'] for x in data))  # Ensure all values are within the specified categories

    def test_generate_time_series(self):
        """
        Test case for generating time-series data.
        It checks if the generated data has the correct length and is of the correct type (pandas.DatetimeIndex).
        """
        data = self.generator.generate_time_series(periods=100)
        self.assertEqual(len(data), 100)  # Ensure the correct number of time periods is generated
        self.assertIsInstance(data, pd.DatetimeIndex)  # Ensure the output is a pandas DatetimeIndex

    def test_create_synthetic_dataset(self):
        """
        Test case for creating a synthetic dataset.
        It checks the shape of the resulting DataFrame and ensures the time-series feature is included if specified.
        """
        df = self.generator.create_synthetic_dataset(continuous_features=2, categorical_features=1, num_samples=1000, include_time_series=True)
        self.assertEqual(df.shape, (1000, 4))  # 2 continuous, 1 categorical, and 1 time-series column
        self.assertIn('time_series', df.columns)  # Ensure the time-series column is present

    def test_add_noise_continuous(self):
        """
        Test case for adding noise to continuous features.
        It verifies that continuous features are modified after adding noise.
        """
        df = self.generator.create_synthetic_dataset(continuous_features=2, categorical_features=1, num_samples=1000)
        noisy_df = self.generator.add_noise(df, continuous_noise_level=0.1, categorical_noise_level=0)
        
        # Check that continuous features have been modified by the noise
        continuous_cols = [col for col in df.columns if 'continuous_feature' in col]
        for col in continuous_cols:
            self.assertFalse(np.array_equal(df[col], noisy_df[col]), f"Continuous data in {col} should have noise")

    def test_add_noise_categorical(self):
        """
        Test case for adding noise to categorical features.
        It verifies that categorical features are modified after adding noise.
        """
        df = self.generator.create_synthetic_dataset(continuous_features=0, categorical_features=1, num_samples=1000)
        noisy_df = self.generator.add_noise(df, continuous_noise_level=0, categorical_noise_level=0.1)
        
        # Check that categorical features have been modified by the noise
        categorical_col = 'categorical_feature_1'
        num_noisy = np.sum(df[categorical_col] != noisy_df[categorical_col])  # Count the number of changed categorical values
        self.assertGreater(num_noisy, 0, "Categorical data should have noise")

    def test_no_noise(self):
        """
        Test case for ensuring that no noise is added when noise levels are set to 0.
        It verifies that the dataset remains unchanged when no noise is applied.
        """
        df = self.generator.create_synthetic_dataset(continuous_features=2, categorical_features=1, num_samples=1000)
        noisy_df = self.generator.add_noise(df, continuous_noise_level=0, categorical_noise_level=0)
        
        # Check that the DataFrame remains unchanged when noise levels are 0
        self.assertTrue(df.equals(noisy_df), "No noise should be added when noise levels are set to 0")

if __name__ == "__main__":
    unittest.main()  # Run all the test cases
