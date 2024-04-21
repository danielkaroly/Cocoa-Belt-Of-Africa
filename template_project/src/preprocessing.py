import pandas as pd

file_path = '../data/raw/FAOSTAT_data_en_4-5-2024-combined.csv'

df = pd.read_csv(file_path)

new_df = df.drop(columns=['Domain Code', 'Domain', 'Area Code (M49)','Element Code',
       'Element', 'Item Code (CPC)', 'Item', 'Year Code',
       'Flag', 'Flag Description', 'Note', 'Unit'], inplace=False)

new_df.rename(columns={"Area": "Country", "Value": "Cocoa Production (tons)"}, inplace =True)

# Round the Cocoa Production(tons) to whole numbers for better readability
new_df["Cocoa Production (tons)"] = new_df["Cocoa Production (tons)"].round(0).astype(int)

# The data is in long format which is good for databases but not good for readability and analysis
pivoted_df = new_df.pivot(index="Country", columns="Year", values="Cocoa Production (tons)")

# Adding a total production row per year across all countries to show the overall production trends.
total_production_per_year = pivoted_df.sum(axis=0)
total_production_df = total_production_per_year.to_frame(name="Total Production")
total_production_df.reset_index(inplace=True)
total_production_df.rename(columns={"index":"Year"}, inplace=True)

# Altered df so that the index is the years and the columns are the countries
grouped_df = new_df.groupby(["Year", "Country"])["Cocoa Production (tons)"].sum().unstack()

