import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to filter by? (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter a valid city name.")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month would you like to filter by? (all, January, February, ... , June): ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month name.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day would you like to filter by? (all, Monday, Tuesday, ... Sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day name.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is: {most_common_month}")

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print(f"The most common day of week is: {most_common_day_of_week}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {most_common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start station and end station trip is: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of user types:\n{user_types}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nCounts of gender:\n{gender_counts}")
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request by the user."""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
    start_loc = 0
    while view_data.lower() == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input('Do you wish to continue? Enter yes or no.\n')
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)  # Call the function to display raw data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()