from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
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

    browser.implicitly_wait(15)

    #--- Save infos in dict ---
    dic = {"reparateur": [], "adresse": [], "numero": []}
    i= 2
    while True:
        try:
            dic["reparateur"] += [i.text for i in browser.find_elements_by_class_name('pro')]
            dic["adresse"] += [i.text[19:] for i in browser.find_elements_by_class_name('adress')]
            dic["numero"] += [i.text for i in browser.find_elements_by_class_name('liste_tel') if i.text != ""]
            page = browser.find_element_by_link_text(str(i))
            page.click()
            i+=1
        except NoSuchElementException:
            #--- Save infos in csv file ---
            with open('reparateur.csv', 'w') as f:
                f = csv.writer(f)
                f.writerow(dic.keys())
                f.writerows(zip(*dic.values()))
            browser.close()
            break

repair_by_spe()
search_like_dog("plombier", "75009")
