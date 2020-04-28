from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import dataInsulin


def ScrapMyLife():
    # driver = webdriver.Firefox()
    # driver.get("https://france.mylife-software.net/Pages/Filterable/Logbook.aspx?ItemValue=logbook")
    # userName = driver.find_element_by_id("UserName")
    # userName.send_keys(os.getenv('USERNAME_MYLIFE'))
    # userPass = driver.find_element_by_id("Password")
    # userPass.send_keys(os.getenv('PASSWORD_MYLIFE'))

    # driver.find_element_by_id("LoginButton").click()

    # tableElement = driver.find_element_by_id("ctl00_conContent_rgLogbookGrid_ctl00")
    # contentHtml = tableElement.get_attribute('outerHTML')
    # driver.close()


    #with open('table.html', 'w') as f:
    #    f.write(tableElement.get_attribute('outerHTML'))#

    with open("table.html") as fp:
        contentHtml = fp.read()

    arrayInsul = dataInsulin.dataInsulinOp.convertHtml2dataInsulin(contentHtml)
    #dataInsulin.dataInsulinOp.saveJson(arrayInsul)

    return arrayInsul

