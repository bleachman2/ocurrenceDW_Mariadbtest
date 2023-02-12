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
