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

    def like_tweet(self, tweet: Tweet) -> bool:
        """
        Handles the action of liking a tweet.
        """
        success: bool

        return success

    def unlike_tweet(self, tweet: Tweet) -> bool:
        """
        Handles the action of unliking a tweet.
        """
        success: bool

        return success

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
