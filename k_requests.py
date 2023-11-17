import requests
from bs4 import BeautifulSoup as beautiful
from source_scraper import k_in_DF
import pandas as pd
from datetime import date


#----Open Session and log in---#

class Fetch_Data():
    def __init__(self):
        my_url = self.bring_url()
        # 'https://www.komoot.com/user/555196135573/tours??sport_types=&type=tour_recorded&sort_field=date&sort_direction=desc&name=&status=private&hl=en&page=1&limit=48'
        page1= requests.get(my_url)
        self.soup = beautiful(page1.content, "html.parser")
        ''' To print html file for debugging'''
        # with open("html_to _test.html", "w") as f:
        #     f.write(self.soup.prettify())
        self.k_input = k_in_DF()
        self.komoot_tours_update = self.k_input.create_pandas(self.soup)
        self.today_date = date.today().strftime("%d%m%y")
        self.today_file_name = f"today_csv_{self.today_date}.csv"
        self.komoot_tours_update.to_csv(self.today_file_name)
        #self.input_file = pathname
        #self.update_main()

    #--Fetch URL ----#
    '''this functioin brings the currnt URL to get update'''
    def bring_url(self):
        try:
            file = open('current_url.txt', "r")
            url = file.read()[1:159:]
            file.close()
        except IOError:
            print("URL File does not exist")
            url = 'https://www.komoot.com/user/555196135573/tours??sport_types=&type=tour_recorded&sort_field=date&sort_direction=desc&name=&status=private&hl=en&page=1&limit=48'

        return url


    # ----------save to main.csv----------#
    '''-------this function check if there is existing main.csv. if yes backup it
    --------and save the new on in place'''
    def save_main_csv(self):
        try:
            old_csv = pd.read_csv('main.csv')
            old_csv.to_csv(f"main{self.today_date}.csv")
        except IOError:
            print("No main.csv exists")
        self.komoot_tours.to_csv('main.csv')

    #----get the html file --------------#
    #----this def get the html file and create the "self.komoot_tours" from it.
    def update_file(self, input_file):
        try:
            file = open(input_file, "br")
        except FileNotFoundError:
            print("File does not exist, please type the exact name")
        page = file.read()
        file.close()
        soup = beautiful(page,"html.parser")
        print(len(soup.body.prettify()))
        self.komoot_tours = self.k_input.create_pandas(soup)
        self.save_main_csv()
        #return soup

    '''function to reload the main. append the new file from the request and save as the new_main.csv'''
    def update_main(self):
        try:
            old_main = pd.read_csv('main.csv', parse_dates=[1])
            old_main.to_csv(f"main{self.today_date}.csv")
        except IOError:
            print("main.csv does not exist")
            return False
        try:
              comming_update = pd.read_csv(self.today_file_name, parse_dates=[1])
        except IOError:
            print("updated.csv does not exist")

        #new_main = old_main.append(self.komoot_tours_update, ignore_index=True)
        new_main = old_main.append(comming_update, ignore_index=True)
        new_main.drop('Unnamed: 0', inplace=True, axis=1)
        #new_main = new_main.sort_values(by="Date", ascending=False)
        #new_main.drop_duplicates(subset="Date", inplace=True)
        new_main.drop_duplicates(inplace=True)
        new_main = new_main.sort_values(by="Date", ascending=False)
        new_main.to_csv("main.csv")

        return True



#-----------Start main -------#
if __name__ == "__main__":
    fetch_test = Fetch_Data()
    fetch_test.update_file(("Doron 030322.html"))

