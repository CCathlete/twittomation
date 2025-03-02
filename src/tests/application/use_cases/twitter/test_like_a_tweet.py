"""
Testing the entire application flow for a use case of liking a tweet.
"""

import pytest
import pytest_mock as ptm
from unittest import mock
from datetime import datetime, timezone
from typing import Callable
from src.application.use_cases.twitter.like_a_tweet import LikeATweet
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from src.infrastructure.api_clients.twitter import ApiClient
from src.domain.entities.twitter import Tweet


tweet = Tweet(
    tweet_id="123",
    content="Hello world",
    author_id="456",
    created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    like_count=0,
)


@pytest.fixture
def mock_api_client(mocker) -> ptm.MockType:
    mock_client = mocker.Mock(spec=ApiClient)
    mock_client.like_tweet.return_value = True  # Simulating a
    # successful like.
    mock_client.get_tweet_by_id.return_value = {
        "id": tweet.tweet_id,
        "content": tweet.content,
        "author_id": tweet.author_id,
        "created_at": tweet.created_at.strftime(
            "%a %b %d %H:%M:%S %z %Y",
        ),
        "like_count": tweet.like_count,
    }

    # Setting the constructor to return the mock object instead of
    # the real one.
    mocker.patch(
        "src.infrastructure.api_clients.twitter.api_client.ApiClient",
        return_value=mock_client,
    )
    return mock_client


@pytest.fixture
def mock_tweet_liking_service(mocker) -> ptm.MockType:
    mock_domain_service = mocker.Mock(spec=TweetLikingService)
    mock_domain_service.like_tweet.return_value = True  # Simulating a
    # successful like.

    # Setting the constructor to return the mock object instead of
    # the real one.
    mocker.patch(
        "src.domain.services.twitter.tweet_liking_service.TweetLikingService",
        return_value=mock_domain_service,
    )
    return mock_domain_service


def test_like_a_tweet_use_case(
    mock_tweet_liking_service: ptm.MockType,
    mock_api_client: ptm.MockType,
) -> None:
    """
    Testing a use case that calls a domain service for liking a tweet.
    """

    engagement_criteria: Callable[[Tweet], bool] = lambda tweet: True
    # Executing the use case, passing in the mock api client, mock
    # domain service and the tweet.
    result: bool = LikeATweet(
        twitter_api_client=mock_api_client,
        tweet_liking_service=mock_tweet_liking_service,
        engagement_criteria=engagement_criteria,
        tweet_id=tweet.tweet_id,
    ).execute()

    mock_tweet_liking_service.like_tweet.assert_called_once_with(
        tweet,
        engagement_criteria,
    )

    # The next assertion is only relevant if we're not using a mock
    # for the liking service because the mock doesn't call the
    # api_client.
    # mock_api_client.like_tweet.assert_called_once_with(tweet)

    assert result is True
