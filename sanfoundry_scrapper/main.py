import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class Question:
    name = any
    answers = []
    answer = any

    def __init__(self, name, answer):
        self.answers = []
        self.name = name
        self.answer = answer


# sf-nav-bottom is next button.
url = input("Enter url: ")
fileName = input("Enter output file name: ")
next_button = input("Enter next button's xpath")
driver = webdriver.Firefox()
driver.fullscreen_window()
driver.get(url)

all_iframes = driver.find_elements_by_tag_name("iframe")
if len(all_iframes) > 0:
    print("Ad Found\n")
    driver.execute_script("""
        var elems = document.getElementsByTagName("iframe"); 
        for(var i = 0, max = elems.length; i < max; i++)
             {
                 elems[i].hidden=true;
             }
                          """)
    print('Total Ads: ' + str(len(all_iframes)))
else:
    print('No frames found')

result = []
for _ in range(3):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    questions = soup.find("div", "entry-content")
    questions = questions.find_all('p')

    for idx in range(1, len(questions) - 4):
        question = questions[idx]

        answerId = ""
        span = str(question.find("span"))
        for i in range(span.find('id="') + 4, len(span)):
            if span[i] == '"':
                break
            answerId = answerId + span[i]
        id = answerId
        try:
            answerId = '//*[@id="{}"]'.format(answerId)
            # //*[@id="id608e69037d726"]
            # //*[@id="id608e69037d726"]
            driver.execute_script("window.scrollTo(0, {})".format(300 * (idx - 1)))
            time.sleep(1)
            view_answer = driver.find_element_by_xpath(answerId)
            ActionChains(driver).move_to_element(view_answer).click().perform()
            time.sleep(1)
            parts = question.text.split("\n")
            answer = driver.find_element_by_xpath('//*[@id="target-{}"]'.format(id)).text
            print(idx, id, sep="  ")
            print(answer.split('\n')[0][-1], end='\n\n')
            q = Question(str(parts[0][2:]).strip(), answer.split('\n')[0][-1])
            for i in range(1, len(parts) - 1):
                q.answers.append(str(parts[i]).strip())
            result.append(q)
        except:
            print("Error occured at index {}".format(str(idx)))
    try:
        driver.find_element_by_xpath(next_button).click()
    except:
        break

with open('{}.json'.format(fileName), 'w') as outfile:
    outfile.write('[\n')
    for i in range(len(result)):
        question = result[i]
        outfile.write("{\n")
        outfile.write('"question": "{}",\n'.format(question.name))
        outfile.write('"correct_answer": "{}",\n'.format(question.answer))
        outfile.write('"answers": [\n')
        if i == 0:
            print(question.answers)
        for idx in range(0, len(question.answers)):
            if idx == len(question.answers) - 1:
                outfile.write('"{}"\n'.format(question.answers[idx]))
            else:
                outfile.write('"{}",\n'.format(question.answers[idx]))
        outfile.write("]\n")
        if i == len(result) - 1:
            outfile.write("}\n")
        else:
            outfile.write("},\n")
    outfile.write(']')
