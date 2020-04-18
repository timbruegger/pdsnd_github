import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'boston': 'boston.csv'
            }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Hallo! Lass uns Daten von amerikanischen Bikesharing-Diensten erkunden.')
    #get user input for city (chicago, new york city, washington)
    while True:
        city = str(input("Which city would you like to view? Please select between Chicago, New York City, Washington:\n")).lower()
        if city in CITY_DATA:
            print("Great! You have selected {}".format(city.title()))
            break
        else:
            print("Sorry, your city cannot be found. Please make sure that it was correctly spelled.")
            continue
    
    #get user input for month and day 
    while True:
        user_filter = input("Would you like to filter the data by month, day, or not at all? Please enter 'month', 'day' or 'not'\n").lower()
        if user_filter == 'month':
            day = 'all'
            while True:
                month = str(input("Please enter the name of the month that you want to view (between January and June):\n")).lower()
                if month in months:
                    print("Great! You have selected {}".format(month.title()))
                    break
                else:
                    print("Sorry, this is not a valid input for 'month'. Please make sure that you indicate the name of the month")
                    continue
            break
        elif user_filter == 'day':
            month = 'all'
            while True:
                day = str(input("Please enter the name of the day that you want to view:\n")).lower()
                if day in days:           
                    print("Great! You have selected {}".format(day.title()))
                    break
                else:
                    print("Sorry, this is not a valid input for 'day'. Please make sure that you indicate the name of the day.")
                    continue
            break
        else:
            if user_filter != 'not':
                print('The filter term was not matching to day, month or not. Therefore no filter has been applied on day and month')
            month = 'all'
            day = 'all'
            break

    print('The data is filtered to city: {}, month: {} and day: {}.'.format(city.title(), month.title(), day.title()))        
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(months[most_common_month-1].title()))
    
    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(days[most_common_day].title()))
    
    #display the most common start hour
    print('The most common start hour is: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print('The most commonly used start station is: \n{}'.format(df['Start Station'].mode()[0]))

    #display most commonly used end station
    print('The most commonly used end station is: \n{}'.format(df['End Station'].mode()[0]))
    
    #display most frequent combination of start station and end station trip
    print('The most frequent trip is: \n{}'.format((df['Start Station'] + ' to ' + df['End Station']).mode()[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print('The total travel time is: {} (hours/minutes/seconds).'.format(pd.to_timedelta(df['Trip Duration'].sum(), unit = 's')))

    #display mean travel time
    print('The mean travel time is: {} (hours/minutes/seconds).'.format(pd.to_timedelta(df['Trip Duration'].mean(), unit = 's')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('Here are the counts of user types:\n', df['User Type'].value_counts())

    #The following information are not available for Washington
    if city == 'washington':
        print('\nFor Washington, there is no gender or date of birth data available.\n')
    else:
        #Display counts of gender
        print('\nHere are the counts of gender:\n', df['Gender'].value_counts())

        #Display earliest, most recent, and most common year of birth
        print('\nThe oldest user was born in: {}'.format(int(df['Birth Year'].min())))
        print('The youngest user was born in: {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data in blocks of 5 rows."""

    i=0
    user_input='yes'
    while user_input == 'yes':
        try:
            print('Here are five rows of raw data\n', df.iloc[i:i+5])
            user_input = input('\nWould you like to see five more rows of data? Enter yes or no.\n').lower()
            i += 5
        except Exception as e:
            print('There was a problem showing your data: ', e)
            break

def main():
    while True:
        city, month, day = get_filters()
        #print(city, month, day)
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
