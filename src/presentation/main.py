import os, sys
import datetime
from dotenv import load_dotenv
from src.application.use_cases.twitter.like_a_tweet import LikeATweet
from src.infrastructure.api_clients.twitter.api_client import ApiClient
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from tweepy import Client, Response  # type: ignore


# Detecting if we're running as a PyInstaller executable (bundle).
if getattr(sys, "frozen", False):
    # If bundled, use the directory where the executable is located.
    base_dir: str = os.path.dirname(sys.executable)
else:
    # If running as a script, we'll go three levels up to reach the
    # root folder.
    base_dir = os.path.dirname(  # dirname = <project root>
        os.path.dirname(  # dirname = src
            os.path.dirname(  # dirname = presentation.
                os.path.abspath(__file__),
            ),
        ),
    )

# Constructing the path to the .env file in the root directory.
dotenv_path: str = os.path.join(base_dir, ".env")

# Loading variables from the .env file (if exists) into the os
# environment.
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")


# For debug purposes.
def fetch_tweet() -> None:
    """
    Fetches a tweet by its ID using the twitter api client.
    """
    tweepy_client: Client = Client(
        consumer_key=os.getenv(
            "TWITTER_CONSUMER_KEY",
            default="",
        ),
        consumer_secret=os.getenv(
            "TWITTER_CONSUMER_SECRET",
            default="",
        ),
        access_token=os.getenv(
            "TWITTER_ACCESS_TOKEN",
            default="",
        ),
        access_token_secret=os.getenv(
            "TWITTER_ACCESS_TOKEN_SECRET",
            default="",
        ),
    )
    tweet: Response = tweepy_client.get_tweet(
        id=os.getenv("TWITTER_TWEET_ID", default=""),
    )
    print(f"Tweet: {tweet}")


def main() -> None:
    """
    Entry point of the application.
    """
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
    # fetch_tweet()
