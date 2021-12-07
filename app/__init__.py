from datetime import datetime, time, timezone
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


@app.route('/transactions')
def transactions():
    """
    Returns all transactions
    """
    res = {}
    if TRANSACTIONS == []:
        return "There have been no transactions."
    else:
        for transaction in TRANSACTIONS:
            res[len(res) + 1] = {"payer": transaction["payer"], "points": transaction["points"],
                                 "points_spent": transaction["points_spent"], "timestamp": transaction["timestamp"]}
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
    # timestamp will be coming in
    # turn sting into datetime
    # needs something like this "2021-11-06T19:36:00Z"
    timestamp = data["timestamp"]
    utcDate = datetime.now(timezone.utc)
    # timestamp = utcDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(type(timestamp))
    newTransaction = {"payer": payer, "points": points, "points_spent": 0,
                      "timestamp": timestamp}
    TRANSACTIONS.append(newTransaction)
    make_balance(newTransaction)

    return newTransaction, 201

# spend_points

# some how the amount to spend stays the same and will subtract that full amount from the next balance if it excedes the amount of the previous balance.


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
            if totalPointsToSpend != pointsSpent and transaction["points"] >= 0 and transaction["points_spent"] < transaction["points"]:
                pointsLeft = totalPointsToSpend - pointsSpent
                pointsToSpend = min(pointsLeft, transaction["points"])
                # if transaction["points"] >= pointsLeft:
                #     pointsToSpend = pointsLeft
                # else:
                #     pointsToSpend = transaction["points"]
                if BALANCES[transaction["payer"]]["points"] != 0 and transaction["points_spent"] != transaction["points"]:
                    if pointsToSpend <= BALANCES[transaction["payer"]]["points"]:
                        transaction["points_spent"] += pointsToSpend
                    else:
                        transaction["points_spent"] = transaction["points"]
                    # if transaction["points_spent"] == 0 and transaction["points"] <= BALANCES[transaction["payer"]]["points"]:
                    #     transaction["points_spent"] = pointsToSpend
                    # elif transaction["points"] > transaction["points_spent"] and transaction["points"] < BALANCES[transaction["payer"]]["points"]:
                    #     transaction["points_spent"] == (
                    #         transaction["points"] - transaction["points_spent"]) + transaction["points_spent"]
                    # elif transaction["points_spent"] == 0 and transaction["points"] > BALANCES[transaction["payer"]]["points"]:
                    #     transaction["points_spent"] = BALANCES[transaction["payer"]]["points"]
                    # elif transaction["points"] > transaction["points_spent"] and transaction["points"] > BALANCES[transaction["payer"]]["points"] and BALANCES[transaction["payer"]]["points"] + transaction["points_spent"] <= transaction["points"]:
                    #     transaction["points_spent"] = BALANCES[transaction["payer"]]["points"]
                    # elif transaction["points"] > transaction["points_spent"] and transaction["points"] > BALANCES[transaction["payer"]]["points"] and BALANCES[transaction["payer"]]["points"] + transaction["points_spent"] > transaction["points"]:
                    #     transaction["points_spent"] = transaction["points"]
                    # need to check transaction vs balances because balances will be greater than a transacion at times.
                    # if BALANCES[transaction["payer"]]["points"] == pointsToSpend and transaction["points"] == pointsToSpend:
                    #     transaction["points_spent"] = pointsToSpend
                    # elif BALANCES[transaction["payer"]]["points"] > pointsToSpend and transaction["points"] == pointsToSpend:
                    #     transaction["points_spent"] = transaction["points"] - \
                    #         pointsToSpend
                    # else:
                    #     transaction["points_spent"] = pointsToSpend - \
                    #         BALANCES[transaction["payer"]]["points"]

                    if (BALANCES[transaction["payer"]]["points"] - pointsToSpend) >= 0:
                        BALANCES[transaction["payer"]
                                 ]["points"] -= pointsToSpend
                        pointsSpent += pointsToSpend
                    else:
                        balanceLeft = BALANCES[transaction["payer"]]["points"]
                        pointsSpent += balanceLeft
                        BALANCES[transaction["payer"]]["points"] = 0

    return f"All points spent current balances are {BALANCES}", 201
