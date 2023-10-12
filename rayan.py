import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read and preprocess the dataset
airline = pd.read_csv("Airline Dataset.csv")

# Drop rows with missing values
airline.dropna(inplace=True)

# Convert 'Departure Date' to datetime if it's not already in datetime format
airline['Departure Date'] = pd.to_datetime(airline['Departure Date'], errors='coerce')

# Extract the year and create a new 'Year' column
airline['Year'] = airline['Departure Date'].dt.year

# Create a Streamlit app
st.title("Airline Data Analysis")

# Sidebar filters
st.sidebar.header("Filters")

# Age slider
min_age = int(airline['Age'].min())
max_age = int(airline['Age'].max())
selected_min_age = st.sidebar.slider("Select Minimum Age", min_age, max_age, min_age)
selected_max_age = st.sidebar.slider("Select Maximum Age", min_age, max_age, max_age)

# Flight status dropdown
flight_statuses = airline['Flight Status'].unique()
selected_flight_status = st.sidebar.selectbox("Select Flight Status", flight_statuses)

# Apply filters
filtered_data = airline[(airline['Age'] >= selected_min_age) & (airline['Age'] <= selected_max_age)
                        & (airline['Flight Status'] == selected_flight_status)]

# Display filtered data
# st.write("Filtered Data:")
# st.write(filtered_data)

# Histogram of passenger ages using Matplotlib for filtered data
st.subheader("Histogram of Passenger Ages (Filtered Data)")
fig_age_filtered = plt.figure(figsize=(8, 6))
plt.hist(filtered_data['Age'][:250], bins=20, density=True, alpha=0.6, color='g', edgecolor='k')
plt.title('Histogram of Passenger Ages (Filtered Data)')
plt.xlabel('Age')
plt.ylabel('Density')
st.pyplot(fig_age_filtered)


st.write("This histogram provides a visual representation of the age distribution of passengers. Each bar in the histogram corresponds to a range of ages, while the height of each bar indicates the frequency or number of passengers within that age range. Histograms are an effective way to explore the underlying patterns within a dataset, and in this case, it helps us understand the age demographics of the passengers. The histogram reveals insights into the central tendencies and spread of passenger ages. ")
# Top 10 Nationalities among passengers
st.subheader("Top 10 Nationalities Among Passengers (First 500 Records)")
top_nationalities_filtered = filtered_data['Nationality'][:500].value_counts().head(10).reset_index()
top_nationalities_filtered.columns = ['Nationality', 'Count']
fig_nationalities_filtered = px.sunburst(
    top_nationalities_filtered,
    path=['Nationality'],
    values='Count',
    title='Top 10 Nationalities Among Passengers (First 500 Records)'
)
fig_nationalities_filtered.update_traces(textinfo='label+percent parent')
st.plotly_chart(fig_nationalities_filtered)

# Animated bubble chart on a map
st.subheader("Distribution of Flights on World Map (Animated Bubble Chart)")
fig_map_filtered = px.scatter_geo(filtered_data[:1000],
                                  locations='Country Name',
                                  locationmode='country names',
                                  color='Flight Status',
                                  title='Distribution of Flights on World Map (Animated Bubble Chart)')
st.plotly_chart(fig_map_filtered)

# Box plot of passenger ages by continent
st.subheader("Box Plot of Passenger Ages by Continent")
fig_box_filtered = px.box(filtered_data.head(500), x='Continents', y='Age',
                           title='Box Plot of Passenger Ages by Continent')
st.plotly_chart(fig_box_filtered)

# Line chart of flight counts by month
st.subheader("Number of Flights by Month (First 1000 Records)")
filtered_data['Departure Date'] = pd.to_datetime(filtered_data['Departure Date'])
flight_counts_by_month_filtered = filtered_data[:1000].groupby(
    filtered_data['Departure Date'].dt.to_period('M')).size().reset_index(name='Flight Count')
flight_counts_by_month_filtered['Departure Date'] = flight_counts_by_month_filtered[
    'Departure Date'].dt.strftime('%Y-%m')
fig_line_filtered = px.line(flight_counts_by_month_filtered, x='Departure Date', y='Flight Count',
                            title='Number of Flights by Month (First 1000 Records)',
                            labels={'Departure Date': 'Month', 'Flight Count': 'Flight Count'})
fig_line_filtered.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig_line_filtered)
