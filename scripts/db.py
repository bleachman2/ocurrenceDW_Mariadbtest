import mariadb
import sys


def load_db():
    try:
        conn = mariadb.connect(host="localhost", database="ocurrDW")
    except mariadb.Error as e:
        print(f"Error connecting {e}")
        sys.exit(1)
    return conn.cursor(), conn


def load_data():
    curr, conn = load_db()
    try:
        curr.execute(
            "CREATE TABLE IF NOT EXISTS crimes(\
            dim_3 VARCHAR(10),geodsg VARCHAR(30),geocod VARCHAR(10),\
            valor VARCHAR(10),sinal_conv_desc VARCHAR(30),\
            sinal_conv VARCHAR(10),dim_3_t VARCHAR(50))"
        )
        curr.execute(
            "LOAD DATA LOCAL INFILE 'data/crimeData.csv' \
            INTO TABLE crimes \
            FIELDS TERMINATED BY ',' IGNORE 1 ROWS"
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.close()


def first_load():
    curr, conn = load_db()
    try:
        # Location Metadata
        curr.execute(
            "CREATE TABLE IF NOT EXISTS location(\
            locationKey INTEGER\
            ,placeID INTEGER\
            ,Place VARCHAR(50)\
            ,Location VARCHAR(50)\
            ,District VARCHAR(30)\
            ,Region VARCHAR(30)\
            ,Island VARCHAR(30))"
        )
        curr.execute(
            "LOAD DATA LOCAL INFILE 'data/metadataTreat.csv'\
            INTO TABLE location \
            FIELDS TERMINATED BY ',' IGNORE 1 ROWS"
        )
        # crimes metadata
        curr.execute(
            "CREATE TABLE IF NOT EXISTS crimeTypes(\
            crimeKey INTEGER\
            ,crimeID VARCHAR(10)\
            ,crimeName VARCHAR(50))"
        )
        curr.execute(
            "LOAD DATA LOCAL INFILE 'data/metadataCrimesTreat.csv'\
            INTO TABLE crimeTypes \
            FIELDS TERMINATED BY ',' IGNORE 1 ROWS"
        )
        # Crimes Factless fact
        curr.execute(
            "CREATE TABLE IF NOT EXISTS crimeFacts(\
            uniqueKey INTEGER\
            ,locationKey INTEGER\
            ,crimeKey INTEGER)"
        )
        curr.execute(
            "LOAD DATA LOCAL INFILE 'data/crimeTreat.csv'\
            INTO TABLE crimeFacts \
            FIELDS TERMINATED BY ',' IGNORE 1 ROWS"
        )
        conn.commit()

    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.close()


first_load()
