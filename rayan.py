import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
dataset = pd.read_csv("Airline Dataset.csv")
airline = dataset.copy()

# Check for missing values in each row
missing_rows = airline.isnull().any(axis=1)
missing_data = airline[missing_rows]

# Replace inf values with NaN
airline.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop rows with missing values
airline.dropna(inplace=True)

# Convert 'Departure Date' to datetime
airline['Departure Date'] = pd.to_datetime(airline['Departure Date'], errors='coerce')

# Extract the year and create a new 'Year' column
airline['Year'] = airline['Departure Date'].dt.year

# Create a Streamlit app
st.title("Airline Data Analysis")

# Display missing data (if any)
if not missing_data.empty:
    st.subheader("Missing Data")
    st.write(missing_data)

# Histogram of passenger ages
st.subheader("Histogram of Passenger Ages")
fig_age = plt.figure(figsize=(8, 6))
sns.histplot(data=airline[:250], x='Age', bins=20, kde=True)
plt.title('Histogram of Passenger Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
st.pyplot(fig_age)

# Top 10 Nationalities among passengers
st.subheader("Top 10 Nationalities Among Passengers (First 500 Records)")
top_nationalities = airline['Nationality'][:500].value_counts().head(10).reset_index()
top_nationalities.columns = ['Nationality', 'Count']
fig_nationalities = px.sunburst(
    top_nationalities,
    path=['Nationality'],
    values='Count',
    title='Top 10 Nationalities Among Passengers (First 500 Records)'
)
fig_nationalities.update_traces(textinfo='label+percent parent')
st.plotly_chart(fig_nationalities)

# Animated bubble chart on a map
st.subheader("Distribution of Flights on World Map (Animated Bubble Chart)")
fig_map = px.scatter_geo(airline[:1000],
                         locations='Country Name',
                         locationmode='country names',
                         color='Flight Status',
                         title='Distribution of Flights on World Map (Animated Bubble Chart)')
st.plotly_chart(fig_map)

# Box plot of passenger ages by continent
st.subheader("Box Plot of Passenger Ages by Continent")
fig_box = px.box(airline.head(500), x='Continents', y='Age',
                 title='Box Plot of Passenger Ages by Continent')
st.plotly_chart(fig_box)

# Line chart of flight counts by month
st.subheader("Number of Flights by Month (First 1000 Records)")
airline['Departure Date'] = pd.to_datetime(airline['Departure Date'])
flight_counts_by_month = airline[:1000].groupby(airline['Departure Date'].dt.to_period('M')).size().reset_index(name='Flight Count')
flight_counts_by_month['Departure Date'] = flight_counts_by_month['Departure Date'].dt.strftime('%Y-%m')
fig_line = px.line(flight_counts_by_month, x='Departure Date', y='Flight Count',
                   title='Number of Flights by Month (First 1000 Records)',
                   labels={'Departure Date': 'Month', 'Flight Count': 'Flight Count'})
fig_line.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig_line)
