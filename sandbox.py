from datetime import datetime, time, timezone
from operator import attrgetter
TRANSACTIONS = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
]

BALANCES = []

# now = datetime.utcnow()
# oldestTransaction = TRANSACTIONS[0]
# oldestTimestamp = min(dt["timestamp"] for dt in TRANSACTIONS)
# for transaction in TRANSACTIONS:
#     if transaction["timestamp"] < oldestTimestamp:
#         oldestTransaction = transaction
#     print(oldestTransaction)


def get_timestamp(obj):
    return obj["timestamp"]


orderedTransactions = [*TRANSACTIONS]
# print(TRANSACTIONS)
orderedTransactions.sort(
    key=lambda transaction: transaction['timestamp'], reverse=True)
print(orderedTransactions)

# def make_balances(transaction):
#     for transaction in transactions:
#         if transaction["payer"] in BALANCES:
#             BALANCES[transaction["payer"]]["points"] += transaction["points"]
#         else:
#             BALANCES[transaction["payer"]] = {
#                 "payer": transaction["payer"], "points": transaction["points"]}
#     print(BALANCES)


def make_balance(transaction):
    if len(BALANCES) == 0:
        print(
            f'{transaction["payer"]} has been added to your Balances with {transaction["points"]} points.')
        BALANCES.append(transaction)
    else:
        for balance in BALANCES:
            if balance["payer"] == transaction["payer"]:
                negativeCheck = balance["points"] + transaction["points"]
                if negativeCheck < 0:
                    print(
                        f'Subtracting that amount will leave your points from {transaction["payer"]} in the negative. Unable to process.')
                    # exit so that negative amount not shown.
                    return
                else:
                    balance["points"] += transaction["points"]
            else:
                print(
                    f'{transaction["payer"]} has been added to your Balances with {transaction["points"]} points.')
                BALANCES.append(transaction)
    return {"payer": transaction["payer"], "points": transaction["points"]}


# make_balances(TRANSACTIONS)
# print(make_balance({"payer": "DANNON", "points": 1000,
#                     "timestamp": "2020-11-02T14:00:00Z"}))
# print(make_balance({"payer": "DANNON", "points": -1001,
#                     "timestamp": "2020-11-02T14:00:00Z"}))
# print(make_balance(
#     {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"}))
