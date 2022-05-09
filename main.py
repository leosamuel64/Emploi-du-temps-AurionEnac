from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import datetime
from cal_setup import get_calendar_service
import icalendar
import os
import re
# ----------------------------------------------------------------------------------
# ------------------------------- Configuration ------------------------------------
# ----------------------------------------------------------------------------------
USERNAME='XXXXXX'   # Aurion Username
PASSWORD='XXXXXX'   # Aurion Password

jour=5              # jour de syncro (lundi->1, mardi->2 ...)

File_ics_download='xxxxx'
Chromedriver_Path='xxxxx'
# ----------------------------------------------------------------------------------




service = get_calendar_service()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only


    
def connexion(driver,username_text,password_text):
    username = driver.find_element_by_id("username")
    username.send_keys(username_text)

    password = driver.find_element_by_name("password")
    password.send_keys(password_text)

    button = driver.find_element_by_id("j_idt28")
    button.click()
    
def Aller_page_EDT(driver):
    time.sleep(5)
    lien=driver.find_element_by_id("form:j_idt887")
    lien.click()
    
def Afficher_Semaine_suivante(driver):
    time.sleep(5)
    case = driver.find_element_by_id("form:week")
    case.clear()
    time.sleep(1)
    date=datetime.date.today()
    y=date.strftime("%Y")
    m=date.strftime("%m")
    d=date.strftime("%d")
    _,w,_=datetime.date(int(y), int(m), int(d)).isocalendar()
    w+=1
    
    case.send_keys(str(w)+'-'+str(y))
    time.sleep(10)
    bouton = driver.find_element_by_id("form:j_idt115")
    bouton.click()
    time.sleep(10)
    bouton = driver.find_element_by_id("form:j_idt115")
    bouton.click()
    
def Telecharger_EDT(driver):
    time.sleep(3)
    bouton=driver.find_element_by_id("form:j_idt120")
    bouton.click()
    
def couleur_ID(name):
    if re.search("Travaux pratiques",name)!=None:
        res=5
    elif re.search("Cours",name)!=None:
        res=7
    elif re.search("Conférence",name)!=None:
        res=8
    elif re.search("Bureau d'études",name)!=None:
        res=2
    elif re.search("Travaux dirigés",name)!=None:
        res=3
    elif re.search("EVALUATION",name)!=None:
        res=11
    else:
        res=1
    return res
    
def ajouter_events(file):
    e = open(file, 'rb')
    ecal = icalendar.Calendar.from_ical(e.read())
    for component in ecal.walk():
        if component.name == "VEVENT":
            name=component.get("summary")
            description=component.get("description")
            lieu=component.get("location")
            dstart=component.decoded("dtstart")
            dend=component.decoded("dtend")            
    
            event = {
                    'summary': name,
                    'location': lieu,
                    'colorId': couleur_ID(name),
                    'description': description,
                    'start': {
                        'dateTime': dstart.strftime("%Y-%m-%dT%H:%M:%S"),
                        'timeZone': 'Europe/Paris',
                            },
                    'end': {
                        'dateTime': dend.strftime("%Y-%m-%dT%H:%M:%S"),
                        'timeZone': 'Europe/Paris',
  },
}

            event = service.events().insert(calendarId='primary', body=event).execute()
    e.close()
    
def supprimer_fichier(file):
    os.system("rm "+file)
    
def main():
    semaines=[]
    while True:
        date=datetime.date.today()
        y=date.strftime("%Y")
        m=date.strftime("%m")
        d=date.strftime("%d")
        _,w,d=datetime.date(int(y), int(m), int(d)).isocalendar()
        if d>=jour and not((w+1) in semaines):
            driver = webdriver.Chrome(Chromedriver_Path, options=chrome_options)
            driver.get('https://aurion-prod.enac.fr/faces/Login.xhtml') 
            connexion(driver,USERNAME,PASSWORD)
            Aller_page_EDT(driver)
            Afficher_Semaine_suivante(driver)
            Telecharger_EDT(driver)

            file=File_ics_download
            print("fin Scraping")
            time.sleep(5)

            ajouter_events(file)
            supprimer_fichier(file)
            semaines.append(w+1)
            driver.close()
                    
    
    
main()

