#https://www.imdb.com/search/title/?genres=Action&explore=title_type%2Cgenres&ref_=ft_popular_0
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import re
import pandas as pd
from selenium.webdriver.common.by import By
import csv

class MovieExtract():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disbale-blink-features=AutomationControlled")
        self.service = Service(
            executable_path=r'C://Users//' + os.environ["USERNAME"] + '//Desktop//chromedriver-win64//chromedriver.exe')
        self.bot = webdriver.Chrome(service=self.service, options=chrome_options)

    def data_extract(self):
        movie_data = []
        genre_list = ["Action","Comedy","Horror","Animation","Romance","Family"]

        #COMMENT 1: LOOPING THROUGH THE GENRE LIST IN IMDB WEBSITE
        for genre in genre_list:
            url = "https://www.imdb.com/search/title/?genres=" + genre + "&explore=title_type%2Cgenres&ref_=ft_popular_0"
            self.bot.get(url=url)
            film_eles = self.bot.find_elements(By.CLASS_NAME, 'lister-item-content')
            for ele in film_eles:
                title = ''
                actor_names = ''
                director = ''
                cert = ''
                rate = ''
                year = ''
                # COMMENT 2: CREATING A TEMPORARY LIST TO COLLECT THE INDIVIDUAL FILM DETAILS
                row_data = []

                # COMMENT 3: EXTRACTING FILM TITLE NAME
                try:
                    title_ele = ele.find_element(By.TAG_NAME,"h3")
                    title = title_ele.find_element(By.TAG_NAME,"a").text
                    row_data.append(title)
                except:
                    row_data.append(title)

                # COMMENT 4: ADDING GENRE TO THE LIST
                row_data.append(genre)

                # COMMENT 5: EXTRACTING YEAR
                try:
                    year_text = ele.find_element(By.CLASS_NAME,"lister-item-year").text
                    year = re.findall("[0-9]+",year_text)
                    row_data.append(year[0])

                except:
                    row_data.append(year[0])

                # COMMENT 6: EXTRACTING CERTIFICATE

                try:
                    cert = ele.find_element(By.CLASS_NAME,"certificate").text
                    row_data.append(cert)
                except:
                    row_data.append(cert)

                # COMMENT 7: EXTRACTING RATINGS
                try:
                    rate_text = ele.find_element(By.CLASS_NAME,"ratings-bar").text
                    rate = re.findall('[0-9\.?]+',rate_text)
                    row_data.append(rate[0])
                except:
                    row_data.append(rate)

                # COMMENT 8: EXTRACTING DIRECTOR AND ACTORS

                try:
                    names = ele.find_elements(By.TAG_NAME,"p")

                    is_dir = False
                    for nn in names:
                        if re.search("Director", nn.text):
                            is_dir = True
                            break
                    for nam in names:
                        actors = nam.find_elements(By.TAG_NAME,"a")
                        for act in actors:
                            actor_names += act.text + ","
                    if is_dir == True:
                        names_split = actor_names.split(",")
                        director = names_split[0]
                        actor_names = ','.join(names_split[1:])
                        row_data.append(director)
                        row_data.append(actor_names[:-2])
                    else:
                        row_data.append(director)
                        row_data.append(actor_names[:-2])
                except:
                    row_data.append(director)
                    row_data.append(actor_names)

                movie_data.append(row_data)
        headers = ["Title", "Genre", "Year", "Certification", "Rating", "Director", "Actors"]
        with open(r'.\movie_data.csv', 'w',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(movie_data)
        return genre_list

    def movie_checker(self,genre_list):

        # COMMENT 9: READING THE MOVIE DATASET BY PANDAS

        df = pd.read_csv(r'.//movie_data.csv',encoding='latin-1')
        while True:
            print("Please choose any of following genres: Action/Comedy/Horror/Animation/Romance/Family")

            # COMMENT 10: RECEIVING THE INPUT FROM THE USER

            genre = input("Genre: ")
            genre = genre.title()
            if genre in genre_list:
                df2 = df[df["Genre"] == genre]
                movie_names = df2.Title.to_list()
                import random
                r = random.choice(movie_names)
                df3 = df2[df2["Title"] == r]

                # COMMENT 11: PRINTING THE REQUIRED DETAILS SUCH FILM TITLE, YEAR ETC... TO THE USER

                for ind, itn in enumerate(["Title","Genre","Year","Certification","Rating","Director","Actors"]):
                    if not pd.isna(df3.iloc[0,ind]):
                        print(itn,":",df3.iloc[0,ind])
                    else:
                        print(itn,":","Unknown")
                choice = input("Do you want to choose again? Y/N:")

                if str(choice).upper() == "Y":
                    continue
                else:
                    break
            else:
                print("Genre is not the given list")
                attempt = input("Do you want to try again Y/N:")
                if str(attempt).upper() == 'Y':
                    continue
                else:
                    break


if __name__ == '__main__':
     movies = MovieExtract()
     movies.data_extract()
     genre_list = movies.data_extract()
     movies.movie_checker(genre_list)
     print("Thank You! See you again")

