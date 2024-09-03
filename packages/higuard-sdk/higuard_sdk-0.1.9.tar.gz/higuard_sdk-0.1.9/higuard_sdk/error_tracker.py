class ErrorTracker:
    def __init__(self, max_age: int):
        """
        Initialize error tracker

        :param max_age: How long the error should be stored in memory (in milliseconds).
        """
        self.error_tracker = {}
        self.max_age = max_age

    def duplicate_check(self, message:str, timestamp:int) -> bool:
        """
        Check to see if an error is a duplicate.
        
        :param message: Error message
        :param timestamp: Timestamp of the error
        :return: Retruns true if duplicate error found
        """
    
        if message in self.error_tracker:
            timestamps = self.error_tracker[message]
            if timestamps:
                last_timestamp = timestamps[-1]
                if timestamp - last_timestamp < self.max_age:
                    return True
        return False
    
    def add_timestamp(self, message:str, timestamp: int) -> None:
        """
        Adds a timestamp to the error tracker directory

        :param message: Error message title.
        :param timestamp: Timestamp of the error (UNIX)
        """

        if message not in self.error_tracker:
            self.error_tracker[message] = []
        self.error_tracker[message].append(timestamp)

    def clean_old_timestamps(self, current_timestamp:int) -> None:
        """
        Cleans up old timestamps from the error tracker dictionary

        :param current_timestamp: Current date timestamp (UNIX)
        """
        for error_msg, timestamps in list(self.error_tracker.items()):
            self.error_tracker[error_msg] = [
                ts for ts in timestamps if current_timestamp - ts <= self.max_age
            ]
            if not self.error_tracker[error_msg]:
                del self.error_tracker[error_msg]
