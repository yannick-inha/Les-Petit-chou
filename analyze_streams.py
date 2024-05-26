import pandas as pd

def analyze_csv(file_path):
    # Load the CSV file with tab separator
    data = pd.read_csv(file_path, sep='\t', header=None)

    # Assign column names for better understanding
    data.columns = ['ID', 'Language', 'Game', 'Timestamp', 'Type', 'Channel_ID', 'Views', 'Video_ID', 'Status']

    # Basic information about the dataset
    print("Basic Information:")
    print(data.info())

    # Descriptive statistics
    print("\nDescriptive Statistics:")
    print(data.describe())

    # Count of unique games
    unique_games_count = data['Game'].nunique()
    print(f'\nNumber of unique games: {unique_games_count}')

    # Count of streams per game
    streams_per_game = data['Game'].value_counts().head(10)  # Top 10 games by number of streams
    print("\nTop 10 games by number of streams:")
    print(streams_per_game)

    # Fill missing values in the 'Game' column with an empty string
    data['Game'].fillna('', inplace=True)

    # Filter out rows with numerical game names
    filtered_data = data[~data['Game'].str.isdigit()]

    # Average views per game
    average_views_per_game = filtered_data.groupby('Game')['Views'].mean().sort_values(ascending=False).head(10)  # Top 10 games by average views
    print("\nTop 10 games by average views:")
    print(average_views_per_game)

    # Distribution of 'live' and 'vodcast'
    type_distribution = data['Type'].value_counts()
    print("\nDistribution of 'live' and 'vodcast':")
    print(type_distribution)

    # Check for streams with unusually high view counts
    high_view_streams = data[data['Views'] > 10000]
    print("\nStreams with unusually high view counts:")
    print(high_view_streams)

# Path to your CSV file
file_path = '2017-10-05-17-30.csv'

# Run the analysis
analyze_csv(file_path)
