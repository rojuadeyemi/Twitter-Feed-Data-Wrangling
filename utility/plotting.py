import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utility.auxiliary import day_name, month_name


# This function Plots number of tweets within a year, for specific period
def plot_period(df, period):
    """
    INPUT:
    df : dataframe containing the attribute column
    period:  A string. that determines period tweets occurred. E.g hourly, monthly, daily
    """
    # Obtain years in the dataset
    years = df['year'].unique()
    years.sort()

    # Set colors
    colors = ['tab:blue', 'tab:brown', 'darkblue']

    # Group data based on the specified period
    period_dict = {
        'daily': (['year', 'day_number'], 'Day', day_name),
        'monthly': (['year', 'month_number'], 'Month', month_name),
        'hourly': (['year', 'hour_number', 'hour'], 'Hour', lambda x: x)
    }
    
    group_cols, x_lab, label_func = period_dict.get(period, (None, None, None))
    
    if not group_cols:
        raise ValueError("Invalid period. Choose from 'daily', 'monthly', 'hourly'.")

    df_grouped = df.groupby(group_cols)['tweet_id'].count().reset_index()

    # Create figure and polar axes of r rows, 1 column. r = number of years
    fig, axs = plt.subplots(len(years), 1, figsize=(17, 10), sharex=False)

    if len(years) == 1:
        axs = [axs]

    for id, year in enumerate(years):
        df_year = df_grouped[df_grouped['year'] == year]
        labels = df_year[group_cols[-1]].apply(label_func).tolist()
        values = df_year['tweet_id'].values
        
        # Plot each year
        sns.lineplot(x=np.arange(len(labels)), y=values, ax=axs[id], color=colors[id % len(colors)],markers=True,lw=1.1)
        
        # Set the ticks and ticklabels
        axs[id].set_xticks(np.arange(len(labels)))
        axs[id].set_xticklabels(labels)
        
        # Set plot labels
        axs[id].set_ylabel('Number of Tweets')
        axs[id].set_xlabel(x_lab)

        for x, y in zip(np.arange(len(labels)), values):
            axs[id].text(x, y, f'{y:.0f}', ha='center', va='bottom')
    
        # Add title
        axs[id].set_title(f'{period.title()} Total Tweets ({year})')

    # Adjust the spacing between subplots
    fig.tight_layout()

def plot_attributes(df, attrib, value, func, top=10):
    """
    Plots specified attribute.
    
    Parameters:
    df : DataFrame
        The dataframe containing the data.
    attrib : str
        A categorical variable to group by.
    value : str
        A continuous variable to aggregate.
    func : str
        Aggregation function ('sum' or 'mean').
    top : int, optional
        Determines number of categories to plot (default is 10).
    """
    # Validate the aggregation function
    if func not in ['sum', 'mean']:
        raise ValueError("Function must be 'sum' or 'mean'")

    ylab = 'Average' if func=='mean' else 'Total'
    # Group and aggregate the data
    aggregation = df.groupby(attrib)[value].agg(func).nlargest(top)
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plot the data
    sns.barplot(x=aggregation.index, y=aggregation.values, ax=ax, alpha=0.9,hue=aggregation.values,palette='viridis',legend=False)
    
    # Set labels and title
    plt.xticks(rotation=10)
    ax.set_ylim(0, aggregation.max() + aggregation.max() * 2 / top)
    ax.set_ylabel(ylab)
    ax.set_xlabel(attrib.title())
    ax.set_title(f'Top {top} {attrib.title()} by {value.replace("_", " ").title()}')
    # Add labels to the bars with comma separator
    for container in ax.containers:
        ax.bar_label(container, fmt='{:,.0f}', padding=3,fontsize=12)

    
    # Show plot
    plt.show()


def plot_attrib(attrib,xlabel,title):
    
    """
    This function plots the distribution of an attribute
    
    INPUT.
    attrib:  A categorical variable to plot
    title: str. Title of the plot
    xlabel: str. Label for x-axis
    """
    
    #Configure axes for ploting the attribute
    fig, ax = plt.subplots(figsize = (12,3))
    
    #plot the attribute
    ax = sns.barplot(x=attrib.index,y=attrib.values,hue=attrib.values,palette='viridis',legend=False,alpha=0.8)
    
    #set label and title
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_ylim([0,attrib.values.max()+10])
    plt.xticks(rotation=10)
    for container in ax.containers:
        ax.bar_label(container, fmt='{:,.0f}', padding=3,fontsize=10)