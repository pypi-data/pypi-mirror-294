from typing import Optional

class Configs:
    def __init__(self,
                 verbose: bool=False,
                 samping_rate: int=2,
                 max_age: int = 20000,
                 retry_delay: int = 3000,
                 retry_attempts: int =3):
        
        """
        Initilization of the Configs class with either default or specified settings.

        :param vervose: Enable verbose output for logging. Default is false.
        :param sampling_rate: The rate at which to sample event or requests. Default is 2.
        :param max_age: The maximum age (in milliseconds) that an error should be kept in memory. Default is 20000.
        :param retry_delay: The delay (in milliseconds) between retry attempts. Default is 3000.
        :param retry_attempts: The number of retry attempts allowed. Default is 3.
        """
        self.verbose = verbose
        self.samping_rate = samping_rate
        self.max_age = max_age
        self.retry_delay = retry_delay
        self.retry_attempts = retry_attempts


class Configuration:
    def __init__(self, configs:Optional[Configs] = None):
        """
        Initializes Configuration class to store and manage configuration settings. If none are given, default settings will be used.

        :param configs: An optional Configs object.
        """

        default_configs = Configs()
        self.configs = configs if configs else default_configs

    def get_config(self, key:str) -> Optional[int]:
        """
        Retrieves the value of the specificed configuration setting.

        :param key: The name of the configuration setting to retrieve.
        :return: The value of the configurationi setting, or None if the setting does not exist.
        """

        return getattr(self.configs, key, None)
    
    def set_config(self, key:str, value) -> None:
        """
        Sets the value of the specified configuration setting, with validation.

        :param key: The name of the configuration setting to set.
        :param value: The value to assign to the configuration setting.
        :raises ValueError: If the value is not valid for the specified setting. 
        """
        
        if key == "sampling_rate" and value <= 0:
            raise ValueError("sampling_rate must be a positive number")
        if key == "max_age" and value <= 0:
            raise ValueError("max_age must be a positive number")
        if key == "retry_delay" and value <= 0:
            raise ValueError("retry_delay must be a positive number")
        if key == "retry_attempts" and value <= 0:
            raise ValueError("retry_attempts must be a positive number")
        setattr(self.configs, key, value)
