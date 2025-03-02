"""
Testing the domain service for tweet liking.
"""

import pytest
import pytest_mock as ptm
from datetime import datetime
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from src.infrastructure.api_clients.twitter import ApiClient
from src.domain.entities.twitter import Tweet


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


def test_like_a_tweet(mock_api_client: ptm.MockType) -> None:
    """
    Testing the the domain service that modifies the entities when a
    tweet is liked.
    """

    tweet = Tweet(
        tweet_id="123",
        content="Hello world",
        author_id="456",
        created_at=datetime(2025, 1, 1),
        like_count=0,
    )
    result: bool = TweetLikingService(
        mock_api_client,
    ).like_tweet(
        tweet,
        lambda tweet: True,
    )

    mock_api_client.like_tweet.assert_called_once_with(tweet)
    assert result is True
