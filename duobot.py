from selenium import webdriver 
from translate import Translator # https://pypi.org/project/translate/
import json
from shortcuts import *
from login import login
from time import sleep

questions = {
    "Which one of these is" : image_multiple_choice,
    "Write this in English" : write_this_in_english
}


if __name__ == "__main__":

    # open xpaths file
    with open("xpaths.json", "r") as f:
        xpaths = f.read()
    xpaths = json.loads(xpaths)

    # login
    driver = webdriver.Chrome()
    driver.get("https://www.duolingo.com/skill/es/Intro/2?isLoggingIn=true")

    username, password = "clemybot", "gotosyntaxerror"
    login(driver, username, password)

    # input("navigate to relevant area ")


    while True:
        try:
            sleep(0.5)
            question_element = driver.find_element_by_css_selector('#root > div > div > div > div > div._3yOsW._3VXxf > div > div > div > div > div.FZpIH > h1')
            question_text = question_element.text

            just_question = filter_question(question_text)
            relevant_function = questions[just_question]
            relevant_function(driver)

        except Exception as e:
            raise(e)

