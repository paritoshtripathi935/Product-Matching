import sqlite3
import os
import sys
import time
import datetime
import pandas as pd
import numpy as np

sys.path.append("src")
from utils import DatabaseUtils, LoggerUtil

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

