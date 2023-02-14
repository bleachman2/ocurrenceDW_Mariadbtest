import configparser
import scripts.treatment as trt
import scripts.downloadDump as dump


def read_configs() -> tuple[str]:
    config = configparser.ConfigParser()
    config.read("scripts/config.cfg")
    crimeURL = config["URL"]["crimesRegistadosURL"]
    dumpFileName = config["URL"]["crimesDump"]
    treatFileName = config["URL"]["crimesTreat"]
    metadataURL = config["URL"]["metadataURL"]
    metadataDump = config["URL"]["metadataDump"]
    metadataTreat = config["URL"]["metadataTreat"]
    metadataCrimesTreat = config["URL"]["metadataCrimesTreat"]

    return (
        crimeURL,
        dumpFileName,
        treatFileName,
        metadataURL,
        metadataDump,
        metadataTreat,
        metadataCrimesTreat,
    )


def main():
    (
        crimeURL,
        dumpFileName,
        treatFileName,
        metadataURL,
        metadataDump,
        metadataTreat,
        metadataCrimesTreat,
    ) = read_configs()
    dump.load_crimesData(crimeURL, dumpFileName)
    dump.load_metadata(metadataURL, metadataDump)
    trt.metadata_tratment(metadataDump, metadataTreat, metadataCrimesTreat)
    trt.crime_treatment(dumpFileName, treatFileName)


if __name__ == "__main__":
    main()
