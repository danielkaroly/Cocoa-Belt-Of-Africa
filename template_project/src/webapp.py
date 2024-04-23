import pandas as pd
import plotly.express as px
import streamlit as st
from preprocessing import total_production_df
from preprocessing import grouped_df
from helper import year_over_year
from helper import plot_cocoa_production
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Title and data source
st.markdown("""
<div style='text-align: center'>
    <h1>Cocoa Belt of Africa 🍫</h1>
</div>
""", unsafe_allow_html=True)
url = "https://www.fao.org/faostat/en/#data/QCL"
st.markdown(f"""
<div style='text-align: center'>
    Data Source: <a href='{url}' target='_blank'>{url}</a>
</div>
""", unsafe_allow_html=True)




# Implementing a checkbox to toggle total production
if st.sidebar.checkbox("Total Cocoa Production Over Time"):
    

    fig_total_production = px.line(total_production_df, x='Year', y='Total Production', title='Total Cocoa Production Over Time')

    fig_total_production.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Cocoa Production (tons)',
        title_x=0.30,
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=True),   
    )
    st.plotly_chart(fig_total_production)


# Implementing checkbox to toggle High and low production countries
if st.sidebar.checkbox("Cocoa Production Comparison"):
    #st.header("Cocoa Production of Comparison of High and Low Productuion Countries")
    # Assuming 'grouped_df' is your DataFrame and you've identified high and low production countries
    high_prod_countries = ['Nigeria', 'Ghana', 'Côte d\'Ivoire', 'Cameroon']
    low_prod_countries = [country for country in grouped_df.columns if country not in high_prod_countries]

    # Define a color sequence that will be used for both high and low production countries
    color_sequence_high = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Example colors for high production countries
    color_sequence_low = ['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']  # Example colors for low production

    # Create the subplot figure
    fig = make_subplots(rows=2, cols=1, subplot_titles=('High Production Countries', 'Low Production Countries'))

    # Add traces for high production countries
    for i, country in enumerate(high_prod_countries):
        fig.add_trace(
            go.Bar(
                x=grouped_df.index,  # The years
                y=grouped_df[country],
                name=country,
                marker_color=color_sequence_high[i]  # Set the bar color using the sequence
            ),
            row=1, col=1
        )

    # Add traces for low production countries
    for i, country in enumerate(low_prod_countries):
        # Use modulo to cycle through the color sequence for low production countries
        color = color_sequence_low[i % len(color_sequence_low)]
        fig.add_trace(
            go.Bar(
                x=grouped_df.index,  # The years
                y=grouped_df[country],
                name=country,
                marker_color=color  # Set the bar color
            ),
            row=2, col=1
        )

    # Update the layout
    fig.update_layout(
        barmode='stack',
        title={'text': "Cocoa Production Comparison", 'x': 0.225},
        xaxis_title="Year",
        yaxis_title="Cocoa Production (tons)",
        legend_title="Country",
        height=800
    )

    # Show the figure
    st.plotly_chart(fig)


emoji_map = {
    'Cameroon': '🇨🇲',  
    'Ghana': '🇬🇭',  
    'Equatorial Guinea': '🇬🇶',  
    'Gabon': '🇬🇦',  
    'Democratic Republic of the Congo': '🇨🇩',  
    'Congo': '🇨🇬',  
    'Côte d\'Ivoire': '🇨🇮',  
    'Nigeria': '🇳🇬',  
    'Sao Tome and Principe': '🇸🇹',  
    'Sierra Leone': '🇸🇱',  
    'Togo': '🇹🇬',  
}

if st.sidebar.checkbox("Cocoa Production of individual countries"):
    #st.header("Cocoa Production of individual countries")
    
    # Dropdown for selecting the country
    countries = grouped_df.columns.tolist()
    country_name = st.selectbox("Choose a country", countries)

    # Display the emoji as a subheader
    emoji = emoji_map.get(country_name, '')  # Get the emoji from the map
    if emoji:
        st.markdown(f"<h3 style='text-align: center;'>{emoji} {country_name}</h3>", unsafe_allow_html=True)

    # Button to generate plots
    if st.button("Generate Plots"):
        yoy_data = year_over_year(grouped_df[country_name])
        plot_cocoa_production(grouped_df, country_name, yoy_data)


    
