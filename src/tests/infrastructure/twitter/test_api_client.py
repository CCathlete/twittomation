import os
import pytest
import pytest_mock as ptm
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from src.infrastructure.api_clients.twitter import ApiClient


# Setting up a fixture for reusability.
@pytest.fixture
def api_client() -> ApiClient:
    return ApiClient(
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


@pytest.fixture
def mock_api_client(mocker) -> ptm.MockType:
    mock_client = mocker.Mock(spec=ApiClient)
    mock_client.like_tweet.return_value = True  # Simulating a
    # successful like.

    # Setting the constructor to return the mock object instead of
    # the real one.
    mocker.patch(
        "src.infrastructure.api_clients.twitter.api_client.ApiClient",
        return_value=mock_client,
    )
    return mock_client
