import time
from tweepy import OAuth1UserHandler, API, Tweet, errors  # type: ignore
from src.domain.entities.twitter import Tweet, Id
from typing_extensions import TypeAlias


EndpointInfo: TypeAlias = dict[str, int]
"""
Type: dict[str, int]
"""
Resource: TypeAlias = dict[str, EndpointInfo]
"""
Type: dict[str, EndpointInfo]
"""
ResourcesDict: TypeAlias = dict[str, Resource]
"""
Type: dict[str, Resource]\n
Resource: dict[str, EndpointInfo]\n
EndpointInfo: dict[str, int]\n
"""


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
        resource_name: str,
        endpoint_uri: str,
    ) -> tuple[bool, int]:
        """
        Checking if we have reached the rate limit for a specific
        resource and endpoint, returning a tuple (bool, int):
        - bool: True if rate limit exceeded, False otherwise
        - int: The reset time if rate limit exceeded, 0 if not
        """
        above_limit: bool = False
        reset_time: int = 0
        try:
            # Contains informatino about status pf a specific
            # resource.
            info_json: ResourcesDict = self.api.rate_limit_status(
                resources=[resource_name],
            )
            resource: Resource = info_json[resource_name]
            endpoint: EndpointInfo = resource[endpoint_uri]
            remaining_requests: int = endpoint["remaining"]
            reset_time = endpoint["reset"]
            print(f"Remaining requests for {resource_name}: {remaining_requests}")
            if remaining_requests == 0:
                above_limit = True

        except errors.TweepyException as e:
            print(f"Failed to get rate limit status: {e}.")

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
