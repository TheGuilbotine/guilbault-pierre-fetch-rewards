from datetime import datetime, time, timezone
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

BALANCES = []


def make_balance(transaction):
    if len(BALANCES) == 0:
        print(
            f'{transaction["payer"]} has been added to Balances with {transaction["points"]} points.')
        BALANCES.append(transaction)
    else:
        for balance in BALANCES:
            if balance["payer"] == transaction["payer"]:
                negativeCheck = balance["points"] + transaction["points"]
                if negativeCheck < 0:
                    print(
                        f'Subtracting that amount will leave points from {transaction["payer"]} in the negative. Unable to process.')
                    # exit so that negative amount not shown.
                    return
                else:
                    balance["points"] = balance["points"] + \
                        transaction["points"]
            else:
                print(
                    f'{transaction["payer"]} has been added to Balances with {transaction["points"]} points.')
                BALANCES.append(transaction)
    return {"payer": transaction["payer"], "points": transaction["points"]}


# if __name__ == "__main__":
#     app.run(debug=True)

# example objects { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }


@app.route('/')
def balances():
    """
    Returns all current balances
    """
    res = {}
    for data_column in BALANCES:
        res[data_column["payer"]] = data_column["points"]
    return res


@app.route('/transaction', methods=['POST'])
def catch_points():
    """
    Adds points from a specific payer and at a specific time
    """
    data = request.get_json()
    # return data["payer"], 201
    payer = data["payer"]
    points = data["points"]
    utcDate = datetime.now(timezone.utc)
    timestamp = utcDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    newTransaction = {"payer": payer, "points": points,
                      "timestamp": timestamp}
    TRANSACTIONS.append(newTransaction)
    make_balance(newTransaction)

    print(TRANSACTIONS)
    print(BALANCES)
    return newTransaction, 201


@app.route('/spend_points', methods=['PUT'])
def throw_points():
    """
    Spends points in total from each of the oldest90 transaction times until points are spent
    """
    data = request.get_json()
    print(data)
    totalPointsToSpend = data["points"]
    pointsSpent = data["points"]
    orderedTransactions = [*TRANSACTIONS]
    orderedTransactions.sort(
        key=lambda transaction: transaction['timestamp'])
    if pointsSpent > 0:
        for transaction in orderedTransactions:
            pointsRemainingBefore = pointsSpent
            pointsSpent -= transaction["points"]
            pointsRemainingAfter = pointsSpent
            for balance in BALANCES:
                if balance["payer"] == transaction["payer"]:
                    balance["points"] = balance["points"] - pointsSpent
                    # (pointsRemainingBefore - pointsRemainingAfter)
    else:
        print(f"All points have been spent. New balances are {BALANCES}")
    return f"Successfully spent points, balances are as follows{BALANCES}", 201


# Do these need to be a PUT methods? Spend points should be I think. Will I also need to use forms?
