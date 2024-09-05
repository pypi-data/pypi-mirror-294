import requests


def ping_google() -> bool:
    """
    Ping Google to check it is reachable

    :return:
    """

    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


ping_google()