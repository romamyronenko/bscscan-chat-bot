from get_response import get_response


def get_contract_execution_status(txhash, api_key):
    query_params = {
        "module": "transaction",
        "action": "getstatus",
        "txhash": txhash,
        "apikey": api_key,
    }
    return get_response(query_params)


def get_transactions(
    address,
    api_key,
    start_block=None,
    end_block=None,
    page=None,
    offset=None,
    sort=None,
):
    query_params = {
        "module": "account",
        "action": "txlistinternal",
        "address": address,
        "startblock": start_block,
        "endblock": end_block,
        "page": page,
        "offset": offset,
        "apikey": api_key,
        "sort": sort,
    }

    return get_response(query_params)


def transactions_with_status_generator(
    address,
    api_key,
    start_block=None,
    end_block=None,
    page=None,
    offset=None,
    sort=None,
):
    transactions = get_transactions(
        address, api_key, start_block, end_block, page, offset, sort
    )

    for index, elem in enumerate(transactions):
        transactions[index]["contractExecutioStatus"] = get_contract_execution_status(
            elem["hash"], api_key
        )
        yield transactions[index]
