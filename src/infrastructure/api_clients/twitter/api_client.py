from src.domain.entities.twitter import Tweet, Id


class ApiClient:
    """
    An object that represents a user of the Twitter API.
    """

    def __init__(self):
        pass

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
        Fetches the data of a tweet by ID from the twitter API(JSON).
        """
        tweet_data: dict[str, str]
        return tweet_data
