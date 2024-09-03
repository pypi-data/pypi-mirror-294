from datetime import datetime, timedelta
import user_agents
from typing import Dict, Optional

def date_is_within_hour(date_check: datetime) -> bool:
    """
    Checks if the given date and time is within the last hour.

    :param date_check: datetime object to check.
    :return: True if the date_check is within the last hour, False otherwise.
    """

    current_datetime = datetime.now()
    last_hour = current_datetime - timedelta(minutes=60)

    return last_hour <= date_check <= current_datetime


def parse_user_agent(ua_string: str) -> Dict[str, Optional[str]]:
    """
    Parses the user agent string and returns information about the browser, operating system, and device.

    :param ua_string: The user agent string to parse.
    :return: A dictionary with keys browserName, browserVersion, operatingSystem, osVersion, and device. Each key maps 
    to a string value or None if the information is not available. 
    """

    user_agent = user_agents.parse(ua_string)

    return {
        "browserName": user_agent.browser.family,
        "browserVersion": user_agent.browser.version_string,
        "operatingSystem": user_agent.os.family,
        "osVersion": user_agent.os.version_string,
        "device": user_agent.device.family,
    }
