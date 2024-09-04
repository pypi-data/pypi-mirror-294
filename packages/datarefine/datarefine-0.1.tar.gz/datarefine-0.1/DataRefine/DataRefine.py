import streamlit as st
import pandas as pd
from missing import MissingDataHandler
from outliers import OutlierHandler
import plotly.graph_objects as go
import io

# Page 1: Project Name, Logo, and CSV Upload
def show_upload_page():
    st.set_page_config(
        layout="centered",
        page_title="DataRefine",
        page_icon="drlogo2.jpeg",
        initial_sidebar_state="expanded"
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='color: #2a98bd;'>DataRefine</h1>", unsafe_allow_html=True)
        st.image("drlogo2.jpeg", width=200)
    
    st.write("Upload a CSV file to start cleaning..")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.handler = MissingDataHandler(df)
            st.session_state.outlier_handler = OutlierHandler(df)
            
            st.markdown("<p style='color: #2a98bd;'>File uploaded successfully!</p>", unsafe_allow_html=True)
            if st.button("Go to Data Cleaning"):
                st.session_state.page = 'analysis'
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Page 2: Data Cleaning
def show_analysis_page():
    st.set_page_config(
        layout="wide",
        page_title="DataRefine",
        page_icon="drlogo2.jpeg",
        initial_sidebar_state="expanded"
    )
    
    if 'df' in st.session_state:
        handler = st.session_state.handler
        outlier_handler = st.session_state.outlier_handler
        df = st.session_state.df
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        
        st.sidebar.header("Data Cleaning")
        
        action = st.sidebar.selectbox("Select Action", [
            "Data Overview",
            "Missing Values",
            "Outliers"
        ])
        
        if action == "Data Overview":
            st.markdown("<h2 style='color: #2a98bd;'>Data Overview</h2>", unsafe_allow_html=True)
            st.write("**Data Shape:**")
            st.write(df.shape)
            
            st.write("**Dataframe:**")
            st.write(df)
            
            st.write("**Data Information:**")
            buffer = io.StringIO()
            df.info(buf=buffer)
            buffer.seek(0)
            
            info_lines = buffer.getvalue().splitlines()
            data_lines = info_lines[5:-2]
            
            if data_lines:
                table_data = []
                for line in data_lines:
                    parts = line.split()
                    if len(parts) >= 3:
                        column = ' '.join(parts[:-2])
                        non_null_count = parts[-2] + ' ' + parts[-1]
                        dtype = parts[-3]
                        column = ' '.join(part.lstrip('0123456789') for part in column.split())
                        table_data.append([column, non_null_count, dtype])
                
                table_df = pd.DataFrame(table_data, columns=["Column", "Dtype", "Non-Null Count"])
                st.write(table_df)
        
        elif action == "Missing Values":
            st.markdown("<h2 style='color: #2a98bd;'>Missing Values Detection and Handling</h2>", unsafe_allow_html=True)
            
            st.write("**DataFrame with Missing Values**")
            st.write(df)
            
            st.plotly_chart(handler.plot_missing_values(df))
            
            st.sidebar.write("### Handle Missing Values")
            columns = st.sidebar.multiselect("Select Columns for Imputation", options=df.columns.tolist(), default=df.columns.tolist())
            strategy = st.sidebar.selectbox("Select Imputation Strategy", ["mean", "median", "most_frequent", "predictive", "custom"])
            fill_value = None
            if strategy == "custom":
                fill_value = st.sidebar.text_input("Fill Value", value="0")

            if st.sidebar.button("Impute Missing Values"):
                with st.spinner("Imputing missing values..."):
                    try:
                        df_subset = df[columns].copy() if columns else df.copy()
                        df_imputed = handler.impute_missing(strategy, fill_value=fill_value, dataframe=df_subset)
                        if columns:
                            df[columns] = df_imputed
                        else:
                            df = df_imputed
                        st.session_state.df = df
                        
                        st.write("### DataFrame After Imputation:")
                        st.write(df)
                        st.plotly_chart(handler.plot_missing_values(df))
                        st.success("Missing values imputed successfully.")
                    except Exception as e:
                        st.error(f"Error during imputation: {e}")
        
        elif action == "Outliers":
            st.markdown("<h2 style='color: #2a98bd;'>Outlier Detection and Handling</h2>", unsafe_allow_html=True)
            method = st.sidebar.selectbox("Select Outlier Detection Method", ["zscore", "iqr", "isolation_forest", "lof"])
            threshold = st.sidebar.slider("Select Threshold", 0.0, 5.0, 3.0, 0.1)
            
            try:
                st.write("**Original DataFrame:**")
                st.write(df)

                outliers_df, outlier_counts = outlier_handler.detect_outliers(method=method, threshold=threshold)
                
                
                
                st.plotly_chart(outlier_handler.plot_outliers(outlier_counts))
                
                st.sidebar.write("### Handle Outliers")
                handling_method = st.sidebar.selectbox("Select Outlier Handling Method", ["remove", "cap", "impute"])
                
                if st.sidebar.button("Handle Outliers"):
                    with st.spinner("Handling outliers..."):
                        try:
                            # Handle outliers only in numerical columns
                            df_handled, old_outlier_counts, new_outlier_counts = outlier_handler.handle_outliers(
                                method=handling_method,
                                detection_method=method,
                                threshold=threshold
                            )
                            st.session_state.df = df_handled
                            
                            st.write("### DataFrame After Outlier Handling:")
                            st.write(df_handled)
                            
                            st.write("### Outlier Counts After Handling:")
                            new_outlier_counts_df = pd.DataFrame(list(new_outlier_counts.items()), columns=['Column', 'Outlier Count'])
                            st.write(new_outlier_counts_df)
                            
                            st.plotly_chart(outlier_handler.plot_outliers(new_outlier_counts))
                            st.success("Outliers handled successfully.")
                        except Exception as e:
                            st.error(f"Error handling outliers: {e}")
            except Exception as e:
                st.error(f"Error detecting outliers: {e}")

# Main app logic
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'
    
    if st.session_state.page == 'upload':
        show_upload_page()
    elif st.session_state.page == 'analysis':
        show_analysis_page()

if __name__ == "__main__":
    main()
