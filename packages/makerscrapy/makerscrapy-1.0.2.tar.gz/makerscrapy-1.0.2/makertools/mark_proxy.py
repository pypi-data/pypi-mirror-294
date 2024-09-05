import requests



def get_aby_proxy() -> dict:
    ...


def get_ipdeal_proxy() -> dict:
    return {"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"}