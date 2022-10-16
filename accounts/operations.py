"""accounts operations"""


def get_transactions_queryset(transactions, params):
    transactions = transactions.filter(monthlybill=None)
    category = params.get("category", None)
    filter_type = params.get("type", None)
    if category is not None:
        transactions = transactions.filter(category=category)
    if filter_type is not None:
        transactions = transactions.filter(type=filter_type)

    return transactions
