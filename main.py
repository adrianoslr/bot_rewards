import time

from selenium import webdriver
from selenium.webdriver.common.by import By


from lib.mso.save_log import logger
words=("aa","bb","cc","dd","ee","ff","gg","hh","ii","jj","kk","ll","mm","nn","oo","pp","qq","rr","ss","tt","uu","vv","ww","xx","yy","zz","aaa","bbb","ccc","ddd","eee","fff","ggg","hhh")

def open_site():
    """Login and search rewards"""
    browser = webdriver.Edge()
    browser.maximize_window()
    browser.get('https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1')
    time.sleep(5)
    cookie = browser.find_element(By.ID,"bnp_btn_accept")
    cookie.click()

    for word in words:
        if words.index(word) % 4 == 0 and words.index(word) !=0:
        time.sleep(900)
        element = browser.find_element(By.ID, 'sb_form_q')
        element.send_keys(word)
        element.submit()
        time.sleep(3)
        click= browser.find_element(By.ID,"rh_meter")
        click.click()
        time.sleep(2)
        browser.get('https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1')
        logger.debug("Running program")
        time.sleep(2)

    browser.quit()
    logger.debug("Closing program")


if __name__ == "__main__":
    open_site()
