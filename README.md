# Emploi du temps : Aurion-Enac Google-Agenda
Synchronisation de l'emploi du temps depuis Aurion vers un google agenda

## Installation

Testé sur un Raspberry pi 3B+ avec Debian (Buster)

- Installation de chromium et du driver

``` Bash
>> sudo apt install chromium chromium-l10n
>> sudo apt install chromium-chromedriver
```
- Installation des bibliotheques Python

``` Bash
>> sudo pip3 install selenium
>> sudo pip3 install icalendar
>> sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Configuation

- Création d'un projet google

Tuto : https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/

Il faut joindre le fichier JSON et indiquer son emplacement dans le fichier *cal_setup.py*

- Configuration de Aurion
Dans main.py, il faut indiquer :
  - login 
  - mot de passe 
  - jour de synchronisation (Vendredi -> 5)
  - emplacement du fichier planning téléchargé (.../Downloads/Planning.ics par exemple)
  - emplacement du fichier chromedriver
  
  Pour obtenir ce chemin :
  ``` Bash
>> which chromedriver
/usr/bin/chromedriver
```


## Utilisation

``` Bash
>> python3 main.py
```

