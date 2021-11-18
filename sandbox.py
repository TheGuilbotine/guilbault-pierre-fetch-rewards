TRANSACTIONS = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
]

BALANCES = []


# def make_balances(transaction):
#     for transaction in transactions:
#         if transaction["payer"] in BALANCES:
#             BALANCES[transaction["payer"]]["points"] += transaction["points"]
#         else:
#             BALANCES[transaction["payer"]] = {
#                 "payer": transaction["payer"], "points": transaction["points"]}
#     print(BALANCES)

def make_balance(transaction):
    print(BALANCES)
    if len(BALANCES) == 0:
        BALANCES.append(transaction)
    else:
        for balance in BALANCES:
            if balance["payer"] == transaction["payer"]:
                balance["points"] += transaction["points"]
            else:
                print("didnt exist")
                BALANCES.append(transaction)
    print(BALANCES)
    return {"payer": transaction["payer"], "points": transaction["points"]}


# make_balances(TRANSACTIONS)
print(make_balance({"payer": "DANNON", "points": 1000,
                    "timestamp": "2020-11-02T14:00:00Z"}))
print(make_balance({"payer": "DANNON", "points": 1000,
                    "timestamp": "2020-11-02T14:00:00Z"}))
print(make_balance(
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"}))
# print(BALANCES)
