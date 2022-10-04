import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv', #completed
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(): #completed
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while True:
        city = input('Which city would you like data for? ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Invalid city. Please try again.')
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month_or_day = input('Would you like to filter by month, day, or all? ').lower()
        if month_or_day in ['month', 'day', 'all']:
            break
        else:
            print('Invalid choice. Please try again.')
            
    if month_or_day == 'month':
        while True:
            day = 'all'
            month = input('Which month would you like data for? (All, January, February, ..., June): ').lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Invalid month. Please try again.')
    # get user input for day of week (all, monday, tuesday, ... sunday
    elif month_or_day == 'day':
        while True:
            month = 'all'
            day = input('Which day do you want information for(enter 3 letters)? (ALL, MON, TUE, WED, THU, FRI, SAT, SUN): ').lower()
            day = day[:3]
            if day in ['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                break
            else:
                print('Invalid input. Please try again.')
    else:
        month = 'all'
        day = 'all'
        
    print('-'*40)
    return city, month, day

def load_data(city, month, day): #completed
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Day of Week'] = df['Start Time'].dt.day_of_week
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month
    df['Trip'] = df['Start Station'] + ',' + df['End Station']
    
    if month != 'all':
        month_nums = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        month = month_nums[month]
        df = df.loc[df['Month'] == month]
    if day != 'all':
        day_nums = {'sun': 6, 'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5}
        day = day_nums[day]
        df = df.loc[df['Day of Week'] == day]
    
    return df

def time_stats(df): #completed
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_nums = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    common_month = month_nums.get(df['Month'].mode()[0])
    print('The most common month was: {}'.format(common_month))

    # display the most common day of week
    day_nums = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    common_day = day_nums.get(df['Day of Week'].mode()[0])
    print('The most common day of the week was: {}'.format(common_day))


    # display the most common start hour
    print('The most common start hour was: {}'.format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df): #completed
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common starting station was:\n  {}\n'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common ending station was:\n  {}\n'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    common_trip = df['Trip'].mode()[0]
    common_start = common_trip.split(',')[0]
    common_end = common_trip.split(',')[1]
    print('The most common trip was:\n  Starting at {}\n  Ending at {}'.format(common_start, common_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df): #completed
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_days = df['Trip Duration'].sum() // 86400
    total_hours = (df['Trip Duration'].sum() % 86400) // 3600
    total_minutes = ((df['Trip Duration'].sum() % 86400) % 3600) // 60 
    total_seconds = ((df['Trip Duration'].sum() % 86400) % 3600) % 60
    print('The total travel time was:\n  {} days\n  {} hours\n  {} minutes and\n  {} seconds\n'.format(total_days, total_hours, total_minutes, total_seconds))

    # display mean travel time
    average_minutes = df['Trip Duration'].mean() // 60
    average_seconds = df['Trip Duration'].mean() % 60
    print('The average travel time was:\n  {} minutes and\n  {} seconds'.format(average_minutes, average_seconds))
    
    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)

def user_stats(df): #completed
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    num_customer = df['User Type'].value_counts().loc['Customer']
    num_subscriber = df['User Type'].value_counts().loc['Subscriber']
    print('User type data:\n  {} Subscribers\n  {} Customers\n'.format(num_subscriber, num_customer))
    
    try:
        # Display counts of gender
        num_male = df['Gender'].value_counts().loc['Male']
        num_female = df['Gender'].value_counts().loc['Female']
        num_unspecified = len(df) - num_male - num_female
        print('Gender data:\n  {} male users,\n  {} female users, and\n  {} unspecified users.\n'.format(num_male, num_female, num_unspecified))

        # Display earliest, most recent, and most common year of birth
        first_year = int(df['Birth Year'].min())
        last_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        specified_year = int(df['Birth Year'].value_counts().sum())
        unspecified_year = int(len(df['Birth Year'])-df['Birth Year'].value_counts().sum())
        print('Birth year data:\n  Earliest birth year: {}\n  Most recent birth year: {}\n  Most common birth year: {}\n\n  Users providing a birth year: {}\n  Users not providing a birth year: {}'
            .format(first_year, last_year, common_year, specified_year, unspecified_year))
    except KeyError:
        print('Gender and Birth Year are not available for Washington.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main(): #completed
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        want_raw = input('\nDo you want to view 5 lines of raw data? (yes or no): ').lower()
        line_counter = 0
        while want_raw == 'yes':
            print(df.iloc[line_counter:(line_counter + 5)])
            line_counter += 5
            want_raw = input('\nDo you want to view 5 more lines of raw data? (yes or no): ').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__": #completed
	main()