import requests
import configparser
import csv

def load_data():
    config = configparser.ConfigParser()
    config.read('scripts/config.cfg')
    crimeURL = config['URL']['crimesRegistadosURL']
    ## Dados de 2021
    r= requests.get(crimeURL).json()[0]['Dados']['2021']
    with open('data/crimeData.csv', 'w') as file:
        ## get all unique keys 
        header = {head for ocurrence in r for head in ocurrence.keys()}
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        writer.writerows(r)

load_data())