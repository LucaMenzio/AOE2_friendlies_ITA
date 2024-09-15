import time
from threading import Semaphore
from time import sleep

import requests
from requests import RequestException

from modules.logging import logger


class ApiRateLimiter:
    """
    A class that manages API rate limits by restricting the number of requests
    that can be made per second. It uses a semaphore to limit the concurrency
    of the requests and automatically resets the rate limit every second.

    Attributes:
        max_calls_per_second (int): The maximum number of allowed API calls per second.
        semaphore (Semaphore): A semaphore to restrict the number of concurrent requests.
        last_reset_time (float): The last time the rate limit was reset.
    """

    def __init__(self, max_calls_per_second: int) -> None:
        """
        Initializes the ApiRateLimiter with a specified rate limit.

        Args:
            max_calls_per_second (int): The maximum number of allowed API calls per second.
        """
        self.max_calls_per_second = max_calls_per_second
        self.semaphore = Semaphore(max_calls_per_second)
        self.last_reset_time = time.time()

    def _check_rate_limit(self) -> None:
        """
        Resets the semaphore if a second has passed since the last reset, ensuring that
        the rate limit is enforced per second.
        """
        current_time = time.time()
        time_passed = current_time - self.last_reset_time

        # Check if one second has passed since the last reset
        if time_passed >= 1:
            # Reset the semaphore to allow up to max_calls_per_second new requests
            self.semaphore = Semaphore(self.max_calls_per_second)
            self.last_reset_time = current_time

    def make_request(self, url: str, **kwargs) -> None:
        """
        Makes a GET request to the given URL, ensuring that the rate limit is respected.

        Args:
            url (str): The URL to send the GET request to.
            **kwargs: Optional arguments that `requests.get` accepts.

        Prints:
            The HTTP response status code.

        Raises:
            Any exceptions raised by `requests.get`.
        """
        # Ensure the rate limit is checked before making the request
        self._check_rate_limit()
        # Acquire a semaphore token to proceed with the request
        self.semaphore.acquire()

        try:
            # Make the actual GET request to the given URL
            return self._make_request_attempts(url, **kwargs)
        finally:
            # Always release the semaphore token after the request is completed
            self.semaphore.release()

    def _make_request_attempts(
        self,
        url: str,
        max_attempts: int = 3,
        waiting_time: float = 3,
        **kwargs,
    ) -> None:
        """
        Attempts to make the GET request, retrying on failure.

        Args:
            url (str): The URL to send the GET request to.
            max_attempts (int): The maximum number of retry attempts (default is 3).
            waiting_time (float): The time in seconds to wait between retry attempts (default is 3 seconds).
            **kwargs: Optional arguments that `requests.get` accepts, such as headers or params.

        Returns:
            The JSON response from the API on success.

        Raises:
            RequestException: Propagates the exception after all retry attempts have failed.
        """
        attempt = 0
        while attempt < max_attempts:
            attempt += 1
            try:
                # Make the GET request with the provided arguments
                logger.info(f"Trying to call {url}")
                response = requests.get(url, **kwargs)
                response.raise_for_status()  # Raise an exception for any non-2xx status code
                return response.json()  # Return the JSON response
            except RequestException as e:
                logger.info(f"Attempt {attempt} failed. Error: {e}")
                if attempt < max_attempts:
                    # If there are remaining attempts, wait before retrying
                    logger.info(f"Retrying again in {waiting_time}")
                    sleep(waiting_time)
                else:
                    # If max_attempts are reached, propagate the exception
                    raise
