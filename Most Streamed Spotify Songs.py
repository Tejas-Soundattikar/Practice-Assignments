import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:\\Users\\DELL\\Downloads\\Most Streamed Spotify Songs 2024.csv"

try:
    songs = pd.read_csv(path, encoding='latin1')
except UnicodeDecodeError:
    songs = pd.read_csv(path, encoding='iso-8859-1')

print(songs.head())

print(songs.shape)

print(songs.dtypes)

print(songs.nunique())

print(songs.isnull().sum())

print(songs.describe())

print(songs['Pandora Track Stations'])


### Univariate Analysis - outliers detection in numerical features

num_cols = ['Track Score', 'Spotify Popularity', 'Apple Music Playlist Count', 'Deezer Playlist Count', 'Amazon Playlist Count']

for i in num_cols:
    sns.boxplot(data = songs[i])
    plt.title(f"Outliers for {i}")
    plt.show()


## Top 10 most played tracks on Spotify

top_10_spotify = songs[['Track', 'Spotify Streams']].sort_values('Spotify Streams',ascending=False)

top_10_spotify = top_10_spotify.head(10)
print(top_10_spotify)


sns.barplot(top_10_spotify, x = 'Track', y = 'Spotify Streams')
plt.show()