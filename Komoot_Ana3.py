#--------Komoot Analyze Ver 1.3 02/02/22------#
#--- Preperation to work together with GUI ---#
import pandas as pd
import sys
from bs4 import BeautifulSoup as beautiful
from k_requests import Fetch_Data
from source_scraper import k_in_DF
from source_scraper import K_statistics as Stat


#----------Varables definition area--------------#


#-----------Start main Program--------------#


class K_Analize():
    def __init__(self, pathname, conf):
        self.input_file  = pathname
        self.conf = conf
        print('This is conf', self.conf)
        # self.start_date = '1/1/2021'
        self.start_date = conf[0]
        self.fetch = Fetch_Data()

    def fill_data(self):
        k_stat = Stat()
        if self.fetch.update_main():
            self.komoot_tours = pd.read_csv('main.csv', parse_dates=[1])
        else:
            print("main does not exist")
        self.pandas_weekly_table = k_stat.weekly_rides_seperator_DF(self.komoot_tours, self.start_date, self.conf)
        self.pandas_from_start_date = k_stat.detailed_rides_from_date_DF(self.komoot_tours, self.start_date, self.conf)

        self.summary = []  # The Summary of information to to present
        if self.conf[1]:
            self.data = self.print_2_screen_DF()  #The information to to present
        if self.conf[2]:
            self.data = self.print_details_Df()
            # print(self.data)


    def get_tours(self):
        try:
            self.komoot_tours = pd.read_csv('main.csv', parse_dates=[1])
            self.fetch.update_main
        except IOError:
            print("main.csv does not exists")

            exit()


    def get_file(self):
        try:
            file = open(self.input_file, "br")
        except FileNotFoundError:
            print("File does not exist, please type the exact name")

        page = file.read()
        file.close()
        soup = beautiful(page,"html.parser")
        print(len(soup.body.prettify()))
        return soup

    #create new main form html file
    def create_from_html(self):
        k_input = k_in_DF()
        self.soup = self.get_file()
        komoot_tours = k_input.create_pandas(self.soup)
        komoot_tours.to_csv('main.csv')




    #----------Print the summary to file------------#

    def print_2_file_Df(self):
        i = 0
        if self.conf[0][::-1][:4:][::-1] != '.txt':
            out_file = self.conf[0] + '.txt'
        else:
            out_file = self.conf[0]
        original_stdout = sys.stdout #keep the orginal output pipe
        try:
            file = open(out_file,"w")
        except IOError:
            print("Cannot Open OutPut file")
        sys.stdout= file     #change the std output
        print('\n', f"{'#' : >2}{'   Date' : <14}{'Duration': ^10}{'Distance' : ^10}{'Trips' : ^14}")
        for n in self.data:
            i +=1
            print(f"{i: ^5}{n[0]: <10}{n[1]: >10}{n[2]: >10}{n[3]: >10}")

        print('\n')
        print( f"{'All Time:': <10}{self.summary[0] : >4}{'  All Distance:' : ^12}{self.summary[1]: >5}"
        f"{'  All Trips:' : ^11} {self.summary[2]: >4}")
        sys.stdout = original_stdout # retain the original output pipe
        file.close()

    #----------print summary to screen------------#

    def print_2_screen_DF(self):
        s_list = self.pandas_weekly_table
        s_list = s_list.sort_values(by="Date", ascending=False)
        data = []
        for n in range(len(s_list)):
            line =[]
            line.append(str(s_list.Date.iloc[n])[:10])
            line.append(str(round((s_list.Duration.iloc[n]),2)))
            line.append(str(round((s_list.Distance.iloc[n]),2)))
            line.append(str(round((s_list.Count.iloc[n]), 2)))
            data.append(line)

        self.summary.append(str(round(s_list.Duration.sum(), 2)))
        self.summary.append(str(round(s_list.Distance.sum(), 2)))
        self.summary.append(s_list.Count.sum())
        return data

    def print_details_Df(self):
        s_list = self.pandas_weekly_table
        k_list = self.pandas_from_start_date
        k_list = k_list.sort_values(by="Date", ascending=False)
        data = []
        for n in range(len(k_list)):
            line = []
            line.append(str(k_list.Date.iloc[n])[:10])
            line.append(str(round((k_list.Duration.iloc[n]), 2)))
            line.append(str(round((k_list.Distance.iloc[n]), 2)))
            # line.append(str(round((k_list.Count.iloc[n]), 2)))
            line.append('1')
            data.append(line)

        self.summary.append(str(round(s_list.Duration.sum(), 2)))
        self.summary.append(str(round(s_list.Distance.sum(), 2)))
        self.summary.append(s_list.Count.sum())

        return data












