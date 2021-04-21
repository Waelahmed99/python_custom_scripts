import operator
import csv
import pandas as pd
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


lst = []
for i in range(5):
    with open("page{}.txt".format(i + 1), "+r") as file:
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
            del subs[0:4]
            dur = 1
            points = 0
            for sub in subs:
                time = sub.find('span', 'cell-time')
                if time is not None:  # 0 to 1440
                    time = time.text
                    if time.count(":") == 1:
                        time = "0:" + time
                    time = time.split(':')
                    minutes = int(time[0]) * 24 * 60 + int(time[1]) * 60 + int(time[2])
                    if minutes <= 1440 * dur + 120:
                        par.verdicts.append('✅')
                        # print("✅  ", end="")
                        points += 5
                    else:
                        # print("❌  ", end="")
                        par.verdicts.append('❌')

                else:
                    # print("❌  ", end="")
                    par.verdicts.append('❌')
                dur += 1
            # print(points, name.text, sep="   ")
            par.points = points
            lst.append(par)
        except:
            pass

lst.sort(key=operator.attrgetter('points'), reverse=True)
with open('output.csv', mode='w') as employee_file:
    outputFile = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = get_problems()
    headers.append("points")
    headers.insert(0, "Handle")
    outputFile.writerow(headers)
    for part in lst:
        outList = part.verdicts
        outList.append(part.points)
        outList.insert(0, part.name)
        outputFile.writerow(outList)

read_file = pd.read_csv('output.csv')
read_file.to_excel ('output.xlsx', index=None, header=True)

