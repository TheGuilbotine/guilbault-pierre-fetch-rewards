from flask import Flask
app = Flask(__name__)

database = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}

]

# example objects { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }


@app.route('/')
def balances():
    res = {}
    for data_column in database:
        res[data_column["payer"]] = data_column["points"]
    return res
