import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import plotly.graph_objs as go

class OutlierHandler:
    def __init__(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if not any(dataframe.select_dtypes(include=[np.number]).columns):
            raise ValueError("DataFrame must contain numeric columns for outlier handling")
        self.original_dataframe = dataframe.copy()
        self.dataframe = dataframe.select_dtypes(include=[np.number])
    
    def detect_outliers(self, method='zscore', threshold=3.0, **kwargs):
        if method == 'zscore':
            z_scores = np.abs((self.dataframe - self.dataframe.mean()) / self.dataframe.std())
            outliers = (z_scores > threshold)
        elif method == 'iqr':
            Q1 = self.dataframe.quantile(0.25)
            Q3 = self.dataframe.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.dataframe < (Q1 - threshold * IQR)) | (self.dataframe > (Q3 + threshold * IQR)))
        elif method == 'isolation_forest':
            iso_forest = IsolationForest(**kwargs)
            outlier_predictions = iso_forest.fit_predict(self.dataframe)
            outliers = pd.DataFrame(outlier_predictions, index=self.dataframe.index, columns=['outlier'])
            outliers['outlier'] = outliers['outlier'] == -1
        elif method == 'lof':
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(self.dataframe)
            if 'n_neighbors' not in kwargs:
                kwargs['n_neighbors'] = min(20, len(self.dataframe) - 1)
            lof = LocalOutlierFactor(**kwargs)
            lof_scores = lof.fit_predict(scaled_data)
            outliers = pd.DataFrame(lof_scores, index=self.dataframe.index, columns=['outlier'])
            outliers['outlier'] = outliers['outlier'] == -1
        else:
            raise ValueError("Unsupported outlier detection method")
        
        outlier_counts = outliers.sum(axis=0).to_dict()

        return outliers, outlier_counts

    def handle_outliers(self, method='remove', detection_method='zscore', threshold=3.0, **kwargs):
        outliers, outlier_counts = self.detect_outliers(method=detection_method, threshold=threshold, **kwargs)
        
        if method == 'remove':
            self.dataframe = self.dataframe[~outliers.any(axis=1)]
        elif method == 'cap':
            for column in self.dataframe.columns:
                Q1 = self.dataframe[column].quantile(0.25)
                Q3 = self.dataframe[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                self.dataframe[column] = np.where(self.dataframe[column] < lower_bound, lower_bound, self.dataframe[column])
                self.dataframe[column] = np.where(self.dataframe[column] > upper_bound, upper_bound, self.dataframe[column])
        elif method == 'impute':
            imputer = SimpleImputer(strategy='mean')
            self.dataframe = pd.DataFrame(imputer.fit_transform(self.dataframe), columns=self.dataframe.columns, index=self.dataframe.index)
        else:
            raise ValueError("Unsupported outlier handling method")

        # Update the full DataFrame with proper index alignment
        self.original_dataframe.update(self.dataframe)

        new_outliers, new_outlier_counts = self.detect_outliers(method=detection_method, threshold=threshold, **kwargs)

        return self.original_dataframe, outlier_counts, new_outlier_counts

    def plot_outliers(self, outlier_counts):
        fig = go.Figure()
        for column, count in outlier_counts.items():
            fig.add_trace(go.Bar(x=[column], y=[count], name=column))
        
        fig.update_layout(
            title="Outlier Counts per Column",
            xaxis_title="Columns",
            yaxis_title="Outlier Count",
            barmode='group'
        )
        return fig
