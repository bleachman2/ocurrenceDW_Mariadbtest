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


load_data()
