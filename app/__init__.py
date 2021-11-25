from datetime import datetime, timezone
from flask import Flask, request
app = Flask(__name__)

TRANSACTIONS = [
    # {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    # {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    # {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    # {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    # {"payer": "MILLER COORS", "points": 10000,
    #     "timestamp": "2020-11-01T14:00:00Z"},
    # {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
]

BALANCES = {}


def make_balance(transaction):
    if transaction["payer"] not in BALANCES:
        BALANCES[transaction["payer"]] = {
            "payer": transaction["payer"], "points": transaction["points"]}
        print(
            f'{transaction["payer"]} has been added to Balances with {transaction["points"]} points.')
    else:
        negativeCheck = BALANCES[transaction["payer"]
                                 ]["points"] + transaction["points"]
        if negativeCheck < 0:
            print(
                f'Subtracting that amount will leave points from {transaction["payer"]} in the negative. Unable to process.')
            # exit so that negative amount not shown.
            return
        else:
            BALANCES[transaction["payer"]]["points"] += transaction["points"]
            print(
                f'{transaction["payer"]} has been added to Balances with {transaction["points"]} points.')
    return {"payer": transaction["payer"], "points": transaction["points"]}


@app.route('/')
def balances():
    """
    Returns all current balances
    """
    res = {}
    if BALANCES == {}:
        return "Currently no balances."
    else:
        for key in BALANCES:
            res[BALANCES[key]["payer"]] = BALANCES[key]["points"]
        return res

# transaction


@app.route('/', methods=['POST'])
def catch_points():
    """
    Adds points from a specific payer and at a specific time
    """
    data = request.get_json()
    payer = data["payer"]
    points = data["points"]
    utcDate = datetime.now(timezone.utc)
    timestamp = utcDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    newTransaction = {"payer": payer, "points": points,
                      "timestamp": timestamp}
    TRANSACTIONS.append(newTransaction)
    make_balance(newTransaction)

    return newTransaction, 201

# spend_points


@app.route('/', methods=['PUT'])
def throw_points():
    """
    Spends points in total from each of the oldest transaction timestamps until points are spent
    """
    data = request.get_json()
    totalPointsToSpend = data["points"]
    pointsSpent = 0
    orderedTransactions = [*TRANSACTIONS]
    orderedTransactions.sort(
        key=lambda transaction: transaction['timestamp'])
    for transaction in orderedTransactions:
        # for balance in BALANCES:
        #     #  and balance["points"] >= transaction["points"]
        #     if balance["payer"] == transaction["payer"]:
        if totalPointsToSpend != pointsSpent:
            BALANCES[transaction["payer"]]["points"] -= transaction["points"]
            pointsSpent += transaction["points"]
        else:
            return f"All points spent current balances are {BALANCES}", 201
    # return {BALANCES}, 201

    # if pointsLeft > 0:
    #     for transaction in orderedTransactions:
    #         pointsLeft = pointsLeft - transaction["points"]
    #         for balance in BALANCES:
    #             if balance["payer"] == transaction["payer"]:
    #                 prevBalance = balance["points"]
    #                 if prevBalance < totalPointsToSpend:
    #                     balance["points"] = prevBalance - transaction["points"]
    #                 else:
    #                     balance["points"] = prevBalance - totalPointsToSpend
    # else:
    #     print(f"All points have been spent. New balances are {BALANCES}")
    # return f"Successfully spent points, balances are as follows{BALANCES}", 201
