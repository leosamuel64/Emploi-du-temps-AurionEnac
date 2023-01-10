# Emploi du temps : Aurion-Enac Google-Agenda
Synchronisation de l'emploi du temps depuis Aurion vers un google agenda
Grande inspiration pour recuperer le fichier ics : https://github.com/Spitfireap/PyAurionPlanningCalDav

## Installation

Testé sur un Raspberry pi 3B+ avec Debian (Buster)


- Installation des bibliotheques Python

``` Bash
$ sudo pip3 install icalendar
$ sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Configuation

- Création d'un projet google

Tuto : https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/

Il faut joindre le fichier JSON et indiquer son emplacement dans le fichier *config.json*

- Configuration de Aurion
Dans *config.json*, il faut indiquer :
  - login 
  - mot de passe 
  - jour de synchronisation (Vendredi -> 5)

## Utilisation

``` Bash
$ python3 main.py
```

