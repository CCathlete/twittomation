from typing import Callable
from types import MethodType
from src.domain.entities.tweet import Tweet
import src.infrastructure.api_clients.twitter as twitter


class TweetLikingService:
    """
    Handles the liking and unliking of tweets.
    """

    def __init__(
        self,
        twitter_api_client: twitter.ApiClient,
        engagement_criteria: Callable[[Tweet], bool],
    ):
        self.twitter_api_client = twitter_api_client
        self.engagement_criteria = engagement_criteria

    def like_tweet(self, tweet: Tweet) -> bool:
        """
        If the tweet meets the engagement criteria, it likes the
        tweet and returns True, otherwise returns False.
        """
        # We bind the engagement criteria as a method of the actual
        # tweet instance.
        bound_engagement_criteria: Callable[[], bool] = MethodType(
            self.engagement_criteria,
            tweet,
        )
        if not bound_engagement_criteria():
            print(
                f"Tweet {tweet.tweet_id} skipped since it does not meet the engagement criteria."
            )
            return False

        # Since the tweet meets the criteria, we call the api client
        # to like it.
        success: bool = self.twitter_api_client.like_tweet(tweet.tweet_id)
        if success:
            # If the request was successful, we update the inner
            # tweet entity.
            tweet.like()
            print(f"Tweet {tweet.tweet_id} was liked successfully.")
        else:
            print(f"Request to like tweet {tweet.tweet_id} failed.")

        return success
