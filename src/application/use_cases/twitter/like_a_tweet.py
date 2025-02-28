"""
Implementation of the flow of a user liking a tweet.
"""

from typing import Callable
import src.infrastructure.api_clients.twitter as twitter
from src.domain.entities.twitter import Tweet
from src.domain.services.twitter.tweet_liking_service import TweetLikingService


class LikeATweet:

    def __init__(self, twitter_api_client: twitter.ApiClient, twitter) -> None:
        pass
