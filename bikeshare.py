import time
import pandas as pd
import numpy as np

# City data file paths
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - Name of the city to analyze
        (str) month - Name of the month to filter by, or 'all' to apply no month filter
        (str) day - Name of the day of the week to filter by, or 'all' to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get the city choice from the user
    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington? ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("\nInvalid answer. Please choose from Chicago, New York City, or Washington.")

    # Get the filter choice (month, day, both, or none)
    while True:
        choice = input("\nWould you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter: ").strip().lower()
        if choice in ['month', 'day', 'both', 'none']:
            break
        else:
            print("\nInvalid answer. Please choose from 'month', 'day', 'both', or 'none'.")

    month = 'all'
    day = 'all'

    # If the user wants to filter by month, prompt for a specific month
    if choice == 'month' or choice == 'both':
        while True:
            month = input("\nWhich month? January, February, March, April, May, June, or 'all' for no filter: ").strip().lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                print("\nInvalid month. Please choose from January, February, March, April, May, June, or 'all'.")

    # If the user wants to filter by day, prompt for a specific day
    if choice == 'day' or choice == 'both':
        while True:
            day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all' for no filter: ").strip().lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                break
            else:
                print("\nInvalid day. Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - Name of the city to analyze
        (str) month - Name of the month to filter by, or 'all' for no filter
        (str) day - Name of the day to filter by, or 'all' for no filter

    Returns:
        pd.DataFrame - DataFrame containing the filtered city data
    """
    # Load the dataset for the city
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day from 'Start Time'
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if specified
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day if specified
    if day != 'all':
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month.title())

    # Most popular day of the week
    popular_day = df['day'].mode()[0]
    print('Most Popular Day:', popular_day.title())

    # Most popular start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # Most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # Most frequent combination of start and end station trip
    most_frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent Trip Combination (Start -> End):', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Count of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Gender stats (if available)
    if 'Gender' in df.columns:
        gender_stats = df['Gender'].value_counts()
        print('Gender Stats:\n', gender_stats)
    else:
        print("No Gender data available for this city.")

    # Birth year stats (if available)
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print(f'Earliest Birth Year: {earliest_birth}')
        print(f'Most Recent Birth Year: {most_recent_birth}')
        print(f'Most Common Birth Year: {common_birth}')
    else:
        print("No Birth Year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays raw trip data upon user's request."""
    index = 0
    show_data = input("\nWould you like to view individual trip data? Type 'yes' or 'no': ").strip().lower()

    # Display raw data in chunks of 5 rows
    while show_data == 'yes':
        if index + 5 > len(df):
            print("\nNo more data to display.")
            break
        for i in range(index, index + 5):
            row_data = df.iloc[i].to_dict()
            print(row_data)
        index += 5
        show_data = input("\nWould you like to view more trip data? Type 'yes' or 'no': ").strip().lower()


def main():
    """Main function to run the program."""
    while True:
        # Get the user's filters for city, month, and day
        city, month, day = get_filters()

        # Load data for the specified city, month, and day
        df = load_data(city, month, day)

        # Display various statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        # Ask if the user wants to restart the program
        restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
