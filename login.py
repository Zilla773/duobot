from selenium import webdriver
from time import sleep

def login(driver, username, password):

    for login, value in zip(driver.find_elements_by_class_name("_3MNft"), [username, password]):
        login.send_keys(value)

    print(type(driver.find_element_by_class_name("_1rl91")))
    driver.find_element_by_class_name("_1rl91").click()

    intro_xpath = '//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div'
    go_xpath = '//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[2]'
  
    while True:
        try:
            driver.find_element_by_xpath(intro_xpath).click() # click intro 1
            sleep(0.5)
            driver.find_element_by_xpath(go_xpath).click() # click start            
            break
        except:
            pass


    

if __name__ == "__main__":
    Driver = webdriver.Chrome()
    Driver.get("https://www.duolingo.com/skill/es/Intro/2?isLoggingIn=true")   

    login(Driver, "clemybot", "gotosyntaxerror")
    input('enter to quit')    