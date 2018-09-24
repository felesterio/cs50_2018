import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles")
def articles():
    """Look up articles for geo"""
    # array of dicts with keys 'link' and 'title'

    # get form info
    location = request.args.get("geo")

    # if text missing, raise RuntimeError
    if not location:
        raise RuntimeError("Geo not set")

    articles = lookup(location)

    # return up to 5 articles
    return jsonify(articles[:5])


@app.route("/search")
def search():
    """Search for places that match query"""

    # parses querie into key word array
    q = request.args.get("q")

    # parases query into an array
    q_array = q.split(" ")

    # remove any commas (if any)
    query = []
    for item in q_array:
        if item[len(item) - 1] == ",":
            item = item.replace(",", "")
            query.append(item)
        else:
            query.append(item)

    # Finds postal code, city and state that start within q
    results = db.execute(
        "SELECT * FROM places WHERE country_code LIKE :q OR postal_code LIKE :q OR place_name LIKE :q OR admin_name1 LIKE :q OR admin_code1 LIKE :q OR admin_name2 LIKE :q OR admin_code2 LIKE :q OR latitude LIKE :q OR longitude LIKE :q", q=query[0])

    # for each word in query, search whole database results and find overlapping search results from other word queries
    for i in range(1, len(query)):
        results_cmp = db.execute(
            "SELECT * FROM places WHERE country_code LIKE :q OR postal_code LIKE :q OR place_name LIKE :q OR admin_name1 LIKE :q OR admin_code1 LIKE :q OR admin_name2 LIKE :q OR admin_code2 LIKE :q OR latitude LIKE :q OR longitude LIKE :q", q=query[i])
        results = intersection(results, results_cmp)

    # returns results containing all word queries; if one keyword DNE in database, results will return empty set
    return jsonify(results)

# intersection of search query results
# credit for help from curiouskiwi from CS50 stackexchange


def intersection(a, b):
    s1 = set()
    s2 = set()

    # Convert dict objects to tuples and add to set
    for i in a:
        s1.add(tuple(i.items()))

    for i in b:
        s2.add(tuple(i.items()))

    result = []

    # Iterate over intersection of the two sets
    # Convert each tuple back to dict object
    # Append to result list
    for tup in (s1 & s2):
        result.append(dict(tup))

    return result


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
