import pandas


def crime_treatment(dumpfile: str, treatfile: str):
    crimePd = pandas.read_csv(dumpfile)
    crimePd = crimePd.drop(columns=["sinal_conv_desc", "sinal_conv", "valor"]).rename(
        columns={
            "dim_3": "CrimeId",
            "dim_3_t": "CrimeName",
            "geodsg": "NUTSName",
            "geocod": "NUTSid",
        }
    )
    crimePd.to_csv(treatfile)


def metadata_tratment(metadataDump: str, metadataTreat: str):
    metadataPd = pandas.read_csv(metadataDump)
    metadataPlacePD = metadataPd[metadataPd["dim_num"] == 2]
    # metadataCountry = metadataPlacePD[metadataPlacePD["categ_nivel"] == 1]
    metadataC = metadataPlacePD[metadataPlacePD["categ_nivel"] == 2]
    metadataRegion = metadataPlacePD[metadataPlacePD["categ_nivel"] == 3]
    metadataDistrict = metadataPlacePD[metadataPlacePD["categ_nivel"] == 4]
    metadataLocPD = metadataPlacePD[metadataPlacePD["categ_nivel"] == 5]

    # fully self merge the table to get all nuts categories in flattened
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
            "categ_dsg": "Name",
            "categ_dsg_4": "District",
            "categ_dsg_3": "Region",
            "categ_dsg_2": "Island",
        }
    )
    # remove all the rows where the nuts classifications don't correspond
    metadataLocationFinal = metadataLocationTreat[
        metadataLocationTreat.apply(
            lambda row: row["locationID"].startswith(row["cat_id_2"])
            and row["locationID"].startswith(row["cat_id_3"])
            and row["locationID"].startswith(row["cat_id_4"]),
            axis=1,
        )
    ]
    metadataLocationFinal[
        ["locationID", "Name", "District", "Region", "Island"]
    ].to_csv(metadataTreat)


metadata_tratment("data/metadata.csv", "data/metadataTreat.csv")
