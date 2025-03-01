import os
import pytest
import pytest_mock as ptm
import tweepy  # type: ignore
from src.domain.entities.twitter import Tweet
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from src.infrastructure.api_clients.twitter import ApiClient
from datetime import datetime


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


# Testing using the real api client.
def test_like_a_tweet(
    mocker: ptm.MockFixture,
    api_client: ApiClient,
) -> None:
    """
    Testing the api client part in the liking a tweet process.
    """
    # Creating a mock for the tweepy client.
    mock_tweepy_client: ptm.MockType = mocker.Mock(spec=tweepy.Client)
    # Registering the mock client with the api client.
    api_client.client = mock_tweepy_client

    mock_tweepy_client.like.return_value = True

    tweet = Tweet(
        tweet_id="123",
        content="Hello world",
        author_id="456",
        created_at=datetime(2025, 1, 1),
        like_count=0,
    )
    result: bool = api_client.like_tweet(tweet)

    mock_tweepy_client.like_tweet.assert_called_once_with(tweet)
    assert result is True
