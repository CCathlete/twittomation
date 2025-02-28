"""
Implementation of the flow of a user liking a tweet.
"""

from typing import Callable
import src.infrastructure.api_clients.twitter as twitter
from src.domain.entities.twitter import Tweet, Id
from src.domain.services.twitter.tweet_liking_service import TweetLikingService


class LikeATweet:

    def __init__(
        self,
        twitter_api_client: twitter.ApiClient,
        tweet_liking_service: TweetLikingService,
        engagement_criteria: Callable[[Tweet], bool],
        tweet_id: Id,
    ) -> None:
        self.twitter_api_client = twitter_api_client
        self.tweet_liking_service = tweet_liking_service
        self.engagement_criteria = engagement_criteria
        self.tweet_id: Id
