from typing import Optional
from src.domain.entities.tweet import Tweet
from src.infrastructure.twitter_api import TwitterAPIClient


class TweetLikingService:
    """
    Handles the liking and unliking of tweets
    """

    def __init__(self, twitter_api_client: TwitterAPIClient):
        self.twitter_api_client = twitter_api_client
