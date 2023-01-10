import requests
from bs4 import BeautifulSoup #pip install beautifulsoup4
from urllib import parse
import time
import utils


HEADERS = {
        'Host': 'aurion-prod.enac.fr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://aurion-prod.enac.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
}


class API:
    def __init__(self) -> None:
        self.session = requests.Session()

    def login(self, username, password):
        url = "https://aurion-prod.enac.fr/login"

        payload=f'username={username}&password={password}&j_idt28='
        headers = {
        'Referer': 'https://aurion-prod.enac.fr/faces/Login.xhtml',
        }
        headers.update(HEADERS)
        r = self.session.post(url, headers=headers, data=payload)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        viewstate  = soup.find(name='input',attrs={"id":'j_id1:javax.faces.ViewState:0'})["value"]
        print("login viewstate : "+ str(viewstate))
        self.loginViewState = parse.quote(viewstate)
        print("Connected to Aurion")

    def navigate(self):

        url = "https://aurion-prod.enac.fr/faces/MainMenuPage.xhtml"

        payload = f"form=form&form%3AlargeurDivCenter=1620&form%3Asauvegarde=&form%3Aj_idt825%3Aj_idt827_dropdown=1&form%3Aj_idt825%3Aj_idt827_mobiledropdown=1&form%3Aj_idt825%3Aj_idt827_page=0&form%3Aj_idt916%3Aj_idt919_view=basicDay&form%3Aj_idt786_focus=&form%3Aj_idt786_input=44239&javax.faces.ViewState={self.loginViewState}&form%3Asidebar=form%3Asidebar&form%3Asidebar_menuid=1"
        headers = {
        'Referer': 'https://aurion-prod.enac.fr/faces/MainMenuPage.xhtml',
        }
        headers.update(HEADERS)
        r = self.session.post(url, headers=headers, data=payload)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        viewstate  = soup.find(name='input',attrs={"id":'j_id1:javax.faces.ViewState:0'})["value"]
        self.calendarViewState = parse.quote(viewstate)
        print("At timetable")

    def selectCal(self, weekNumber, year):
        self.weeknumber = weekNumber
        self.year = year
        monday = utils.getUTCDayWWeekNumber(weekNumber, year)
        self.date_monday = parse.quote(monday.strftime("%d-%m-%Y"))
        micro_monday = int(time.mktime(monday.timetuple())) * 1000
        end_of_week = utils.getWeekPlus1(monday)
        micro_end_of_week = int(time.mktime(end_of_week.timetuple())) * 1000

        url = "https://aurion-prod.enac.fr/faces/Planning.xhtml"

        payload = f"javax.faces.partial.ajax=true&javax.faces.source=form%3Aj_idt117&javax.faces.partial.execute=form%3Aj_idt117&javax.faces.partial.render=form%3Aj_idt117&form%3Aj_idt117=form%3Aj_idt117&form%3Aj_idt117_start={micro_monday}&form%3Aj_idt117_end={micro_end_of_week}&form=form&form%3AlargeurDivCenter=1620&form%3Adate_input=2{self.date_monday}&form%3Aweek={self.weeknumber}-{self.year}&form%3Aj_idt117_view=agendaWeek&form%3AoffsetFuseauNavigateur=0&form%3Aonglets_activeIndex=0&form%3Aonglets_scrollState=0&form%3Aj_idt236_focus=&form%3Aj_idt236_input=44239&javax.faces.ViewState={self.calendarViewState}"

        headers = {} 
        headers.update(HEADERS)
        headers.update({
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Faces-Request': 'partial/ajax',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://aurion-prod.enac.fr/faces/Planning.xhtml',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        })
        headers.pop('Sec-Fetch-User')
        r = self.session.post(url, headers=headers, data=payload)
        print(f"Selected week : {weekNumber}")
        self.date_monday = self.date_monday.replace("-", "%2F")

    def getCal(self):
        url = "https://aurion-prod.enac.fr/faces/Planning.xhtml"
        payload = f"form=form&form%3AlargeurDivCenter=1620&form%3Adate_input={self.date_monday}&form%3Aweek={self.weeknumber}-{self.year}&form%3Aj_idt117_view=agendaWeek&form%3AoffsetFuseauNavigateur=0&form%3Aonglets_activeIndex=0&form%3Aonglets_scrollState=0&form%3Aj_idt236_focus=&form%3Aj_idt236_input=44239&javax.faces.ViewState={self.calendarViewState}&form%3Aj_idt120=form%3Aj_idt120"
        headers = {} 
        headers.update(HEADERS) 
        headers.update({
        'Referer': 'https://aurion-prod.enac.fr/faces/Planning.xhtml',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Content-Type':'application/x-www-form-urlencoded',
        })
        r = self.session.post(url, headers=headers, data=payload)
        print("Got the ICS file")
        return(r.text)