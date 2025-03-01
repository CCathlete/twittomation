import time
from tweepy import OAuth1UserHandler, API, Tweet, errors  # type: ignore
from src.domain.entities.twitter import Tweet, Id
from typing_extensions import TypeAlias


class ApiClient:
    """
    An object that represents a user of the Twitter API.
    """

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Authentication (OAuth 1.0) since it's easier to imitate a
        # user.
        self.auth: OAuth1UserHandler = OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        self.api: API = API(self.auth)

    def _is_above_rate_limit(
        self,
    ) -> tuple[bool, int]:
        """
        Checking if we have reached the rate limit for a specific
        resource and endpoint, returning a tuple (bool, int):
            - (False, -1) if there are remaining requests.
            - (True, reset_time) if the rate limit is exceeded.
        """
        above_limit: bool = False
        reset_time: int = -1
        response_headers: dict[str, str] = self.api.last_response.headers
        # Checking the headers from the last api call. If there was no
        # last api call, we assume that the rate limit is not
        # exceeded.
        if response_headers:
            # we're using the dict.get method to avoid KeyError
            # exceptions using default values.
            remaining_requests: int = int(
                response_headers.get("x-rate-limit-remaining", 1),
            )  # If default value was used or remaining requests != 0
            # We'll skip the next condition and return
            # above_limit, reset_time == False, -1

            if remaining_requests == 0:
                above_limit = True
                reset_time = int(
                    response_headers.get(
                        "x-rate-limit-reset",
                        time.time(),
                    ),
                )  # We'll return above_limit, reset_time ==
                # True, reset_time
        else:
            print(
                "No last response available\n",
                "[INFO] Assuming rate limit not exceeded.",
            )  # above_limit, reset_time == False, -1

        return above_limit, reset_time

    def _wait_for_rate_limit_reset(
        self,
        reset_time: int,
    ) -> None:
        """
        Waits for the rate limit to reset.
        """
        # Using max to avoid negative wait times.
        wait_time: float = max(0, reset_time - time.time())
        print(
            "Rate limit exceeded.",
            f" Waiting for {wait_time:.2f} seconds.",
        )
        time.sleep(wait_time)

    def like_tweet(
        self,
        tweet: Tweet,
        retries: int = 3,
    ) -> bool:
        """
        Handles the action of liking a tweet, with retries if
        rate-limited.

        Args:
            tweet (Tweet): The tweet to like.
            retries (int): Number of retry attempts if the request fails.

        Returns:
            - True if the tweet was liked successfully.
            - False if an error occurred after all retries.
        """
        attempts_left: int = retries + 1
        current_attempt: int = 1
        above_limit: bool
        reset_time: int
        while attempts_left > 0:
            attempts_left -= 1
            above_limit, reset_time = self._is_above_rate_limit()
            if above_limit:
                self._wait_for_rate_limit_reset(reset_time)

            try:
                self.api.create_favorite(id=tweet.tweet_id)
                return True
            except errors.TweepyException as e:
                print(
                    f"Attempt to like tweet {tweet.tweet_id}",
                    f"failed, {attempts_left}",
                    f"attempts left: {e}",
                )
                if attempts_left > 0:
                    # If we were above rate limit, waited, tried to
                    # like and it failed, we#ll implement exponential
                    # backoff.
                    time.sleep(2 ** (current_attempt))
                    current_attempt += 1

        return False

    def unlike_tweet(
        self,
        tweet: Tweet,
        retries: int = 3,
    ) -> bool:
        """
        Handles the action of unliking a tweet, with retries if
        rate-limited.

        Args:
            tweet (Tweet): The tweet to unlike.
            retries (int): Number of retry attempts if the request fails.

        Returns:
            - True if the tweet was unliked successfully.
            - False if an error occurred after all retries.
        """
        # TODO: Add a check if the tweet is liked, otherwise there's
        # no need for unliking and we can return True
        attempts_left: int = retries + 1
        current_attempt: int = 1
        above_limit: bool
        reset_time: int
        while attempts_left > 0:
            attempts_left -= 1
            above_limit, reset_time = self._is_above_rate_limit()
            if above_limit:
                self._wait_for_rate_limit_reset(reset_time)

            try:
                self.api.destroy_favorite(id=tweet.tweet_id)
                return True
            except errors.TweepyException as e:
                print(
                    f"Attempt to unlike tweet {tweet.tweet_id}",
                    f"failed, {attempts_left}",
                    f"attempts left: {e}",
                )
                if attempts_left > 0:
                    # If we were above rate limit, waited, tried to
                    # unlike and it failed, we'll implement
                    # exponential backoff.
                    time.sleep(2 ** (current_attempt))
                    current_attempt += 1

        return False

    def get_tweet_by_id(
        self,
        tweet_id: Id,
    ) -> dict[str, str]:
        """
        Checking if we have reached the rate limit for a specific
        resource and endpoint, returning a tuple (bool, int):
        - bool: True if rate limit exceeded, False otherwise
        - int: The reset time if rate limit exceeded, 0 if not
        """
        tweet_data: dict[str, str]
        return tweet_data
