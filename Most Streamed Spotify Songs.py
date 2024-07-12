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


## Converinng the values in Columns in millions.

cols_to_convert = ['Spotify Streams', 'Spotify Playlist Reach', 'YouTube Views', 'YouTube Likes', 'TikTok Likes', 'TikTok Views',
                   'Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins','Deezer Playlist Reach','Deezer Playlist Count','Amazon Playlist Count', 
                   'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams', 'Shazam Counts']


for col in cols_to_convert:
    songs[col] = songs[col].apply(lambda x: str(x).replace(",",""))
    songs[col] = round(songs[col].astype('Float64') / 1000000,2)
    

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
    print(f"Top 10 Tracks - {col}",top_10['Track'].head(10))

    plt.figure(figsize=(12,8))
    sns.barplot(top_10.head(10), x = 'Track', y = col, palette= 'rainbow')
    plt.xticks(rotation = 60)
    plt.title(f"Top 10 Tracks - {col}")
    plt.show()


## Platform Comparison

songs['All Time Rank'] = songs['All Time Rank'].apply(lambda x: str(x).replace(",", ""))
songs['All Time Rank'] = songs['All Time Rank'].astype("int")
songs.sort_values('All Time Rank',ascending= True ,inplace = True)
cols = ['Track','Spotify Streams', 'YouTube Views', 'TikTok Views']
top_10 = songs[cols].head(10)
top_10['YouTube Views'].fillna(0, inplace=True)
top_10['TikTok Views'].fillna(0, inplace=True)

top_10_melted =top_10[cols].melt(id_vars=['Track'], value_vars=['Spotify Streams', 'YouTube Views', 'TikTok Views'], var_name= 'Platform', value_name='Streams')

sns.barplot(data=top_10_melted, x='Track', y ='Streams', hue='Platform')
plt.title('Comparison of Song Popularity Across Platforms')
plt.xlabel("Track Name")
plt.ylabel("Streams")
plt.xticks(rotation = 45)
plt.legend(title='Platforms')
plt.show()

plt.barh(top_10['Track'], top_10['Spotify Streams'], label = 'Spotify Streams', color = 'b')
plt.barh(top_10['Track'], top_10['YouTube Views'], left=top_10['Spotify Streams'], label = 'YouTube Views', color = 'r')
plt.barh(top_10['Track'], top_10['TikTok Views'], left=top_10['Spotify Streams'] + top_10['YouTube Views'], label = 'TikTok Views', color = 'g')

plt.xlabel('Track Name')
plt.ylabel("Popularity")
plt.legend()
plt.show()


### Top 10 Artist and Albums on Spotify, YouTube and TikTok
cols = songs[['Spotify Streams', 'YouTube Views', 'TikTok Views']]

for col in cols:
    top_10 = songs.groupby('Artist')[col].sum().sort_values(ascending=False).reset_index()
    top_10_artist = top_10.nlargest(10, col)
    
    plt.figure(figsize=(12,8))
    sns.barplot(data=top_10_artist, x = 'Artist', y=col, palette= 'viridis')
    plt.xlabel("Artist")
    plt.ylabel("Streams")
    plt.title(f"Top 10 Artist by {col}")
    plt.xticks(rotation = 45)
    plt.show()
    

for col in cols:
    top_albums = songs.groupby(['Artist', 'Album Name'])[col].sum().sort_values(ascending=False).reset_index()
    top_10_albums = top_albums.nlargest(10, col)
    
    plt.figure(figsize=(14,10))
    sns.barplot(data=top_10_albums, x= 'Album Name', y= col, palette='Spectral')
    plt.xlabel("Album Name")
    plt.ylabel("Streams")
    plt.title(f"Top 10 Albums by {col}")
    plt.xticks(rotation = 45)
    plt.show()


## Playlist Analysis
playlist_columns = ['Track', 'Spotify Playlist Count', 'YouTube Playlist Reach', 'Spotify Streams', 'YouTube Views', 'TikTok Views']

for col in playlist_columns:
    songs[col] = pd.to_numeric(songs[col], errors='coerce')

# Drop rows with NaN values
df_cleaned_tiktok = songs.dropna(subset=playlist_columns)
# Correlation analysis between playlist inclusion and song popularity
playlist_popularity_corr = songs[playlist_columns].corr()

