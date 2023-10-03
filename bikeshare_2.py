import time
import pandas as pd
import numpy as np
import _datetime as dt

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
    city=input("Enter a city name (from this list: chicago, new york city, washington) to see some stats on usage: ").lower()

    # get user input for month (all, january, february, ... , june)
    month=input("For which month would you like to see results, enter ther name of the month between january and june or enter all to see all months: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("For which day of the week would you like to see results, enter, enter a day from this list (all, monday, tuesday, ... ,sunday): ").lower()


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
    if city=='washington':
        df['Gender']="Unknown"
        df['Birth Year']="Unknown"

    df.fillna(0,inplace=True)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday 
    
    # filter by month if applicable
    if month != 'all':
        
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        
    # filter by day of week if applicable
    if day != 'all':
        
        # use the index of the days list to get the corresponding int
        week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        weekday = week_days.index(day.lower())
    
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==weekday]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])                                

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
       
    month_dict= {1: 'january',2:'february',3:'march',4:'april',5:'may',6:'june'}
    print("Most popular month: ",month_dict[popular_month])

    # display the most common day of week
    df['weekday'] = df['Start Time'].dt.weekday
    weekday_dict= {0:'monday', 1: 'tuesday',2:'wednesday',3:'thursday',4:'friday',5:'sunday',6:'sunday'}
    
    popular_weekday = df['weekday'].mode()[0]
    print("Most popular day of the week: ", weekday_dict[popular_weekday])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print("Most popular hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]
    print("Most popular start station: ",popular_start_station)

    # display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]
    print("Most popular end station: ",popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_combo']=df['Start Station']+" - "+df['End Station']
    popular_start_end_combo=df['start_end_combo'].mode()[0]
    print("Most Frequent combination of start station and end station: ",popular_start_end_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time in years:", round(df['Trip Duration'].sum()/60/60/24/365.25,2))

    # display mean travel time
    print("Average travel time in minutes:", round(df['Trip Duration'].mean()/60,2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Frequency of user type:",df['User Type'].value_counts())

    # Display counts of gender
    print("Frequency of user type:",df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print("earliest year of birth: {}, most recent year of birth: {}, and most common year of birth:{}".format(df['Birth Year'].min(),df['Birth Year'].max(),df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        try:
            city, month, day = get_filters()

            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            
            raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
            if raw_data.lower() == 'yes':

                row=0
                while row<=len(df):
                    print(df.loc[row:row+4,:])
                    row+=5    

                    raw_data = input('\nWould you like to see another 5 rows of data? Enter yes or no.\n')
                    if raw_data.lower() != 'yes':   
                        break 

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except:
            print("one of your inputs are incorrect, please try again")
            


if __name__ == "__main__":
	main()
