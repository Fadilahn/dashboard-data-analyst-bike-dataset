import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
df = pd.read_csv("day.csv")

# Set page title
st.title('Bike Sharing Dataset Dashboard')

# Sidebar
st.sidebar.title('Informasi Pribadi')
with st.sidebar:
    st.markdown("""
    **Nama:** Muhammad Fadhillah Nursyawal\n
    **Email:** fadilahnursyawal@gmail.com\n
    **ID Dicoding:**
    """)

# Convert 'dteday' column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# # Date filter
# st.sidebar.subheader('Filter Tanggal')

# # Get minimum and maximum dates from the dataframe
# min_date = df['dteday'].min()
# max_date = df['dteday'].max()

# start_date = st.sidebar.date_input('Tanggal Mulai', min_value=min_date, max_value=max_date)
# end_date = st.sidebar.date_input('Tanggal Akhir', min_value=min_date, max_value=max_date)

# # Filter data based on selected dates
# df_filtered = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]


# Create visualizations
st.header('Proyek Analisis Data: Bike Sharing Dataset')

# Informasi Analisis Data
st.subheader('Informasi Analisis Data')
st.write("""
Proyek Analisis Data ini bertujuan untuk menganalisis dataset Bike Sharing, dengan fokus pada dua pertanyaan bisnis utama:

1. Bagaimana pola penyewaan sepeda berdasarkan musim?
2. Faktor cuaca apa saja yang paling berpengaruh terhadap jumlah penyewaan sepeda?
""")

