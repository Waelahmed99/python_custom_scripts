import operator
import csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time as sleep
from getpass import getpass

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Participant:
    name = any
    verdicts = any
    points = any

    def __init__(self, nam):
        self.name = nam
        self.verdicts = []


def get_data(file):
    f = open(file, "+r")
    return f.read().split("\n")

def main():
    lst = []
    exceptions = get_data("exceptions.txt")
    print("Make sure you added all problems names in " + bcolors.HEADER + "problems.txt" + bcolors.ENDC)
    print("The script will open each page for you")
    print(bcolors.WARNING + "This might take 3 seconds per page, please be patient.😊\n" + bcolors.ENDC)
    pages = int(input("Enter number of pages: "))

    email = input("Enter codeforces handle/email: ")
    password = getpass(prompt="Enter codeforces password: ")

    driver = webdriver.Firefox()
    driver.get("https://codeforces.com/enter")
    element = driver.find_element_by_id("handleOrEmail")
    element.send_keys(email)
    element = driver.find_element_by_id("password")
    element.send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()

    input("Press any key after you ensure codeforces login... ")
    print()
    pagesHTML = []
    for i in range(1, pages + 1):
        print(bcolors.OKCYAN +  "Scrapping" + bcolors.ENDC + " page No.{} content".format(i))
        url = "https://codeforces.com/gym/324287/standings/page/{}".format(i)
        driver.get(url)
        pagesHTML.append(driver.page_source)
        sleep.sleep(3)
            
    for i in range(pages):
        data = str(pagesHTML[i])
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find_all('table', class_='standings')[0]
        body = table.find('tbody')
        handles = body.find_all('tr')

        for handle in handles:
            name = handle.find('td', 'contestant-cell')
            try:
                name = name.find('a', 'rated-user')
                par = Participant(name.text)
                subs = handle.find_all('td')
                del subs[0:4]  # Remove name, penalty, etc.. tds'
                dur = 1
                points = 0
                for sub in subs:  # Loop on every submission
                    time = sub.find('span', 'cell-time')
                    if time is not None:
                        time = time.text
                        if time.count(":") == 1:
                            time = "0:" + time
                        time = time.split(':')
                        minutes = int(time[0]) * 24 * 60 + int(time[1]) * 60 + int(time[2])
                        if minutes <= 1440 * dur + 120:
                            par.verdicts.append('✅')
                            points += 5
                        else:
                            par.verdicts.append('❌')
                    else:
                        par.verdicts.append('❌')
                    dur += 1
                par.points = points
                lst.append(par)  # append new participant
            except:
                pass

    for exception in exceptions:
        exception = exception.split(' ')
        for par in lst:
            if par.name == exception[0]:
                print(bcolors.OKBLUE + par.name + " exception problem " + str(exception[1]) + bcolors.ENDC)
                par.verdicts[int(exception[1]) - 1] = '✅'
                par.points += 5

    lst.sort(key=operator.attrgetter('points'), reverse=True)
    with open('output.csv', mode='w') as employee_file:
        output_file = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers = get_data("problems.txt")
        headers.insert(0, "Handle")
        headers.insert(1, "points")
        output_file.writerow(headers)
        for part in lst:
            out_list = part.verdicts
            out_list.insert(0, part.name)
            out_list.insert(1, part.points)
            output_file.writerow(out_list)

    read_file = pd.read_csv('output.csv')
    read_file.to_excel('output.xlsx', index=None, header=True)
    os.remove("output.csv")
    print(bcolors.OKGREEN + "\nDone scrapping the standing in output.xlsx 💁" + bcolors.ENDC)


if __name__ == "__main__":
    main()
