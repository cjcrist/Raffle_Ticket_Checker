#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Searches online database for winning numbers for Saturday evening, downloads the csv file, and returns filename.
def search_dates(url, date):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.getcwd()}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    date_selector = driver.find_element_by_class_name("date-range-container ")
    start_date = date_selector.find_element_by_id("startDateId")
    if datetime.now().year == 2019:
        start_date.send_keys("1//1/2019")
    else:
        start_date.send_keys("1/1/" + str(datetime.now().year))
    end_date = date_selector.find_element_by_id("endDateId")
    end_date.send_keys(date)
    button = driver.find_element_by_class_name("msl-button.msl-button-green")
    button.send_keys(Keys.ENTER)
    csv_fn = ''
    for i in range(5):
        time.sleep(3)
        download = driver.find_element_by_xpath('//*[@id=\"pagination-element-top\"]/div/div[1]/a')
        download.send_keys(Keys.ENTER)
        # Gets the name of the csv file
        csv_fn = download.get_attribute("download")
        try:
            if os.path.exists(csv_fn):
                driver.close()
                break
            else:
                continue
        except Exception as e:
            print(str(e))
            sys.exit(0)
    return csv_fn


# Processes the csv file of all winning numbers and creates a dictionary of Saturday night drawings
def process_csv(csv_file):
    csv_dict = {}
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r') as f:
                numbers = pd.read_csv(f, delimiter=',')
                for i, row in numbers.iterrows():
                    if (datetime.strptime(row['Draw Date'], '%m/%d/%Y').strftime('%A')) == 'Saturday':
                        csv_dict[row['Draw Date']] = row['Winning Numbers'].replace(',', '')
                    else:
                        pass
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print(str(e))
    return csv_dict


# Checks the user's winning numbers against the csv dictionary and prints the results
def check_d(d, value_list):
    if not d:
        print("There was a problem downloading the winning numbers.")
        sys.exit(0)
    # Check for A
    for i in value_list:
        if i.upper() == 'A':
            print("The winning numbers are:\n")
            for k, v in d.items():
                print("{}--|-->{}".format(k, v))
            return
        else:
            pass
    winner_list = []
    for value in value_list:
        [winner_list.append((k, v)) for k, v in d.items() if v == value]
    if winner_list:
        for item in winner_list:
            print("Your ticket #" + item[1].replace(',', '') + " won on " + item[0])
    else:
        print("\n\t\t~~~¯\\_(ツ)_/¯~~~\n\t~~~You have no winning numbers!~~~")


def main():
    site = "https://www.michiganlottery.com/resources/number-tools?SELECTED_TOOL=PAST_RESULTS&SELECTED_GAME=3"
    today = datetime.now().strftime('%m/%d/%Y')

    # Check the dates and return the file name of the downloaded csv
    csv_filename = search_dates(site, today)
    if csv_filename is None:
        raise Exception("Failed to download csv file.")
    # Creates a dictionary of winning numbers
    csv_dict = process_csv(r'{}/{}'.format(os.getcwd(), csv_filename))
    # Get user input
    print("This tool was created to check your raffle ticket numbers against the winning numbers in the "
          "Weapon-a-Week Raffle.\n")
    print("To use this tool, enter 1 number at time and then press ENTER\n\n")
    user = input("Enter your first raffle ticket number, or type 'A' then ENTER to show all winning numbers.\n"
                 "You can also type 'C' to exit.\n")
    winning_numbers_list = []
    if user.upper() == 'C':
        print("Goodbye!")
        sys.exit(0)
    elif user.upper() == 'A':
        check_d(csv_dict, user)
        sys.exit(0)
    else:
        winning_numbers_list.append(user)
        while user.upper() != 'N':
            user = input("Enter your next raffle ticket number or type 'A' then ENTER to show all winning numbers.\n "
                         "Type 'N' or press ENTER if finished.\n")
            if user.upper() == 'N' or user == '':
                break
            else:
                winning_numbers_list.extend(user.strip().split(','))
    # Check the user's winning numbers against the csv dictionary of winning numbers and print the results
    check_d(csv_dict, winning_numbers_list)
    return 0


if __name__ == "__main__":
    main()

