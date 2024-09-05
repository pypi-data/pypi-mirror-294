import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import logging
from typing import Dict, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MissingValueImputation:
    def __init__(self, strategies: Dict[str, Union[str, int, float]] = None):
        """
        Initialize the MissingValueImputation class with a dictionary of strategies.
        
        Parameters:
        strategies (dict): A dictionary where keys are column names and values are 
                           the imputation strategies ('mean', 'median', 'mode', or a custom number or value).
        """
        self.strategies = strategies or {}
        self.fill_values = {}
        self.logger = logging.getLogger(__name__)

    def _compute_fill_value(self, df: pd.DataFrame, column: str, strategy: Union[str, int, float]) -> Union[float, str]:
        """
        Compute the fill value based on the imputation strategy for a given column.
        
        Parameters:
        df (pd.DataFrame): The dataframe to compute fill values from.
        column (str): The column name for which to compute the fill value.
        strategy (Union[str, int, float]): The imputation strategy to use ('mean', 'median', 'mode', or a custom number or value).
        
        Returns:
        Union[float, str]: The computed fill value based on the strategy.
        
        Raises:
        ValueError: If the strategy is not applicable or unsupported.
        """
        self.logger.debug(f"Computing fill value for column '{column}' with strategy '{strategy}'")
        if isinstance(strategy, (int, float)):
            return strategy
        elif strategy == 'mean':
            if pd.api.types.is_numeric_dtype(df[column]):
                return df[column].mean()
            else:
                self.logger.error(f"Mean strategy is not applicable for non-numeric column '{column}'.")
                raise ValueError(f"Mean strategy is not applicable for non-numeric column {column}.")
        elif strategy == 'median':
            if pd.api.types.is_numeric_dtype(df[column]):
                return df[column].median()
            else:
                self.logger.error(f"Median strategy is not applicable for non-numeric column '{column}'.")
                raise ValueError(f"Median strategy is not applicable for non-numeric column {column}.")
        elif strategy == 'mode':
            return df[column].mode().iloc[0]
        else:
            self.logger.error(f"Strategy '{strategy}' not supported.")
            raise ValueError(f"Strategy {strategy} not supported. Please use 'mean', 'median', 'mode', or a custom number or value.")

    def fit(self, df: pd.DataFrame) -> 'MissingValueImputation':
        """
        Compute the fill values for missing data based on the provided strategies.
        
        Parameters:
        df (pd.DataFrame): The dataframe to compute fill values from.
        
        Returns:
        self: The instance of MissingValueImputation with computed fill values.
        """
        self.logger.info("Fitting MissingValueImputation with the provided DataFrame.")
        for column, strategy in self.strategies.items():
            if column not in df.columns:
                self.logger.error(f"Column '{column}' is not present in the DataFrame.")
                raise ValueError(f"Column {column} is not present in the DataFrame.")
            self.fill_values[column] = self._compute_fill_value(df, column, strategy)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the imputation to the dataframe using the computed fill values.
        
        Parameters:
        df (pd.DataFrame): The dataframe to apply imputation to.
        
        Returns:
        pd.DataFrame: The dataframe with missing values filled.
        """
        self.logger.info("Transforming DataFrame using the computed fill values.")
        for column, fill_value in self.fill_values.items():
            if column not in df.columns:
                self.logger.error(f"Column '{column}' is not present in the DataFrame.")
                raise ValueError(f"Column {column} is not present in the DataFrame.")
            df[column] = df[column].fillna(fill_value)
            self.logger.debug(f"Filled missing values in column '{column}' with '{fill_value}'.")
        return df

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the fill values and apply the imputation to the dataframe in one step.
        
        Parameters:
        df (pd.DataFrame): The dataframe to fit and transform.
        
        Returns:
        pd.DataFrame: The dataframe with missing values filled.
        """
        self.logger.info("Fitting and transforming DataFrame in one step.")
        self.fit(df)
        return self.transform(df)

def display_dataframe(df):
    """
    Display a DataFrame using AgGrid in Streamlit.
    
    Parameters:
    df (pd.DataFrame): The dataframe to display.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gb.configure_side_bar()
    grid_options = gb.build()
    
    AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="streamlit"
    )

def main():
    st.title("FEATUREWISE")

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            if 'original_df' not in st.session_state:
                st.session_state.original_df = pd.read_csv(uploaded_file)
                st.session_state.df = st.session_state.original_df.copy()

            st.write("### Uploaded DataFrame")
            display_dataframe(st.session_state.df)

        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
            return
        except pd.errors.ParserError:
            st.error("There was an issue parsing the CSV file. Please ensure it is formatted correctly.")
            return
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            return

        st.sidebar.title("Imputation Toolbox")
        st.sidebar.header("Imputation Settings")
        strategies = {}
        try:
            for column in st.session_state.df.columns:
                if st.session_state.df[column].isnull().any():
                    strategy = st.sidebar.selectbox(
                        f"Select strategy for {column}",
                        ["mean", "median", "mode", "custom"],
                        key=column
                    )
                    if strategy == "custom":
                        custom_value = st.sidebar.number_input(f"Enter custom value for {column}", key=f"{column}_custom")
                        strategies[column] = custom_value
                    else:
                        strategies[column] = strategy

            if st.sidebar.button("Apply Imputation"):
                imputer = MissingValueImputation(strategies=strategies)
                st.session_state.df = imputer.fit_transform(st.session_state.df)
                st.write("### DataFrame After Imputation")
                display_dataframe(st.session_state.df)

        except KeyError as e:
            st.error(f"Column not found: {e}")
        except Exception as e:
            st.error(f"An error occurred during imputation: {e}")

        st.sidebar.markdown("### Download Transformed Data")
        try:
            csv = st.session_state.df.to_csv(index=False)
            st.sidebar.download_button("Download Transformed CSV", csv, "transformed_data.csv", "text/csv")
        except Exception as e:
            st.error(f"Error generating download: {e}")

if __name__ == "__main__":
    main()
