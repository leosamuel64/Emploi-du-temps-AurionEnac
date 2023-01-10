from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import datetime
from cal_setup import get_calendar_service
import icalendar
import os
import re
import json
import api

# ----------------------------------------------------------------------------------
# ------------------------------- Configuration ------------------------------------
# ----------------------------------------------------------------------------------

with open('config.json', 'r') as f:
    data = json.load(f)

USERNAME = data['login']   # Aurion Username
PASSWORD = data['password']   # Aurion Password

jour = data['jour']           # jour de syncro (lundi->1, mardi->2 ...)

File_ics_download = data['ics']
Chromedriver_Path = data['chrome']
API=api.API()

# ----------------------------------------------------------------------------------


# service = get_calendar_service()


def init(login,pwd):
    API.login(login,pwd)
    API.navigate()

    
def download_week(week_nb,year):
    API.selectCal(week_nb,year)
    ics = API.getCal()
    file = open('planning.ics','w')
    file.write(ics)
    
    
def download_next_week():
    date = datetime.date.today()
    y = date.strftime("%Y")
    m = date.strftime("%m")
    d = date.strftime("%d")
    _, w, _ = datetime.date(int(y), int(m), int(d)).isocalendar()
    w += 1
    download_week(w,int(y))
    

def couleur_ID(name):
    if re.search("Travaux pratiques", name) != None:
        res = 5
    elif re.search("Cours", name) != None:
        res = 7
    elif re.search("Conférence", name) != None:
        res = 8
    elif re.search("Bureau d'études", name) != None:
        res = 2
    elif re.search("Travaux dirigés", name) != None:
        res = 3
    elif re.search("EVALUATION", name) != None:
        res = 11
    else:
        res = 1
    return res


def ajouter_events(file,service):
    e = open(file, 'rb')
    ecal = icalendar.Calendar.from_ical(e.read())
    for component in ecal.walk():
        if component.name == "VEVENT":
            name = component.get("summary")
            description = component.get("description")
            lieu = component.get("location")
            dstart = component.decoded("dtstart")
            dend = component.decoded("dtend")

            event = {
                'summary': name,
                "colorId": couleur_ID(name),
                'location': lieu,
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
    semaines = []
    while True:
        date = datetime.date.today()
        y = date.strftime("%Y")
        m = date.strftime("%m")
        d = date.strftime("%d")
        _, w, d = datetime.date(int(y), int(m), int(d)).isocalendar()
        if d >= jour and not((w+1) in semaines):
            download_next_week()
            file = 'planning.ics'
            print("Fin Scraping")
            time.sleep(5)
            
            service = get_calendar_service()
            
            ajouter_events(file,service)
            supprimer_fichier(file)
            semaines.append(w+1)


main()
