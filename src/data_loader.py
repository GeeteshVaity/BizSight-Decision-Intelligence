"""
Data Loader Module
Handles loading and validating business data from CSV files
"""

import pandas as pd
import os


class DataLoader:
    """
    Load and validate business data from CSV files
    """
    
    def __init__(self, filepath):
        """
        Initialize the DataLoader
        
        Args:
            filepath (str): Path to the CSV file
        """
        self.filepath = filepath
        self.data = None
    
    def load_data(self):
        """
        Load data from CSV file
        
        Returns:
            pd.DataFrame: Loaded business data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If required columns are missing
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        # Load the CSV file
        self.data = pd.read_csv(self.filepath)
        
        # Validate required columns
        required_columns = ['date', 'revenue', 'cost']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Convert date column to datetime
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Sort by date
        self.data = self.data.sort_values('date').reset_index(drop=True)
        
        print(f"Data loaded successfully: {len(self.data)} records")
        return self.data
    
    def get_data_summary(self):
        """
        Get a summary of the loaded data
        
        Returns:
            dict: Summary statistics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        summary = {
            'total_records': len(self.data),
            'date_range': (self.data['date'].min(), self.data['date'].max()),
            'columns': list(self.data.columns),
            'data_types': self.data.dtypes.to_dict()
        }
        
        return summary
