"""
Testing infrastructure/api_clients/twitter/api_client/ApiClient
while mocking the tweepy client.
"""

import os
import pytest
import pytest_mock as ptm
import tweepy  # type: ignore
from src.domain.entities.twitter import Tweet
from src.infrastructure.api_clients.twitter import ApiClient
from datetime import datetime


# Setting up a fixture for reusability. THIS IS NOT A MOCK.
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


# Testing using the real api client while using mocker to generate a
# mock for the tweepy client.
def test_api_client_like_tweet(
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

    # Mocking tweepy.Client's response.
    mock_response = mocker.Mock(tweepy.Response)
    mock_response.headers = {"x-rate-limit-remaining": "50"}
    mock_tweepy_client.like_tweet.return_value = mock_response

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
