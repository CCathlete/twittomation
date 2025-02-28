"""
Implementation of the flow of a user liking a tweet.
"""

from datetime import datetime
from typing import Callable, Optional
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
        self.tweet_id: Id = tweet_id

    def _fetch_tweet_by_id(
        self,
        tweet_id: Id,
    ) -> Optional[Tweet]:
        """
        Fetches a tweet by its ID using the twitter api client.
        """
        tweet_data: dict[str, str] = self.twitter_api_client.get_tweet_by_id(tweet_id)
        if tweet_data:
            # Currently, tweets' creation timestamps are of the
            # format: "Wed Jun 19 02:39:57 +0000 2019"
            created_at_dt: datetime = datetime.strptime(
                tweet_data["created_at"],
                "%a %b %d %H:%M:%S %z %Y",
            )
            return Tweet(
                tweet_id=tweet_data["id"],
                author_id=tweet_data["author_id"],
                content=tweet_data["content"],
                created_at=created_at_dt,
            )
        return None

    def execute(self) -> bool:
        """
        Execution of the flow of actions in a process of liking a
        tweet.
        Returns False if execution fails, True otherwise.
        """
        success: bool = False
        tweet: Optional[Tweet] = self._fetch_tweet_by_id(self.tweet_id)
        if tweet:
            # If we managed to fetch the tweet, we try to like it
            # and if that was successful, success = True.
            success = self.tweet_liking_service.like_tweet(
                tweet,
                self.engagement_criteria,
            )
        else:
            print(f"Tweet with ID: {self.tweet_id} was not found.")

        # If the condition was False or we couldn't like the tweet
        # success stays False.
        return success
