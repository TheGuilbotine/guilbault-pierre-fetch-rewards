TRANSACTIONS = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}
]

BALANCES = {}


def make_balances(transactions):
    for transaction in transactions:
        if transaction["payer"] in BALANCES:
            BALANCES[transaction["payer"]]["points"] += transaction["points"]
        else:
            BALANCES[transaction["payer"]] = {
                "payer": transaction["payer"], "points": transaction["points"]}
        print(BALANCES)


make_balances(TRANSACTIONS)