# Preprocessing data
df['season_name'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df['workingday_name'] = df['workingday'].map({0: 'Non-working day', 1: 'Working day'})
df['holiday_name'] = df['holiday'].map({0: 'Non-holiday', 1: 'Holiday'})
df['weathersit_name'] = df['weathersit'].map({1: 'Cerah/Clear',
                                             2: 'Berawan/Mist',
                                             3: 'Hujan Ringan',
                                             4: 'Hujan Lebat'})

# Menampilkan informasi dataset
st.subheader('Informasi Dataset')
st.write(df.head())

# Visualisasi dan Analisis Data
st.header('Visualisasi dan Analisis Data')

## Pertanyaan 1: Bagaimana pola penyewaan sepeda berdasarkan musim?
st.subheader('Pertanyaan 1: Pola Penyewaan Sepeda Berdasarkan Musim')

### Visualisasi Grafik Garis
st.write("""
Grafik garis di bawah ini menampilkan pola penyewaan sepeda berdasarkan musim dari rentang waktu yang telah dipilih.
""")

# Visualize pattern of bike rentals based on season
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='dteday', y='cnt', hue='season_name')
plt.title('Pola Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot()

# Menghitung rata-rata penyewaan sepeda berdasarkan musim dan mengurutkannya
avg_rental_by_season = df.groupby('season_name')['cnt'].mean().sort_values(ascending=False)

# Mencari musim dengan rata-rata penyewaan tertinggi
max_rental_season = avg_rental_by_season.idxmax()

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Bar Plot untuk rata-rata penyewaan sepeda berdasarkan musim
axes[0].bar(avg_rental_by_season.index, avg_rental_by_season, color=['skyblue' if season != max_rental_season else 'blue' for season in avg_rental_by_season.index])
axes[0].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
axes[0].set_xlabel('Musim')
axes[0].set_ylabel('Rata-rata Penyewaan')
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Box Plot untuk perbandingan distribusi jumlah peminjaman sepeda berdasarkan musim
sns.boxplot(data=df, x='season_name', y='cnt', ax=axes[1])
axes[1].set_title('Perbandingan Distribusi Jumlah Peminjaman Sepeda')
axes[1].set_xlabel('Musim')
axes[1].set_ylabel('Jumlah Peminjaman')

plt.tight_layout()
st.pyplot(fig)

### Analisis
st.write("""
dari grafik waktu diatas dapat dilihat pola yang sama berulang dari tahun 2011 - 2012 per musim, musim yang paling sedikit yaitu spring (dingin/salju) sedangakan yang paling banyak penyewaannya musim gugur (fall)
""")

## Pertanyaan 2: Faktor cuaca apa saja yang paling berpengaruh terhadap jumlah penyewaan sepeda?
st.subheader('Pertanyaan 2: Faktor Cuaca yang Berpengaruh terhadap Jumlah Penyewaan Sepeda')

# Display correlation between weather variables and bike rentals
weather_corr = df[['temp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(weather_corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Korelasi Antara Variabel Cuaca dan Jumlah Penyewaan Sepeda')
st.pyplot()

### Analisis
st.write("""
dapat dilihat bahwa temperatur (temp) dan jumlah penyewaan sepeda (cnt) menunjukan korelasi yang signifikan 0.63, hal ini berarti jumlah penyewaan sepedah berpengaruh terhadap suhu temperatur pada cuaca
""")

### Visualisasi Boxplot dan Barplot
st.write("""
Berikut adalah boxplot dan barplot yang menunjukkan faktor cuaca yang berpengaruh terhadap jumlah penyewaan sepeda.
""")

# Membandingkan jumlah penyewaan sepeda di kondisi cuaca berbeda
avg_rental_by_weather = df.groupby('weathersit_name')['cnt'].mean()
max_rental_weather = avg_rental_by_weather.idxmax()

# Plotting
st.subheader('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# Bar Plot untuk rata-rata penyewaan sepeda berdasarkan cuaca
axes[0].bar(avg_rental_by_weather.index, avg_rental_by_weather, color=['pink' if weather != max_rental_weather else 'lightcoral' for weather in avg_rental_by_weather.index], linewidth=3)
axes[0].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
axes[0].set_xlabel('Cuaca')
axes[0].set_ylabel('Rata-rata Penyewaan')
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Box Plot untuk perbandingan distribusi jumlah peminjaman sepeda berdasarkan cuaca
sns.boxplot(data=df, x='weathersit_name', y='cnt', ax=axes[1])
axes[1].set_title('Perbandingan Distribusi Jumlah Peminjaman Sepeda')
axes[1].set_xlabel('Cuaca')
axes[1].set_ylabel('Jumlah Peminjaman')

# Histogram untuk distribusi jumlah peminjaman sepeda berdasarkan cuaca
sns.histplot(data=df, x='weathersit_name', y='cnt', bins=10, kde=True, ax=axes[2])
axes[2].set_title('Distribusi Jumlah Peminjaman Sepeda')
axes[2].set_xlabel('Cuaca')
axes[2].set_ylabel('Jumlah Peminjaman')

plt.tight_layout()
st.pyplot(fig)

# Display scatter plot of bike rentals against temperature and weather condition
plt.figure(figsize=(10, 8))
sns.scatterplot(x='temp', y='cnt', data=df, hue='weathersit_name', palette='viridis')
plt.title('Jumlah Penyewaan Sepeda terhadap Temperatur dan Cuaca')
plt.xlabel('Temperatur')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.legend(title='Cuaca')
st.pyplot()

### Analisis
st.write("""
Dari visualisasi di atas, dapat dilihat bahwa faktor cuaca berpengaruh signifikan terhadap jumlah penyewaan sepeda. Penyewaan lebih tinggi saat cuaca cerah dan lebih rendah saat cuaca tidak bersahabat seperti hujan ringan.
""")

# Menampilkan kesimpulan
st.subheader('Conclusion')

# Create two columns layout
col1, col2 = st.columns(2)

with col1:
    # Conclution pertanyaan 1: Bagaimana pola penyewaan sepeda berdasarkan musim?
    st.write("### Conclution pertanyaan 1: Bagaimana pola penyewaan sepeda berdasarkan musim?")
    st.markdown("""
    - Dari analisis dan visualisasi data dapat dilihat bahwa ada pola yang sama berulang penyewaan sepeda dari tahun 2011-2012 berdasarkan musimnya yaitu spring - summer - fall - winter.
    - Berdasarkan grafik line diatas, jumlah penyewaan sepeda di musim semi/spring paling sedikit namun perlahan mulai naik ke musim panas/summer, puncaknya disini stabil sampai musim gugur/fall, lalu saat mendekati musim dingin/salju penyewaan menjadi menurun
    - Dari grafik line juga dapat dilihat peningkatan jumlah penyewaan sepeda dari tahun 2011 sampai 2012, namun tetap pada pola musim yang mirip dengan tahun yang berbeda
    """)

with col2:
    # Conclution pertanyaan 2: Faktor cuaca apa saja yang paling berpengaruh terhadap jumlah penyewaan sepeda?
    st.write("### Conclution pertanyaan 2: Faktor cuaca apa saja yang paling berpengaruh terhadap jumlah penyewaan sepeda?")
    st.markdown("""
    - Dari analisis dan visualisasi data diatas matriks korelasi menunjukan bahwa adanya korelasi yang signifikan antara jumlah penyewaan sepeda dengan suhu/temperatur, ini artinya suhu pada cuaca berpengaruh pada penyewaan sepeda.
    - Dan faktor cuaca yang paling berpengaruh terhadap jumlah penyewaan sepeda adalah hujan ringan, jauh sekali dengan cuaca cerah, dari scatterplot juga dapat dilihat, pada cuaca hujan ringan, jumlah penyewaan sepeda sangat sedikit meskipun hari pada cuaca hujan ringan tersebut sedikit, tapi penyewaannya juga sedikit daripada cuaca yang lain.
    - Pada klasifikasi cuaca tidak sampai pada hujan lebat, mungkin karena dari datasetnya, jadi didalam dataframe tidak ada cuaca yang lebih ekstreme selain hujan ringan.
    """)
