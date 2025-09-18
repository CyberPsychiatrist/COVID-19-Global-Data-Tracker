import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Load the dataset
df = pd.read_csv('data/covid19_data.csv')

# Check columns
print(df.columns)

# Preview rows
print(df.head())

# Filter countries of interest and drop missing values
filtered_df = df[df['location'].isin(['Kenya', 'India'])]

# Drop rows with missing dates/critical values
cleaned_df = filtered_df.dropna(subset=['date'])

# Exploratory Data Analysis (EDA)
st.title('Exploratory Data Analysis')

# Plot total cases over time for selected countries
fig, ax = plt.subplots(figsize=(10, 6))
for country in ['Kenya', 'India']:
    data = cleaned_df[cleaned_df['location'] == country]
    if 'total_cases' in data.columns and 'new_cases' in data.columns:
        data.plot(kind='scatter', x='total_cases', y='new_cases', ax=ax)
    else:
        st.write(f"Data for {country} does not contain both 'total_cases' and 'new_cases'.")
plt.title('Total Cases vs New Cases by Country')
plt.xlabel('Total Cases')
plt.ylabel('New Cases')

# Visualizing Vaccination Progress
st.title('Vaccination Progress')

fig, ax = plt.subplots(figsize=(10, 6))
for country in ['Kenya', 'India']:
    data = cleaned_df[cleaned_df['location'] == country]
    if 'total_vaccinations' in data.columns:
        data.plot(kind='line', x='date', y='total_vaccinations', ax=ax)
    else:
        st.write(f"Data for {country} does not contain 'total_vaccinations'.")
plt.title('Cumulative Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Vaccinations')

# Compare % vaccinated population with pie charts
fig, ax = plt.subplots(figsize=(10, 6))
for country in ['Kenya', 'India']:
    data = cleaned_df[cleaned_df['location'] == country]
    if 'percentage_vaccinated' in data.columns:
        data.plot(kind='pie', labels=country, autopct='%1.1f%%')
    else:
        st.write(f"Data for {country} does not contain 'percentage_vaccinated'.")
plt.title('Percentage Vaccinated Population')

# Optional: Build a Choropleth Map
st.title('Choropleth Map')

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
latest_date = cleaned_df['date'].max()
latest_data = cleaned_df[cleaned_df['date'] == latest_date]
merged_df = world.merge(latest_data, left_on='iso_code', right_on='location')

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(merged_df[['total_cases', 'new_cases']].corr(), annot=True)
plt.title('Correlation between Total Cases and New Cases')
plt.xlabel('Country')
plt.ylabel('Country')
st.pyplot(fig)