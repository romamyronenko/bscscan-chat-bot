import requests


def get_response(query_params):
    query_params = {k: v for k, v in query_params.items() if v is not None}

    response = requests.get(f"https://api-testnet.bscscan.com/api", params=query_params)
    if response.json().get("status") != "1":
        raise Exception("something wrong")
    return response.json().get("result")
