import numpy as np
# Day number converter function
def day_name(x):
    """
    x: int. 0 <= x <= 6
    OUTPUT: Weekday name
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekdays[x]

    
# Month number converter function   
def month_name(x):
    """
    x: int. 1 <= x <= 12
    OUTPUT: Month name
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return months[x-1]


# Defining the function to remove the outliers

def discard_outliers(dataframe, column):
    '''
    the function take a dataframe and a column as argument 
    cut the outlier of the dataframe
    and return the new dataframe shape
    '''
    q3 = dataframe[column].quantile(0.75)
    q1 = dataframe[column].quantile(0.25)
    IQR = q3 - q1
    out_1 = q1 - 1.5*IQR
    out_2 = q3 + 1.5*IQR
    dataframe = dataframe.loc[((dataframe[column] > out_1) & (dataframe[column] < out_2))]
    return dataframe


# Define a function to replace with 2nd or 3rd where 1st prediction is not a dog
def get_dog(x):
    
    """
    This functions takes a row object, 
    and uses it to extract the breed of a dog by first check the 1st algorithm, then 2nd and 3rd.
    
    Output: tupple of breed and confidence level
    """
    if x['p1_dog']:
        return x['p1'], x['p1_conf']
    elif x['p2_dog']:
        return x['p2'], x['p2_conf']
    elif x['p3_dog']:
        return x['p3'], x['p3_conf']
    else: return np.nan, np.nan