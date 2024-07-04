import os
import sys
import time
import datetime
import pandas as pd
import numpy as np

class AutoEDA:
    """
    This is a class to perform exploratory data analysis.
     
    Features:
        - This class will take a dataframe as input and perform exploratory data analysis.
        - Anyone can use this class to perform exploratory data analysis.
    
    Attributes:
        - dataframe (pd.DataFrame): The dataframe to perform exploratory data analysis.
        
    Methods:
     
    Output:
        - generate_stats: This method will generate statistics of the dataframe.
        - generate_plots: This method will generate plots of the dataframe.
        - generate_report: This method will generate a report of the dataframe.
        
    Optional:
        - Plotly Dashboard: This class will also generate a plotly dashboard.
        - If the user wants to generate a plotly dashboard, they can use the generate_dashboard method.
     
    Example:
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        if not isinstance(self.dataframe, pd.DataFrame):
            raise ValueError("Dataframe is not correct.")
        
    
    def _generate_basic_stats(self):
        """
        This method will generate basic statistics of the dataframe.
        """
        stats = self.dataframe.describe()
        
        # analyze the data types of the dataframe and suggest the user to convert the data types.
        data_types = self.dataframe.dtypes
        data_types = data_types.reset_index()
        data_types.columns = ['Feature', 'Data Type']
        data_types = data_types.groupby('Data Type').count()
        data_types = data_types.reset_index()
        data_types.columns = ['Data Type', 'Count']
        
        return stats, data_types

        
    

    