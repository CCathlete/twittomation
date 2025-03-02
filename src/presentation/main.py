import os
import datetime
from dotenv import load_dotenv
from src.application.use_cases.twitter.like_a_tweet import LikeATweet
from src.infrastructure.api_clients.twitter.api_client import ApiClient
from src.domain.services.twitter.tweet_liking_service import TweetLikingService


def main() -> None:
    """
    Entry point of the application.
    """
    # Loading variables from the .env file into the os environment.
    load_dotenv()

    consumer_key: str = os.getenv(
        "TWITTER_CONSUMER_KEY",
        default="",
    )
    consumer_secret: str = os.getenv(
        "TWITTER_CONSUMER_SECRET",
        default="",
    )
    access_token: str = os.getenv(
        "TWITTER_ACCESS_TOKEN",
        default="",
    )
    access_token_secret: str = os.getenv(
        "TWITTER_ACCESS_TOKEN_SECRET",
        default="",
    )

    tweet_id: str = os.getenv(
        "TWITTER_TWEET_ID",
        default="",
    )

    if (
        not consumer_key
        or not consumer_secret
        or not access_token
        or not access_token_secret
        or not tweet_id
    ):
        raise Exception("Missing environment variables.")

    api_client: ApiClient = ApiClient(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )

    tweet_liking_service: TweetLikingService = TweetLikingService(
        api_client,
    )

    use_case: LikeATweet = LikeATweet(
        twitter_api_client=api_client,
        tweet_liking_service=tweet_liking_service,
        # For future use in case we want to filter out tweets.
        engagement_criteria=lambda tweet: True,
        tweet_id=tweet_id,
    )

    if use_case.execute():
        print(
            f"Tweet {tweet_id} was liked successfully at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    else:
        print("Failed to like the tweet.")


if __name__ == "__main__":
    main()
