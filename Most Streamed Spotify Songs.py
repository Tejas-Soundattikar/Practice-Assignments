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
print(songs['Spotify Popularity'])



### Converting the Release Date columns into Datetime object.
songs['Release Date'] = pd.to_datetime(songs['Release Date'])
songs['Release Month'] = songs['Release Date'].dt.month
songs['Release Year'] = songs['Release Date'].dt.year

### Univariate Analysis - outliers detection in numerical features

num_cols = ['Track Score', 'Spotify Popularity', 'Apple Music Playlist Count', 'Deezer Playlist Count', 'Amazon Playlist Count']
for i in num_cols:
    sns.boxplot(data = songs[i])
    plt.title(f"Outliers for {i}")
    plt.show()


## Dividing the Columns by 1000.

cols_to_convert = ['Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach', 'YouTube Views', 'YouTube Likes', 'TikTok Posts', 'TikTok Likes', 'TikTok Views',
                   'YouTube Playlist Reach','Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins','Deezer Playlist Reach','Deezer Playlist Count','Amazon Playlist Count', 
                   'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams', 'Shazam Counts']


for col in cols_to_convert:
    songs[col] = songs[col].apply(lambda x: str(x).replace(",",""))
    songs[col] = songs[col].astype(float) / 1000
    
    
## Checking for the duplicate tracks and dopping them

print(songs['Track'].duplicated().sum())
songs.drop_duplicates(subset=['Track'], inplace=True)

print(songs['Track'].duplicated().sum())

## Checking the Distribution
    ## Release Date Distribution
sns.histplot(songs['Release Date'], kde=True, bins = 10)
plt.title("Distribution of Songs by Release Date")
plt.xlabel("Release Date")
plt.ylabel("Number of Songs")
plt.show()

    ## Release Month Distribution
month_distr = songs.groupby('Release Month')['Track'].count().reset_index()
print(month_distr)
sns.barplot(x = month_distr['Release Month'], y = month_distr['Track'], palette= 'coolwarm')
plt.title("Distribution of Songs by Release Month")
plt.xlabel("Release Month")
plt.ylabel("Number of Songs")
plt.show()

    ## Artist Distribution - Top 20 Artists
top_artist = songs['Artist'].value_counts().head(20)
sns.barplot(x=top_artist.values, y = top_artist.index, palette='vlag')
plt.title("Top 20 Artists by Number of Songs")
plt.xlabel("Number of Songs")
plt.ylabel("Artist")
plt.show()



## Top 10 tracks on Different Platforms 
    ## Top 10 Tracks by Popularity on Spotify
top_10_popular_spotify = songs.sort_values('Spotify Popularity', ascending=False)
sns.barplot(top_10_popular_spotify.head(10), x= 'Track', y='Spotify Popularity', palette='rainbow')
plt.title("Top 10 Tracks By Spotify Popularity")
plt.xticks(rotation=60)
plt.show()

for col in cols_to_convert:
    songs.sort_values(col, ascending=False, inplace=True)
    top_10 = songs[['Track',col]].reset_index()
    #print(f"Top 10 Tracks - {col}",top_10['Track'].head(10))

    plt.figure(figsize=(12,8))
    sns.barplot(top_10.head(10), x = 'Track', y = col, palette= 'rainbow')
    plt.xticks(rotation = 60)
    plt.title(f"Top 10 Tracks - {col}")
    plt.show()


## Analyzing How the Popularity of Songs Changes Over Time
