from flask import Flask, render_template
import mariadb
import sys

app = Flask(__name__)
app.config["DEBUG"] = True


def load_db():
    try:
        conn = mariadb.connect(host="localhost", database="ocurrDW")
    except mariadb.Error as e:
        print(f"Error connecting {e}")
        sys.exit(1)
    return conn.cursor(), conn


# route to return all people
@app.route("/table/crimeFacts", methods=["GET"])
def tableread():
    cur, conn = load_db()
    cur.execute("select * from crimeFacts")

    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return render_template("table.html", headings=row_headers, data=rv)


@app.route("/table/crimeInfo", methods=["GET"])
def tableread2():
    cur, conn = load_db()
    cur.execute(
        "select uniqueKey, place, crimeName\
        from crimeFacts c inner join location l\
        on c.locationKey = l.locationKey\
        inner join crimeTypes t\
        on c.crimeKey = t.crimeKey"
    )

    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return render_template("table.html", headings=row_headers, data=rv)


@app.route("/table/crimeInfo", methods=["GET"])
def tablegrouplocation():
    cur, conn = load_db()
    cur.execute(
        "select place, count(*) as cnt\
        from crimeFacts c inner join location l\
        on c.locationKey = l.locationKey\
        group by place, order by cnt"
    )

    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return render_template("table.html", headings=row_headers, data=rv)


@app.route("/table/crimeInfo", methods=["GET"])
def tablegroupCrime():
    cur, conn = load_db()
    cur.execute(
        "select uniqueKey, place, crimeName\
        from crimeFacts c inner join location l\
        on c.locationKey = l.locationKey\
        inner join crimeTypes t\
        on c.crimeKey = t.crimeKey"
    )

    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return render_template("table.html", headings=row_headers, data=rv)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


app.run()