# Display correlation matrix
print("Correlation Matrix:")
print(playlist_popularity_corr)

# Plot heatmap of the correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(playlist_popularity_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Between Playlist Inclusion and Song Popularity')
plt.show()

# Scatter plot to visualize the relationship between playlist counts and streams/views
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
sns.scatterplot(data=songs, x='Spotify Playlist Count', y='Spotify Streams')
plt.title('Spotify Playlist Count vs Spotify Streams')
plt.xlabel('Spotify Playlist Count')
plt.ylabel('Spotify Streams')

plt.subplot(1, 2, 2)
sns.scatterplot(data=songs, x='YouTube Playlist Reach', y='YouTube Views')
plt.title('YouTube Playlist Reach vs YouTube Views')
plt.xlabel('YouTube Playlist Reach')
plt.ylabel('YouTube Views')

plt.tight_layout()
plt.show()



### Analysing the Influence of TikTok Posts on Song Popularity
tiktok_columns = ['TikTok Posts', 'TikTok Likes', 'TikTok Views', 'Spotify Streams', 'YouTube Views']

# Convert columns to numeric, forcing errors to NaN
for col in tiktok_columns:
    songs[col] = pd.to_numeric(songs[col], errors='coerce')

# Drop rows with NaN values
df_cleaned_tiktok = songs.dropna(subset=tiktok_columns)

# Correlation analysis between TikTok metrics and song popularity
tiktok_popularity_corr = df_cleaned_tiktok[tiktok_columns].corr()

# Display correlation matrix
print("Correlation Matrix for TikTok Metrics:")
print(tiktok_popularity_corr)

# Plot heatmap of the correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(tiktok_popularity_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Between TikTok Metrics and Song Popularity')
plt.show()

# Scatter plots to visualize the relationship between TikTok metrics and song popularity
plt.figure(figsize=(14, 7))

plt.subplot(1, 3, 1)
sns.scatterplot(data=df_cleaned_tiktok, x='TikTok Posts', y='Spotify Streams')
plt.title('TikTok Posts vs Spotify Streams')
plt.xlabel('TikTok Posts')
plt.ylabel('Spotify Streams')

plt.subplot(1, 3, 2)
sns.scatterplot(data=df_cleaned_tiktok, x='TikTok Likes', y='Spotify Streams')
plt.title('TikTok Likes vs Spotify Streams')
plt.xlabel('TikTok Likes')
plt.ylabel('Spotify Streams')

plt.subplot(1, 3, 3)
sns.scatterplot(data=df_cleaned_tiktok, x='TikTok Views', y='Spotify Streams')
plt.title('TikTok Views vs Spotify Streams')
plt.xlabel('TikTok Views')
plt.ylabel('Spotify Streams')

plt.tight_layout()
plt.show()


### Analysing the Impact of Radio Play on Streaming Statistics

radio_columns = ['AirPlay Spins', 'SiriusXM Spins', 'Spotify Streams', 'YouTube Views']

# Convert columns to numeric, forcing errors to NaN
for col in radio_columns:
    songs[col] = pd.to_numeric(songs[col], errors='coerce')

# Drop rows with NaN values
df_cleaned_radio = songs.dropna(subset=radio_columns)

# Correlation analysis between radio play metrics and streaming statistics
radio_popularity_corr = df_cleaned_radio[radio_columns].corr()

# Display correlation matrix
print("Correlation Matrix for Radio Play Metrics:")
print(radio_popularity_corr)

# Plot heatmap of the correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(radio_popularity_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Between Radio Play Metrics and Streaming Statistics')
plt.show()

# Scatter plots to visualize the relationship between radio play metrics and streaming statistics
plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
sns.scatterplot(data=df_cleaned_radio, x='AirPlay Spins', y='Spotify Streams')
plt.title('AirPlay Spins vs Spotify Streams')
plt.xlabel('AirPlay Spins')
plt.ylabel('Spotify Streams')

plt.subplot(1, 2, 2)
sns.scatterplot(data=df_cleaned_radio, x='SiriusXM Spins', y='Spotify Streams')
plt.title('SiriusXM Spins vs Spotify Streams')
plt.xlabel('SiriusXM Spins')
plt.ylabel('Spotify Streams')

plt.tight_layout()
plt.show()
