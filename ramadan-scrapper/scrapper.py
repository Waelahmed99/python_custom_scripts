import operator
import csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from selenium import webdriver


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


def get_problems():
    f = open("problems.txt", "+r")
    return f.read().split("\n")


def main():
    lst = []
    exceptions = {
        'shaza.ehab192': 2,
        'Nada_Ashraf': 2,
        'EmanElsayed21': 8,
        'Alaa.Ahmed': 1,
        'Leena_Almekkawy': 2,
    }
    print("Make sure you added all problems names in " + bcolors.HEADER + "problems.txt" + bcolors.ENDC)
    print("The script will open each page for you\ninspect the content html, " + bcolors.BOLD +
          "right click in the html tag, and choose edit as html" + bcolors.ENDC)
    print(bcolors.WARNING + "To save in nano editor, press ctrl+s then ctrl+x to leave.\n" + bcolors.ENDC)
    pages = int(input("Enter number of pages: "))
    driver = webdriver.Firefox()

    driver.get("https://codeforces.com/enter")
    element = driver.find_element_by_id("handleOrEmail")
    email = input("Enter you Email/handle")
    element.send_keys(email)
    password = input("Enter your password")
    element = driver.find_element_by_id("password")
    element.send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()

    for i in range(1, pages + 1):
        input("Press any key to paste page {} content... ".format(i))
        url = "https://codeforces.com/gym/324287/standings/page/{}".format(i)
        driver.get(url)
        with open("pages/page{}.html".format(i + 1), "+w") as file:
            file.write(driver.context())
            
    for i in range(pages):
        with open("pages/page{}.html".format(i + 1), "+r") as file:
            data = file.read().rstrip().lstrip()

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
                if name.text in exceptions:
                    print(bcolors.OKBLUE + name.text + " exception problem " + str(exceptions[name.text]) + bcolors.ENDC)
                    par.verdicts[exceptions[name.text] - 1] = '✅'
                    par.points += 5
                lst.append(par)  # append new participant
            except:
                pass
    lst.sort(key=operator.attrgetter('points'), reverse=True)
    with open('output.csv', mode='w') as employee_file:
        output_file = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers = get_problems()
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
    os.system("rm pages/*")
    print(bcolors.OKGREEN + "Done scrapping the standing in output.xlsx 💁" + bcolors.ENDC)


if __name__ == "__main__":
    main()
