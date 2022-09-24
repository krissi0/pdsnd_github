# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 17:25:58 2022

@author: AAK1SI
"""

import pandas as pd
import numpy as np
import datetime as dt
import calendar
import time

CITY_DATA = { 'chicago': r"U:\Udacity\chicago.csv",
              'new york city': r"U:\Udacity\new_york_city.csv",
              'washington': r"U:\Udacity\washington.csv" }





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
    
    city_list = ['chicago', 'washington', 'new york city']

    
    city = None

    
    while city is None:
        user_input = input('please choose a city (chicago, washington, new york city): ').lower()
        if user_input in city_list:
            city = user_input
        else:
            print('your city is not valid. please try again and choose between chicago, washington or new york city.')
    

        


    print('-'*40)
    return city

def load_data(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data

    df = pd.read_csv(CITY_DATA[city])
    
    #convert data to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    
    #create month and day of week column
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    
    
    month_list = df['Month'].unique().tolist()
    month_list.append('all')
    
    
    day_list = list(calendar.day_name)
    day_list.append('all')
    
    global month
    global day
    city = None
    month = None
    day = None
    

    while month is None:
        user_input = input('please choose a month (all, January, February, March, April, May, June): ')
        if user_input in month_list:
            month = user_input
        else:
            print('your month is not valid. please try again.')
        
        
    while day is None:
        user_input = input('please choose a day of the week (all, Monday, Tuesday, Wednesday,...): ')
        if user_input in day_list:
            day = user_input
        else:
            print('your weekday is not valid. please try again.')
            
    #filter dataframe
    
    if month != 'all':
        
        df = df.loc[df['Month'] == month]
        
    
    if day != 'all':
        df = df.loc[df['Day_of_Week'] == day]
    
    return df
    

# =============================================================================



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':
    # display the most common month
        common_month = df['Month'].value_counts().idxmax()
        common_month_value = df['Month'].value_counts().max()
        print(f"The most common month is {common_month} with a usage of {common_month_value} times.")

    if day == 'all':
    # display the most common day of week
        common_weekday = df['Day_of_Week'].value_counts().idxmax()
        common_weekday_value = df['Day_of_Week'].value_counts().max()
        print(f"The most common Weekday is {common_weekday} with a usage of {common_weekday_value} times.")


    # display the most common day of week
    common_hour = df['Hour'].value_counts().idxmax()
    common_hour_value = df['Hour'].value_counts().max()
    print(f"The most common Hour is {common_hour} o'clock with a usage of {common_hour_value} times.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].value_counts().idxmax()
    common_start_station_value = df['Start Station'].value_counts().max()
    print(f"The most common Start Station is {common_start_station} with a usage of {common_start_station_value} times.")

    # display most commonly used end station


    common_end_station = df['End Station'].value_counts().idxmax()
    common_end_station_value = df['End Station'].value_counts().max()
    print(f"The most common End Station is {common_end_station} with a usage of {common_end_station_value} times.")

    # display most frequent combination of start station and end station trip

    temp_df = df.groupby(["Start Station", "End Station"]).size().reset_index(name="Frequency")
    most_freq = temp_df.loc[temp_df['Frequency'].idxmax()]
    
    print(f"The most common Station Combination is from {most_freq.get('Start Station')} to {most_freq.get('End Station')} with a frequency of {most_freq.get('Frequency')} times.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    sum_travel_time = df['Travel Time'].sum()

    total_days=  sum_travel_time.days
    total_hours = sum_travel_time.seconds//3600
    total_minutes = (sum_travel_time.seconds//60)%60
    
    print(f"The total travel time is {total_days} days, {total_hours} hours and {total_minutes} minutes({sum_travel_time}).")

    # display mean travel time
    
    mean_travel_time = df['Travel Time'].mean()
    
    mean_days=  mean_travel_time.days
    mean_hours = mean_travel_time.seconds//3600
    mean_minutes = (mean_travel_time.seconds//60)%60
    
    print(f"The mean travel time is {mean_days} days, {mean_hours} hours and {mean_minutes} minutes ({mean_travel_time}).")
    print("How was your trip? Post it on our instagram page")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    
    cities_with_gender_birth_year = ['chicago', 'new york city']

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("This is the count of different user types.")
    print(df["User Type"].value_counts())

    
    if city in cities_with_gender_birth_year:
        # Display counts of gender
        df["Gender"] = df["Gender"].replace(np.nan, "not known")
        print("This is the count of genders.")
        print(df["Gender"].value_counts())
        
            # Display earliest, most recent, and most common year of birth
        
        earliest = df["Birth Year"].min()
        print(f"This is the earliest Birth Year: {earliest} ")
        recent_date = df["End Time"].max()
        
        df["Birth Year"] = df["Birth Year"].replace(np.nan, "not known")
        most_recent = df["Birth Year"].loc[df["End Time"] == recent_date].reset_index(drop=True)[0]
        print(f"This is the most recent Birth Year: {most_recent} ")
        
        most_common_birth_year = df['Birth Year'].value_counts()
        most_common_birth_year.drop(index='not known', inplace=True)
        
        most_common_birth_year_value = most_common_birth_year.idxmax()
        print(f"This is the most common Birth Year: {most_common_birth_year_value}")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_raw_data(df):
    
    view_data = input('\nDo you want to see the first 5 rows of raw data? Enter yes or no.\n').lower()

    start_loc = 0
    
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5].to_string())
        start_loc += 5
        
        view_data = input('\nDo you want to see the next 5 rows of data? Enter yes or no.\n').lower()
        
    

def main():
    while True:
        city = get_filters()
        df = load_data(city)

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


