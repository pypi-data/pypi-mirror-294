import time
import threading

class RateLimiter:
    def __init__(self, max_requests, time_window):
        """
        Initialize the rate limiter.

        :param max_requests: The maximum number of requests allowed within the time window.
        :param time_window: The time window in seconds.
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_count = 0
        self.lock = threading.Lock()
        self.reset_time = time.time()

    def allow_request(self):
        """
        Check if the rate limit has been exceeded. Returns True if the request is allowed, False otherwise.
        """
        with self.lock:
            current_time = time.time()
            if current_time - self.reset_time > self.time_window:
                self.request_count = 0
                self.reset_time = current_time
            if self.request_count < self.max_requests:
                self.request_count += 1
                return True
            else:
                return False

    def reset(self):
        """
        Reset the rate limiter.
        """
        with self.lock:
            self.request_count = 0
            self.reset_time = time.time()
