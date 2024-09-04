import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.graph_objects as go

class MissingDataHandler:
    def __init__(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("The input must be a pandas DataFrame.")
        self.dataframe = dataframe

    def detect_missing_values(self, dataframe=None):
        if dataframe is None:
            dataframe = self.dataframe
        missing_data_count = dataframe.isnull().sum()
        return missing_data_count

    def impute_missing(self, strategy='mean', fill_value=None, dataframe=None, **kwargs):
        try:
            if dataframe is None:
                dataframe = self.dataframe
            dataframe = dataframe.replace({None: np.nan})
            missing_data_before = self.detect_missing_values(dataframe)
            if strategy in ['mean', 'median', 'most_frequent']:
                imputer = SimpleImputer(strategy=strategy)
            elif strategy == 'predictive':
                imputer = IterativeImputer(**kwargs)
            elif strategy == 'custom':
                if fill_value is None:
                    raise ValueError("fill_value must be provided for custom imputation")
                imputer = SimpleImputer(strategy='constant', fill_value=fill_value)
            else:
                raise ValueError("Unsupported imputation strategy")
            imputed_data = imputer.fit_transform(dataframe)
            dataframe = pd.DataFrame(imputed_data, columns=dataframe.columns)
            return dataframe
        except ValueError as e:
            self.log_message(str(e))
            raise
        except Exception as e:
            self.log_message(f"An unexpected error occurred: {str(e)}")
            raise

    def plot_missing_values(self, dataframe=None):
        if dataframe is None:
            dataframe = self.dataframe
        missing_data_count = self.detect_missing_values(dataframe)
        fig = go.Figure(go.Bar(
            x=missing_data_count.index,
            y=missing_data_count.values,
            text=missing_data_count.values,
            textposition='auto',
            
        ))
        fig.update_layout(
            title="Count of Missing Values by Column",
            xaxis_title="Columns",
            yaxis_title="Count of Missing Values",
            template="plotly_white"
        )
        return fig  # Return the Plotly Figure object

    @staticmethod
    def log_message(message):
        print(f"Error: {message}")
