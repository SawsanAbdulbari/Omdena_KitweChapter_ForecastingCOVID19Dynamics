import pandas as pd
import numpy as np

# Define preprocessing function
def preprocess_differencing(main_dataframe, dataframe_with_last_known_value):
    """
    Preprocess the main dataframe by subtracting values from the dataframe_with_last_known_value.

    Parameters:
    main_dataframe (pd.DataFrame): The main dataframe containing 14 features. 
                                   This dataframe is expected to have one row of user input.
    dataframe_with_last_known_value (pd.DataFrame): The dataframe containing 6 features and their known values.
                                                    This dataframe is expected to have one row with known values.

    Returns:
    pd.DataFrame: A new dataframe with the same structure as the main_dataframe, 
                  where the values of the 6 matching features have been subtracted 
                  by their corresponding values in the dataframe_with_last_known_value.
    """
    # Identify the common columns
    common_columns = main_dataframe.columns.intersection(dataframe_with_last_known_value.columns)

    # Subtract the values of the known features
    for column in common_columns:
        main_dataframe[column] = main_dataframe[column] - dataframe_with_last_known_value[column]
        if main_dataframe[column].iloc[0] < 0:
            main_dataframe[column] = 0
        
    return main_dataframe

def preprocess_log(user_input, last_value):
    '''
    Preprocess a feature by taking a logarithm from the user's input and the last known value and then subtracting
    the last known value from the user's input.

    Parameters:
    user_input (pd.Series): The series containing one value which is user's input.
                            The series expects to have only one value.
    last_value (pd.Series): The series containing one value which is the last known value.
                            The series expects to have only one value.

    Returns:
    pd.Series: A new series with one preprocessed value.
    '''

    # Use np.log1p for safer logarithm calculation
    log_user_input = np.log1p(user_input)
    log_last_value = np.log1p(last_value)

    # Apply differencing
    transformed_value = log_user_input - log_last_value
    if transformed_value.iloc[0] < 0:
        transformed_value = 0

    return transformed_value