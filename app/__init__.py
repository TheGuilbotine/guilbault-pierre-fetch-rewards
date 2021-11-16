from datetime import datetime, time
from flask import Flask, request
# from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
# api = Api(app)

TRANSACTIONS = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
]


# def make_balances(transactions):
#     for transaction in transaction:
#         if BALANCES[""]


BALANCES = []

# if __name__ == "__main__":
#     app.run(debug=True)

# example objects { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }


@app.route('/')
def balances():
    """
    Returns all current balances
    """
    res = {}
    for data_column in TRANSACTIONS:
        res[data_column["payer"]] = data_column["points"]
    return res


@app.route('/transaction', methods=['POST'])
def catch_points():
    print("YOU ARE IN THE transaction route")
    """
    Adds points from a specific payer and at a specific time
    """
    data = request.get_json()
    # return data["payer"], 201
    payer = data["payer"]
    points = data["points"]
    timestamp = datetime.utcnow()
    newTransaction = {"payer": payer, "points": points, "timestamp": timestamp}
    TRANSACTIONS.append(newTransaction)
    print(TRANSACTIONS)
    return newTransaction, 201


@app.route('/spend_points', methods=['POST'])
def throw_points():
    """
    Spends points in total from each of the most recent transaction times until points are spent
    """
    pass


# Do these need to be a PUT methods? Spend points should be I think. Will I also need to use forms?
