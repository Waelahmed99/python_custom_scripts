import operator
import csv
import pandas as pd
import os
from bs4 import BeautifulSoup


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
    pages = int(input("Enter number of pages: "))
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
                    print(name.text + " exception problem " + str(exceptions[name.text]))
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


if __name__ == "__main__":
    main()
