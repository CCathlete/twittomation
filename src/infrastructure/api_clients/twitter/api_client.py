import time
from tweepy import (  # type: ignore
    OAuth1UserHandler,
    Client,
    Tweet,
    errors,
    Response,
)
from src.domain.entities.twitter import Tweet, Id
from typing import Optional


class ApiClient:
    """
    An object that represents a user of the Twitter Client.
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
        self.client: Client = Client(self.auth)

        # Storing request quotas per endpoint.
        # {endpoint: (remaining_requests, reset_time)}
        self.request_quotas: dict[str, tuple[int, int]] = {}

    def _update_request_quota(
        self,
        endpoint: str,
        response: Response,
    ) -> None:
        """
        Updating stored rate limits after an API request.
        """
        if response and "x-rate-limit-remaining" in response.headers:
            remaining = int(
                response.headers["x-rate-limit-remaining"],
            )
            reset_time = int(response.headers["x-rate-limit-reset"])
            # We're storing the uri of the endpoint as the key in our # rate limit dict.
            self.request_quotas[endpoint] = (remaining, reset_time)

    def _is_above_request_quota(
        self,
        endpoint: str,
    ) -> tuple[bool, int]:
        """
        Checking if we have reached the rate limit for a specific
        endpoint, returning a tuple (bool, int):
            - (False, -1) if there are remaining requests.
            - (True, reset_time) if the rate limit is exceeded.
        """
        exceeded_quota: bool = False
        reset_time: int = -1
        remaining_requests: int
        if endpoint in self.request_quotas:
            remaining_requests, reset_time = self.request_quotas[endpoint]
            exceeded_quota = remaining_requests == 0

        return exceeded_quota, reset_time

    def _wait_for_request_quota_reset(
        self,
        reset_time: int,
    ) -> None:
        """
        Waits for the rate limit to reset.
        """
        # Using max to avoid negative wait times.
        wait_time: float = max(0, reset_time - time.time())
        print(
            "[INFO] Rate limit exceeded.",
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
        request quota is exceeded.

        Args:
            tweet (Tweet): The tweet to like.
            retries (int): Number of retry attempts if the request fails.

        Returns:
            - True if the tweet was liked successfully.
            - False if an error occurred after all retries.
        """
        attempts_left: int = retries + 1
        current_attempt: int = 1
        exceeded_quota: bool
        reset_time: int
        endpoint: str = (
            f"https://api.twitter.com/2/users/{self.client.get_me().data.id}/likes"
        )

        while attempts_left > 0:
            attempts_left -= 1
            exceeded_quota, reset_time = self._is_above_request_quota(
                endpoint,
            )
            if exceeded_quota:
                self._wait_for_request_quota_reset(reset_time)

            try:
                # Sending a request to like the tweet.
                response: Response = self.client.like(tweet.tweet_id)
                self._update_request_quota(endpoint, response)
                return True
            except errors.TooManyRequests as e:
                print(
                    f"[ERROR] Request quota exceeded: {e}",
                    "Retry after reset duration passes.",
                )
                # Making sure we hold the most recent reset time.
                self._update_request_quota(endpoint, e.response)
            except errors.TweepyException as e:
                print(
                    f"[ERROR] Attempt to like tweet {tweet.tweet_id}",
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
        Handles the action of liking a tweet, with retries if
        request quota is exceeded.

        Args:
            tweet (Tweet): The tweet to unlike.
            retries (int): Number of retry attempts if the request fails.

        Returns:
            - True if the tweet was unliked successfully.
            - False if an error occurred after all retries.
        """
        attempts_left: int = retries + 1
        current_attempt: int = 1
        exceeded_quota: bool
        reset_time: int
        endpoint: str = (
            f"https://api.twitter.com/2/users/{self.client.get_me().data.id}/likes"
        )

        while attempts_left > 0:
            attempts_left -= 1
            exceeded_quota, reset_time = self._is_above_request_quota(
                endpoint,
            )
            if exceeded_quota:
                self._wait_for_request_quota_reset(reset_time)

            try:
                # Sending a request to unlike the tweet.
                response: Response = self.client.unlike(tweet.tweet_id)
                self._update_request_quota(endpoint, response)
                return True
            except errors.TooManyRequests as e:
                print(
                    f"[ERROR] Request quota exceeded: {e}",
                    "Retry after reset duration passes.",
                )
                # Making sure we hold the most recent reset time.
                self._update_request_quota(endpoint, e.response)
            except errors.TweepyException as e:
                # TODO: Check error string in a case we unlike a
                # tweet we have not liked.

                # If the tweet is not liked, we can return True without retrying.
                if "not liked" in str(e):
                    print(f"Tweet {tweet.tweet_id} is not liked.")
                    return True

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
    ) -> Optional[dict[str, str]]:
        """
        Fetches tweet data by ID.

        Returns:
            - The tweet data as a dictionary.
            - None if the tweet could not be fetched.
        """
        tweet_data: Optional[dict[str, str]] = None
        exceeded_quota: bool
        reset_time: int  # Timestamp of when the rate limit will
        # reset.
        endpoint: str = f"https://api.twitter.com/2/tweets"
        exceeded_quota, reset_time = self._is_above_request_quota(
            endpoint,
        )
        if exceeded_quota:
            self._wait_for_request_quota_reset(reset_time)

        try:
            response: Response = self.client.get_tweet(
                id=tweet_id,
            )
            self._update_request_quota(endpoint, response)
            # TODO: verify that response.data is a dict.
            tweet_data = response.data

        except errors.TweepyException as e:
            print(f"[ERROR] Failed to fetch tweet {tweet_id}: {e}")

        return tweet_data
