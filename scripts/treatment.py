import pandas


def metadata_tratment(metadataDump: str, metadataTreat: str, metadataCrimesTreat: str):
    metadataPd = pandas.read_csv(metadataDump)
    metadataTypePD = metadataPd[metadataPd["dim_num"] == 3]
    metadataPlacePD = metadataPd[metadataPd["dim_num"] == 2]
    # metadataCountry = metadataPlacePD[metadataPlacePD["categ_nivel"] == 1]
    metadataC = metadataPlacePD[metadataPlacePD["categ_nivel"] == 2]
    metadataRegion = metadataPlacePD[metadataPlacePD["categ_nivel"] == 3]
    metadataDistrict = metadataPlacePD[metadataPlacePD["categ_nivel"] == 4]
    metadataLocPD = metadataPlacePD[metadataPlacePD["categ_nivel"] == 5]

    # fully self merge the table to get all nuts categories in flattened
    location_treatment(
        metadataTreat, metadataC, metadataRegion, metadataDistrict, metadataLocPD
    )
    type_treatment(metadataTypePD, metadataCrimesTreat)


def type_treatment(metadataTypePD: pandas.DataFrame, metadataCrimesTreat: str):
    metadataTypePD.rename(
        columns={"cat_id": "crimeID", "categ_dsg": "crimeName"}, inplace=True
    )
    metadataTypePD.reset_index(inplace=True)
    metadataTypePD.index.rename("crimeKey", inplace=True)
    metadataTypePD[["crimeID", "crimeName"]].to_csv(metadataCrimesTreat)


def location_treatment(
    metadataTreat,
    metadataC: pandas.DataFrame,
    metadataRegion: pandas.DataFrame,
    metadataDistrict: pandas.DataFrame,
    metadataLocPD: pandas.DataFrame,
):
    print(len(metadataLocPD.columns))

    metadataLocPD.loc[9999] = [None] * len(metadataLocPD.columns)
    metadataLocationTreat = pandas.merge(
        pandas.merge(
            pandas.merge(
                metadataLocPD, metadataDistrict, how="cross", suffixes=[None, "_4"]
            ),
            metadataRegion,
            how="cross",
            suffixes=[None, "_3"],
        ),
        metadataC,
        how="cross",
        suffixes=[None, "_2"],
    ).rename(
        columns={
            "cat_id": "locationID",
            "categ_dsg": "Location",
            "categ_dsg_4": "District",
            "categ_dsg_3": "Region",
            "categ_dsg_2": "Island",
        }
    )
    # remove all the rows where the nuts classifications don't correspond
    metadataLocationFinal = metadataLocationTreat[
        metadataLocationTreat.apply(
            lambda row: row["cat_id_3"].startswith(row["cat_id_2"])
            and row["cat_id_4"].startswith(row["cat_id_3"])
            and (
                row["locationID"].startswith(row["cat_id_4"])
                if row["locationID"]
                else row["locationID"] is None
            ),
            axis=1,
        )
    ]
    metadataLocationFinal.reset_index(inplace=True)
    metadataLocationFinal.index.rename("locationKey", inplace=True)
    metadataLocationFinal["Place"] = metadataLocationFinal["Location"].fillna(
        metadataLocationFinal["District"]
    )
    metadataLocationFinal["placeID"] = metadataLocationFinal["locationID"].fillna(
        metadataLocationFinal["cat_id_4"]
    )
    metadataLocationFinal[
        ["placeID", "Place", "Location", "District", "Region", "Island"]
    ].to_csv(metadataTreat)


def crime_treatment(
    dumpfile: str, treatfile: str, crimeTreatFile: str, locationTreatFile: str
):
    crimePd = pandas.read_csv(dumpfile)
    # Load treated metadata
    crimesMetadata = pandas.read_csv(crimeTreatFile)
    locationMetadata = pandas.read_csv(locationTreatFile)
    crimePd.rename(
        columns={
            "dim_3": "crimeID",
            "geocod": "NUTSid",
        },
        inplace=True,
    )

    resPD = crimePd.merge(crimesMetadata, how="left", on="crimeID").merge(
        locationMetadata, how="left", left_on="NUTSid", right_on="placeID"
    )
    resPD.index.rename("uniqueKey", inplace=True)
    resPD[["locationKey", "crimeKey"]].to_csv(treatfile)


metadata_tratment(
    "data/metadata.csv", "data/metadataTreat.csv", "data/metadataCrimesTreat.csv"
)
crime_treatment(
    "data/crimeData.csv",
    "data/crimeTreat.csv",
    "data/metadataCrimesTreat.csv",
    "data/metadataTreat.csv",
)
