import requests
from time import sleep
from typing import Dict


def error_dashboard_fetch(
        client_secret: str,
        client_id: str,
        method: str,
        endpoint: str,
        body: dict = None,
        headers: dict = None,
        retry_attempts: int = 3,
        retry_delay: int = 3000
) -> Dict[str, bool]:
    """
    Fetch function to send errors to the dashboard server with retry mechanism.

    :param client_secret: Client secret for the dashboard server.
    :param client_id: Client ID for the dashboard server.
    :param method: HTTP method to be used.
    :param headers: Additional headers to be sent.
    :param endpoint: Endpoint to send the data.
    :param body: Body of the request.
    :param retry_attempts: Number of retry attempts.
    :param retry_delay: Delay between retry in milliseconds.
    :return: Returns a dictionary with either isError or isSuccess

    """

    is_error = False
    is_success = False

    if not headers:
        headers = {}

    headers.update({
        "Content-Type": "application/json",
        "client_secret": client_secret,
        "client_id": client_id
    })

    for attempt in range(retry_attempts):
        try:
            if method.upper() == "POST":
                response = requests.post(endpoint, json=body, headers=headers)
            elif method.upper() == "GET":
                response = requests.get(endpoint, headers=headers, params=body)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 200:
                is_success = True
                return {"isSuccess": is_success, "isError": is_error}
            else:
                is_error = True
        except requests.exceptions.RequestException as e:
            print(f"Fetch error: {e}")
            is_error = True

        if attempt < retry_attempts - 1:
            sleep(retry_delay / 1000.0)

    return {"isSuccess": is_success, "isError": is_error}
