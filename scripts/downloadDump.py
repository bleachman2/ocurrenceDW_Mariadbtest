import requests
import csv


def load_data(r: requests.Response, dumpFile: str):
    with open(dumpFile, "w") as file:
        # get all unique keys
        header = {head for ocurrence in r for head in ocurrence.keys()}
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(r)


def load_crimesData(crimeURL: str, dumpFileName: str):
    r = requests.get(crimeURL).json()[0]["Dados"]["2021"]
    load_data(r, dumpFile=dumpFileName)


def load_metadata(metadataURL: str, dumpFile: str):
    r = requests.get(metadataURL).json()[0]["Dimensoes"]["Categoria_Dim"][0]
    r = [v for v in r.values()]
    r = [i[0] for i in r]

    load_data(r, dumpFile=dumpFile)
