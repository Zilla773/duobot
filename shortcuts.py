from selenium import webdriver
import login
import json
from translate import Translator # https://pypi.org/project/translate/

to_en = Translator(to_lang='en', from_lang='es')
to_es = Translator(to_lang='es', from_lang='en')
WebElement = webdriver.remote.webelement.WebElement

with open("xpaths.json", "r") as f:
    xpaths = f.read()
xpaths = json.loads(xpaths)

with open("css_selectors.json", "r") as f:
    css_selectors = f.read()
# global css_selectors
css_selectors = json.loads(css_selectors)

def get(driver, xpath):
    return driver.find_element_by_xpath(xpath)
def click(driver, xpath):
    get(driver, xpath).click()
def write(driver, xpath, text):
    get(driver, xpath).send_keys(text)

def get_text_in_quotes(string):
    """
    Returns the text in double quotes from a given string, e.g.
    Which one of these is “the apple”?
    would return 'the apple' (without the single quotes)
    """
    new_str = ""
    add_to_new_str = False
    for char in string:
        if add_to_new_str:
            new_str += char

        if char == '\"' or ord(char) in [8220, 8221]: # in and out quotes are different! # the "quotation marks used in duolingo aren't acutally quotation marks!"
            add_to_new_str = not(add_to_new_str)

    return new_str[:-1] # the trailing quotation mark is left on so we need to remove it

def filter_question(string):
    new = ''
    for char in string:
        if char == '\"' or ord(char) in [8220, 8221]: # in and out quotes are different! # the "quotation marks used in duolingo aren't acutally quotation marks!"
            break
        new += char

    return new.strip() # removes leading and trailing spaces
        
def check_and_continue(driver):
    driver.find_element_by_xpath("//*[@id=\"session/PlayerFooter\"]/div/div/button").click() # check
    driver.find_element_by_xpath("//*[@id=\"session/PlayerFooter\"]/div/div[2]/button").click() # continue (assumes correct answer)

def image_multiple_choice(driver):
    question_element = driver.find_element_by_class_name("_2LZl6")
    question = question_element.text

    img_options = xpaths["img-ms"]
    option_elements = []

    for option_xpath in img_options.values():
        option_elements.append(driver.find_element_by_xpath(option_xpath))


    english_prompt = get_text_in_quotes(question)
    options_text = [element.text[:-2] for element in option_elements] # have to remove last 3 characters as they are \n{an integer from 1 to 3}

    answer = to_es.translate(english_prompt)
    try:
        answer_index = options_text.index(answer)
    except:
        answer_index = 0
    option_elements[answer_index].click()
    
    check_and_continue(driver)

def write_this_in_english(driver):
    selectors = css_selectors["Write this in English"]
    # get(driver, xpaths["use keyboard"]).click() # switch to keyboard
    driver.find_element_by_css_selector('#session\/PlayerFooter > div > div.GE35t > button').click()
    spanish = driver.find_element_by_css_selector(selectors["translation prompt"]).text
    english = to_en.translate(spanish)
    text_box = driver.find_element_by_css_selector(selectors["text box"])
    text_box.send_keys(english)

    check_and_continue(driver)

def how_do_you_say(driver):
    pass



    check_and_continue(driver)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.duolingo.com/skill/es/Intro/2")
    login.login(driver, 'clemybot', 'gotosyntaxerror')
    input('navigate to lesson... ')

    # img_options = {
    # "img-ms-1" : "//*[@id=\"root\"]/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[1]",
    # "img-ms-2" : "//*[@id=\"root\"]/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]",
    # "img-ms-3" : "//*[@id=\"root\"]/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[3]"
    # }

    # option_elements = []
    # for option_xpath in img_options.values():
    #     option_elements.append(driver.find_element_by_xpath(option_xpath))

    # image_multiple_choice(driver, driver.find_element_by_class_name("_2LZl6"), option_elements)
    # print(driver.get_element_by_)

    input('enter to terminate ')