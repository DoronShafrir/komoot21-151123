''' ver 1.3 8/12/22
change the date funding way to the beginning of the dataframe
'''
import pandas as pd
import sys
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
from datetime import timedelta


class k_in_DF():
    def __init__(self):
        pass


#-----------This function returns the date of tour
    def find_name(self, tour):
        date_time = tour.find('a', class_='tw-font-bold c-link c-link--inherit').text[9::]
        date = date_time[:11:]
        time = date_time[12::]
        return (date, time)


# -----------This function returns the duration of tour
    def find_duration(self, tour):
        for child in tour.find('div', class_="css-1f0x93j").contents:
            for grand_child in child.contents:
                return grand_child

            # ------------This one returns the avarage speed of -----------------#


    def find_distance(self, tour):
        grand_father = tour.find('span',
                                class_='icon-distance tw-inline-flex tw-items-center tw-justify-center tw-text-inherit tw-text-secondary').parent.parent

        return grand_father.find('span', class_='tw-font-bold').text[:4:]


    # ------------This one returns the avarage speed of -----------------#
    def find_speed(self, tour):
        grand_father = tour.find('span',
                                 class_='icon-speed tw-inline-flex tw-items-center tw-justify-center tw-text-inherit tw-text-secondary').parent.parent

        return grand_father.find('span', class_='tw-font-bold').text[:4:]


    # ------------This on returns the Uphill climbing of the tour-----------------#
    def find_uphill(self, tour):
        grand_father = tour.find('span',
                                 class_='icon-uphill tw-inline-flex tw-items-center tw-justify-center tw-text-inherit tw-text-secondary').parent.parent

        return grand_father.find('span', class_='tw-font-bold').text[0:4:]

    #------------This on returns the Downphill decending of the tour-----------------#
    def find_downhill(self, tour):
        try:
            grand_father = tour.find('span',class_='icon-downhill tw-inline-flex tw-items-center tw-justify-center tw-text-inherit tw-text-secondary').parent.parent
            return grand_father.find('span', class_='tw-font-bold').text[0:4:]
        except:
            return ''


    # ------------This on returns the Date as imprint in the Komoot record-----------------#
    def find_date(self, tour):
        order_of_months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                           'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11',
                           'December': '12'}

        raw_date = tour.find('span', class_='tw-text-secondary tw-text-sm tw-mb-0').text
        month_day = raw_date.split(',')[0].split(' ')
        month_day[0] = order_of_months[month_day[0]]
        year = raw_date[len(raw_date) - 4::]
        if int(month_day[1]) < 10:
            month_day[1] = '0' + month_day[1]
        date_to_return = year + month_day[0] + month_day[1]
        return date_to_return




#         # ---------This sub seperate the time duration of the rides to seperate weeks DF-----------#
#
#     def weekly_rides_seperator_DF(self, df, start_date):
#         weekly_rides = pd.DataFrame(columns=['Date', 'Distance', 'Duration', 'Count'])
#         DAYS = timedelta(7)
#         Day = timedelta(1)
#         week_start_date = pd.to_datetime(start_date)
# #------chose the first comning Sunday ----------#
#         while week_start_date.weekday() != 6:
#             week_start_date += Day
#         last_date = df['Date'].max()
#
#
#         while week_start_date < last_date:
#             weekly_activities = df[(df['Date'] >= week_start_date) & (df['Date'] < (week_start_date + DAYS))]
#
#             weekly_rides = weekly_rides.append({'Date': week_start_date , 'Distance': weekly_activities.Distance.sum(),
#                                                 'Duration' : weekly_activities.Duration.sum(), 'Count' : weekly_activities.Distance.count()}, ignore_index=True)
#
#             week_start_date += DAYS



        return weekly_rides

    def time_to_float(self, time):
        time_parse = time.split(':')
        hours = int(time_parse[0])
        minutes= int(time_parse[1]) / 60
        return hours +minutes


    #--Initiate create Pandas DataFreme---#
    def create_pandas(self, soup):

        init_line = ['Date', 'Name', 'Duration', 'Distance', 'Speed', 'UpHill', 'DownHill']
        komoot_tours = pd.DataFrame(columns = init_line)

        all_ul = soup.find_all("ul")
        for i in range(len(all_ul)):
            if all_ul[i].attrs['class']==['o-list-ui', 'o-list-ui--large', 'o-list-ui--separator', 'o-list-ui--border', 'o-list-ui--flush-vertical']:
                tours=all_ul[i].find_all("li")
                for tour in range(len(tours)):
                    date = pd.DataFrame([self.find_date(tours[tour])], columns =['Date']).astype('datetime64')
                    (date_in_name, start_time_in_name) = self.find_name(tours[tour])
                    time_in_motion = self.time_to_float((self.find_duration(tours[tour])))
                    distance = float(self.find_distance(tours[tour]))
                    speed = float(self.find_speed(tours[tour]))
                    uphill = self.find_uphill(tours[tour])
                    downhill = self.find_downhill(tours[tour])
                    line = pd.DataFrame([[date.Date[0], date_in_name, time_in_motion, distance, speed, uphill, downhill]], columns = init_line)
                    komoot_tours = komoot_tours.append(line, ignore_index = True)
        komoot_tours.drop_duplicates(inplace=True)
        #print(komoot_tours)
        return komoot_tours

#-----end of class ---#

class K_statistics():
    def __init__(self):
        pass

    # ---------This sub seperate the time duration of the rides to seperate weeks DF-----------#
    def weekly_rides_seperator_DF(self, df, start_date, date_set):
        weekly_rides = pd.DataFrame(columns=['Date', 'Distance', 'Duration', 'Count'])
        DAYS = timedelta(7)
        Day = timedelta(1)
        if not date_set[4]:
            week_start_date = pd.to_datetime(start_date)
        elif date_set[4]:
            week_start_date = df['Date'].min()

        # ------chose the first comming Sunday ----------#
        while week_start_date.weekday() != 6:
            week_start_date += Day
        last_date = df['Date'].max()
        while week_start_date < last_date:
            weekly_activities = df[(df['Date'] >= week_start_date) & (df['Date'] < (week_start_date + DAYS))]

            weekly_rides = weekly_rides.append(
                {'Date': week_start_date, 'Distance': weekly_activities.Distance.sum(),
                 'Duration': weekly_activities.Duration.sum(), 'Count': weekly_activities.Distance.count()},
                ignore_index=True)

            week_start_date += DAYS

        return weekly_rides

    # ---------This sub initiate the time duration of the rides from a start date DF-----------#
    def detailed_rides_from_date_DF(self, df, start_date, date_set):
        detailed_rides = pd.DataFrame(columns=['Date', 'Distance', 'Duration', 'Count'])
        Day = timedelta(1)
        start_date = pd.to_datetime(start_date)
        last_date = df['Date'].max()
        while start_date < last_date:
            daily_activitis = df[df['Date'] == start_date]

            activitis_to_add = pd.DataFrame({'Date': daily_activitis['Date'], 'Distance': daily_activitis['Distance'],'Duration': daily_activitis['Duration'], 'Count': 1})
            detailed_rides = detailed_rides.append(activitis_to_add, ignore_index=True)

            start_date += Day
        return detailed_rides





