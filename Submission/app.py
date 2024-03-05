import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

all_data = pd.read_csv('https://raw.githubusercontent.com/Ashurinnn123/Data_Analyst_Dicoding/main/Submission/main_data.csv')

datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

def create_month_recap(df):
    plot_month = df['month'].astype(str)
    plot_year = df['year'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['total_sum'] = df.groupby('year_month')['total'].transform('sum')
    return df[['year_month', 'total_sum']]


def create_season_recap(df):
    season_recap = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_recap


def create_weather_recap(df):
    weather_recap = df.groupby(by='weather').agg({
    'total': 'mean'
    }).reset_index()
    return weather_recap

max_date = pd.to_datetime(all_data['date']).dt.date.max()
min_date = pd.to_datetime(all_data['date']).dt.date.min()

with st.sidebar:

    start_date, end_date = st.date_input(
        label='Pilih  Rentang Waktu',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    st.write(
        """ 
        **Prabu Shakti Parama P.S**\n
        Dicoding ID: **prabu_shakti**\n
        Email: **m258d4ky1563@bangkit.academy**
        """
    )

main_df = all_data[(all_data['date'] >= str(start_date)) & 
                (all_data['date'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)

# Membuat UI
st.header('BIKE SHARING ANALYTICS DASHBOARD')

st.subheader('Hubungan Antara Kondisi Kelembaban dan Jumlah Sewa Sepeda Perhari')
plt.figure(figsize=(10, 6))
sns.set(style='whitegrid')
sns.lineplot(
    data=main_df,  
    x='temp',  
    y='total',  
    marker='o'
)
plt.title("Hubungan Antara Kondisi Kelembaban dan Jumlah Sewa Sepeda Perhari")
plt.xlabel("Kelembaban Udara")
plt.ylabel("Jumlah Sewa")

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)

# Subheader Season and Weather Recap
st.subheader('Recap Musim dan Cuaca')

# Create a subplot with a figure size of 20x10
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y='registered',
    x='season',
    data=season_recap_df.sort_values(by='registered', ascending=False),
    color='tab:blue',
    label='Registered User',
    ax=ax
)

sns.barplot(
    y='casual',
    x='season',
    data=season_recap_df.sort_values(by='casual', ascending=False),
    color='tab:orange',
    label='Casual User',
    ax=ax
)

ax.set_title('Sepeda yang Paling Banyak dan Paling Sedikit Direntalkan Setiap Musim', loc='center', fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.legend(fontsize=20)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)

# Subheader Monthly Recap
st.subheader('Total Sepeda yang Direntalkan Setiap Bulan Antara Tahun 2011 Hingga 2012')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['total_sum'],
    marker='o',
    linewidth=5,
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)
