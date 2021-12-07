from flask import Flask, request


app = Flask(__name__)

TRANSACTIONS = []

BALANCES = {}

'''
make_balances function
Creates a balance or adds points to a balance in the BALANCES dictionary
@param {dictionary} transaction will be the transaction from a request made to the / GET route
@return {dictionary} a dictionary with payer and points keys pointing to those of the transaction

it will check if the transaction payer exists in BALANCES
if it is not it will create a key with that payers name pointing to a dictionary with the payer and points
otherwise it will add the points from the new transaction to the existing balance points for that payer
'''


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
    # response to return
    res = {}
    # check for balances
    if BALANCES == {}:
        return "Currently no balances."
    else:
        for key in BALANCES:
            # add each balance to the res to return a dictionary of all balances
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


@app.route('/transaction', methods=['POST'])
def catch_points():
    """
    Adds points from a specific payer and at a specific time
    """
    data = request.get_json()
    payer = data["payer"]
    points = data["points"]
    timestamp = data["timestamp"]
    newTransaction = {"payer": payer, "points": points, "points_spent": 0,
                      "timestamp": timestamp}
    TRANSACTIONS.append(newTransaction)
    make_balance(newTransaction)

    return newTransaction, 201


@app.route('/spend_points', methods=['PUT'])
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

                if BALANCES[transaction["payer"]]["points"] != 0 and transaction["points_spent"] != transaction["points"]:
                    if pointsToSpend <= BALANCES[transaction["payer"]]["points"]:
                        transaction["points_spent"] += pointsToSpend
                    else:
                        transaction["points_spent"] = transaction["points"]

                    if (BALANCES[transaction["payer"]]["points"] - pointsToSpend) >= 0:
                        BALANCES[transaction["payer"]
                                 ]["points"] -= pointsToSpend
                        pointsSpent += pointsToSpend
                    else:
                        balanceLeft = BALANCES[transaction["payer"]]["points"]
                        pointsSpent += balanceLeft
                        BALANCES[transaction["payer"]]["points"] = 0

    return f"All points spent current balances are {BALANCES}", 201
