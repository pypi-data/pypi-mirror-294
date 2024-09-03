import time
import requests
from threading import Timer
from typing import List, Optional
from .environment import base_url
from .configs import Configuration
from .error_tracker import ErrorTracker


class ErrorDashboardClient:
    _instance = None

    def __init__(self, client_id: str, client_secret: str, configs: Optional[Configuration] = None):
        """
        Initializes ErrorDashboardclient with the given client ID, client secret, and configurations.

        :param: client_id: Client ID for authentication.
        :param: client_Secret: Client secret for authentication.
        :param: configs: Configuration settings for the client. If not provided, default settings will be used.
        :param: base_url: The base URL for the dashboard server.
        :param: error_tracker: An instance of ErrorTracker to track errors.
        :param: _setup_periodic_cleanup: A method to set up periodic cleanup of old timestamps.
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.configs = configs if configs else Configuration()
        self.base_url = base_url
        self.error_tracker = ErrorTracker(self.configs.get_config("max_age"))
        self._setup_periodic_cleanup()

    @classmethod
    def initialize(cls, client_id: str, client_secret: str):
        """
        Initialize and returns single instance of ErrorDashboardClient

        :param: client_id: Client ID for authentication.
        :param: client_secret: Client secret for authentication.
        :return: Returns the single instance of ErrorDashboardClient.
        """

        if cls._instance is None:
            cls._instance = cls(client_id, client_secret)
            return cls._instance

    def _setup_periodic_cleanup(self):
        """
        Sets up a periodic cleanup that removes old timestamps from the error tracker based on the maximum age configuration.
        """

        max_age = self.configs.get_config('max_age')
        self.timer = Timer(max_age / 1000.0, self._clean_old_timestamps)
        self.timer.start()

    def _clean_old_timestamps(self):
        """
        Cleans old timestamps from the error tracker. Called periodically by the timer.
        """

        now = int(time.time() * 1000)
        self.error_tracker.clean_old_timestamps(now)
        self._setup_periodic_cleanup()

    def send_error(self, error: Exception, message: str, tags: Optional[List[str]] = None, attach_user: Optional[str] = None):
        """
        Sends an error to the dashboard server with message. 
        Checks for duplicate errors before sending the error, and retries based on configured attempts and delays.

        :param error: The exception object containing the error detials.
        :param message: The description about the error.
        :param tags: An optional list of tags to label the error.
        :param attach_user: An optional user identifier to attach to the error.
        """

        current_time = int(time.time() * 1000)

        if self.error_tracker.duplicate_check(message, current_time):
            if self.configs.get_config("verbose"):
                print("Duplicate error found, not sending to dashboard")
            return

        error_stack = str(error)
        user_affected = attach_user if attach_user else "N/A"
        retry_attempts = self.configs.get_config("retry_attempts")
        retry_delay = self.configs.get_config("retry_delay")

        error_request_body = {
            "userAffected": user_affected,
            "stackTrace": error_stack,
            "messsage": message,
            "tags": tags or [],
        }

        is_success = self._send_to_dashboard(
            error_request_body, retry_attempts, retry_delay)

        if is_success and self.configs.get_config('verbose'):
            print("Data sent to dashboard")
            self.error_tracker.add_timestamp(message, current_time)
        elif not is_success and self.configs.get_config('verbose'):
            print("Error sending data to dashboard")

    def _send_to_dashboard(self, payload, retry_attempts, retry_delay):
        """
        Sends error data to the dashboard server with aretry mechanism.

        :param payload: The data to be sent to the server.
        :param retry_attempts: Number of times to retry sending in case of failure.
        :param retry_delay: Delay between retries in milliseconds.
        :return: True if data was successfully sent, False otherwise.
        """

        url = f"{self.base_url}"

        headers = {
            "Authorization": self.client_secret,
            "Content-Type": "application/json",
            "client_id": self.client_id
        }

        for attempt in range(retry_attempts):
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    return True
                else:
                    print(
                        f"Error sending data to dashboard: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to dashboard: {e}")

            if attempt < retry_attempts - 1:
                time.sleep(retry_delay / 1000.0)
        return False

    @classmethod
    def override_configs(cls, new_configs: Configuration):
        """
        Overrides the current configuration settings with the provided new ones.

        :param new_configs: A dictionary of new configuration settings.
        :raises: Exception if ErrorDashboardClient is not initialized. 
        """

        if cls._instance is None:
            raise Exception(
                "ErrorDashboardClient not initialized, call initialize() first.")

        for key, value in new_configs.items():
            cls._instance.configs.set_config(key, value)
