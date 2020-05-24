from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import dataInsulin
import os
# from pyvirtualdisplay import Display


def ScrapMyLife(fake=False):
    if (fake is False):
        # only for the docker use
        # TODO Improve the management of the content
        # display = Display(visible=0, size=(800, 600))
        # display.start()
        driver = webdriver.Firefox()
        driver.get("https://france.mylife-software.net/Pages/Filterable/Logbook.aspx?ItemValue=logbook")

        userName = driver.find_element_by_id("UserName")
        userName.send_keys(os.getenv('USERNAME_MYLIFE'))

        driver.find_element_by_id("LoginButton").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Password"))
        )
        userPass = driver.find_element_by_id("Password")
        userPass.send_keys(os.getenv('PASSWORD_MYLIFE'))

        driver.find_element_by_id("LoginButton").click()

        driver.get("https://france.mylife-software.net/Pages/Filterable/Logbook.aspx?ItemValue=logbook")

        tableElement = driver.find_element_by_id("ctl00_conContent_rgLogbookGrid_ctl00")
        contentHtml = tableElement.get_attribute('outerHTML')
        driver.close()
        # only for the docker use
        # TODO improve the management of the content
        # display.stop()
        with open('table.html', 'w') as f:
            f.write(contentHtml)
    else:
        with open("table.html") as fp:
            contentHtml = fp.read()

    arrayInsul = dataInsulin.dataInsulinOp.convertHtml2dataInsulin(contentHtml)
    # dataInsulin.dataInsulinOp.saveJson(arrayInsul)

    return arrayInsul
