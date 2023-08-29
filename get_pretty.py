def get_pretty(transaction_data: dict, tab=0) -> str:
    retval = ""
    for k, v in transaction_data.items():
        if isinstance(v, str):
            retval += "    " * tab + f"{k}: {v}\n"
        if isinstance(v, dict):
            retval += f"{k}:\n"
            retval += get_pretty(v, tab + 1)
    return retval
