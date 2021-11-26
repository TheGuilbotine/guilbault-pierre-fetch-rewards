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
    balancePoints = [BALANCES[key]["points"] for key in BALANCES]
    if totalPointsToSpend > sum(balancePoints):
        return "Points to spend exceeds total points in Balances."
    if len(TRANSACTIONS) == 0:
        return "There are no Transactions", 102
    elif all(points == 0 for points in balancePoints):
        return "All balances are at zero.", 403
    else:
        for transaction in orderedTransactions:
            if totalPointsToSpend != pointsSpent and transaction["points"] >= 0:
                pointsLeft = totalPointsToSpend - pointsSpent
                if transaction["points"] >= pointsLeft:
                    pointsToSpend = pointsLeft
                else:
                    pointsToSpend = transaction["points"]
                if BALANCES[transaction["payer"]
                            ]["points"] != 0 and (BALANCES[transaction["payer"]]["points"] - pointsToSpend) >= 0:
                    BALANCES[transaction["payer"]
                             ]["points"] -= pointsToSpend
                    pointsSpent += pointsToSpend
                else:
                    pointsSpent + BALANCES[transaction["payer"]]["points"]
                    BALANCES[transaction["payer"]]["points"] = 0
    return f"All points spent current balances are {BALANCES}", 201
