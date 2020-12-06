    import time
    import pandas as pd
    import numpy as np
    import calendar

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
        city_input = ['chicago',"new york city",'washington']
        while True:
            city = input('Would you like to explore data for, select City from {}? - '.format(', '.join(city_input).title())).lower()
            if city in city_input:
                break

        while True:
            month, day = None, None
            filter_input = input('Would you like to filter the data by month, day, or both. Type "none" for no time filter? - ').lower()
            if filter_input == 'none':
                month, day = 'all', 'all'
                break
            if filter_input == 'month' or filter_input == 'both':
                month_input = ['january','february','march','april','may','june']
                while True:
                    month = input('Which Month? {}? - '.format(', '.join(month_input).title())).lower()
                    if month in month_input:
                        break
                if filter_input == 'month':
                    day = 'all'
                    break
            if filter_input == 'day' or filter_input == 'both':
                day_input = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
                while True:
                    day = input('Which Day? {}? - '.format(', '.join(day_input).title())).lower()
                    if day in day_input:
                        break
                if filter_input == 'day':
                    month = 'all'
                    break
            if filter_input == 'both' and month != 'all' and day != 'all':
                break


        print('-'*40)
        print('Selected filters: City - {}, Month - {}, Day - {}'.format(city, month, day).title())
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
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])

        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name


        # filter by month if applicable
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month)+1
            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

        return df


    def time_stats(df):
        """Displays statistics on the most frequent times of travel."""

        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
        freq_month = calendar.month_name[df['month'].mode()[0]]
        freq_day = df['day_of_week'].mode()[0]
        freq_hour = df['Start Time'].dt.hour.mode()[0]

        #Calender Refernce https://docs.python.org/3/library/calendar.html    
        print('The Most Frequent: \n\tMonth - {} \n\tDay of week - {} \n\tStart hour - {}'.format(freq_month, freq_day, freq_hour))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


    def station_stats(df):
        """Displays statistics on the most popular stations and trip."""

        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        s_station = df['Start Station'].mode()[0]
        s_station_count = df['Start Station'].value_counts()[0]
        e_station = df['End Station'].mode()[0]
        e_station_count = df['End Station'].value_counts()[0]

        print('The Most Popular Stations: \n\tStart Station - {} with Count {} \n\tEnd Station - {} with Count {}'.format(s_station, s_station_count,e_station,e_station_count))

        df['trip'] = df['Start Station'].str.cat(df['End Station'],sep="<-->")
        trip = df['trip'].mode()[0]
        trip_start = trip.split('<-->')[0]
        trip_end = trip.split('<-->')[1]
        trip_count = df['trip'].value_counts()[0]
        print('\nThe Most Popular trip with Count - {} : \n\tStart at - {} \n\tEnd at - {}'.format(trip_count,trip_start,trip_end))


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


    def trip_duration_stats(df, city, month, day):
        """Displays statistics on the total and average trip duration."""

        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        print('Trip details of City "{}" in "{}" month, on "{}" (day):'.format(city, month, day).title())
        print('\tTotal Travel time - {} \n\tAvarage time - {}'.format(df['Trip Duration'].sum(skipna = True), df['Trip Duration'].mean()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


    def user_stats(df):
        """Displays statistics on bikeshare users."""

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        print('User breakdown based on User Type:\n{}'.format(df['User Type'].value_counts()))

        if 'Gender' in df.columns:
            print('\nUser breakdown based on Gender:\n{}'.format(df['Gender'].value_counts()))
        else:
            print('\nUser Gender data unavailable')

        if 'Birth Year' in df.columns:
            earlist = int(df['Birth Year'].min())
            recent = int(df['Birth Year'].max())
            common = int(df['Birth Year'].mode()[0])
            print('\nUser birth year Stats: \n\tEarlist - {} \n\tMost recent - {} \n\tMost common - {}'.format(earlist,recent,common))
        else:
            print('\nUser birth year data unavailable')


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def print_dataframe(df):
        #to_json Refernce https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
        df = df.drop(['month','day_of_week','trip'], axis = 1)
        for i in range(0,len(df), 5):
            for j in range(5,len(df), 5):
                raw = input('\nWould you like to see the raw trip data? Enter yes or no.\n').lower()
                while raw == 'yes':
                    print(df[i:j].to_json(orient="records", lines=True))
                    i += 5
                    j += 5
                    break
                if raw =='no':
                    break
            else:
                continue
            break



    def main():
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df, city, month, day)
            user_stats(df)
            print_dataframe(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

    if __name__ == "__main__":
        main()