import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from itertools import cycle


def year_over_year(series):
    """
    Calculate the Year-over-Year percentage change of a pandas Series.
    
    Parameters:
    series (pd.Series): A pandas Series where the index represents time (e.g., year) 
                        and the values represent the measurement (e.g., production).
                        
    Returns:
    pd.Series: A pandas Series with the Year-over-Year percentage change.
    """
    # Calculate the YOY percentage change and convert to percentage format, rounded to two decimal places
    yoy_change_percentage = (series.pct_change() * 100).round(2)
    
    # Handle the NaN value for the first year
    yoy_change_percentage.iloc[0] = 0
    
    return yoy_change_percentage



# Define a list of colors to cycle through. 11 colors for the 11 countries
colors = cycle(['green', 'blue', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'grey', 'brown'])

def plot_cocoa_production(grouped_df, country, yoy_data):
    """
    Plot cocoa production and its year-over-year change for a specific country using stacked bar charts.

    This function creates two vertically stacked bar charts. The top chart displays the absolute cocoa production
    of the specified country over time, while the bottom chart shows the year-over-year percentage change in 
    production. Both charts are plotted on a common timeline.

    Parameters:
    grouped_df (pd.DataFrame): A pandas DataFrame containing cocoa production data, where the index represents
                               the time (e.g., year) and each column represents production data for a different
                               country.
    country (str): The name of the country for which the cocoa production and its YoY change should be plotted.
                   This should be one of the column names in grouped_df that contains the production data.
    yoy_data (pd.Series): A pandas Series containing the year-over-year change in production, expressed as
                          percentages. The index should match that of grouped_df.

    Returns:
    None: This function outputs a plot and does not return any value. It uses Plotly to generate and show
          the interactive charts.
    """
    color = next(colors)  # Get the next color from the cycle

    fig = make_subplots(rows=2, cols=1, subplot_titles=(
        f"Cocoa Production of {country} Over Time",
        f"Year over Year Change in the Cocoa Production of {country} Over Time"
    ))

    # First subplot for absolute production
    fig.add_trace(
        go.Bar(
            x=grouped_df.index,
            y=grouped_df[country],
            marker_color=color
        ),
        row=1, col=1
    )
    
    # Second subplot for year over year change
    fig.add_trace(
        go.Bar(
            x=yoy_data.index,
            y=yoy_data,
            marker_color=color
        ),
        row=2, col=1
    )
    
    # Update the layout of the figure to format axis titles and improve overall presentation
    fig.update_layout(
        height=700,
        showlegend=False,
        xaxis_title="Year",
        yaxis_title="Cocoa Production (tons)",
        xaxis2_title="Year",
        yaxis2_title="Percentage Change"
    )
    fig.show()
