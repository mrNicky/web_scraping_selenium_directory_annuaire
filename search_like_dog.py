from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import csv


def repair_by_spe():
        #--- Return all type of repairers you can scrape in http://www.allo-reparateurs.fr
    spe = webdriver.Firefox(executable_path=r'/home/zack/Bureau/jupyter/web_scraping/geckodriver')
    spe.get("http://www.allo-reparateurs.fr/specialites/")
    liste_spe = []
    for i in ['block_1_ville', 'block_2_ville']:
        liste_spe += [i.text for i in spe.find_elements_by_class_name(i)]
    for j in liste_spe:
        print(j)
    spe.close()

def search_like_dog(what, where):
    #--- Find elements and save in csv file  ---
    browser = webdriver.Firefox(executable_path=r'/home/zack/Bureau/jupyter/web_scraping/geckodriver')
    browser.get("http://www.allo-reparateurs.fr/")

    specialite = browser.find_element_by_id('categorie_rech')
    ville = browser.find_element_by_id('location_rech')

    specialite.click()
    specialite.send_keys(what)

    ville.click()
    ville.send_keys(where)
    ville.submit()
    browser.implicitly_wait(5)

    #--- Save infos in dict ---
    dic = {"reparateur": [], "adresse": [], "numero": []}
    p= 2
    while True:# les pages 1, 2, 3, 4
        try:
            element = len(browser.find_elements_by_class_name('pro'))

            for i in range(element):
                browser.find_elements_by_class_name('pro')[i].click()
                browser.implicitly_wait(3)
                try:
                    WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')
                    alert = browser.switch_to.alert
                    alert.accept()
                    print("alert accepted")
                except TimeoutException:
                    print("no alert")

                dic['reparateur'] += [(browser.find_element_by_class_name('fiche')).text]
                dic['adresse'] += [(browser.find_element_by_class_name('adress')).text]
                dic['numero'] += [(browser.find_element_by_class_name('liste_tel')).text]
                print(dic)
                browser.back()
                browser.implicitly_wait(2)
            page = browser.find_element_by_link_text(str(p)) #page 2, 3, 4
            page.click()
            p +=1

        except NoSuchElementException:
            #--- Save infos in csv file ---
            with open('reparateur.csv', 'w') as f:
                f = csv.writer(f)
                f.writerow(dic.keys())
                f.writerows(zip(*dic.values()))
            browser.close()
            print("FINISH")
            break
search_like_dog("plombier", "75013")
