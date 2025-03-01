import pytest
import pytest_mock as ptm
from src.domain.services.twitter.tweet_liking_service import TweetLikingService
from src.infrastructure.api_clients.twitter import ApiClient


@pytest.fixture
def mock_api_client(mocker: ptm.MockerFixture) -> ptm.MockType:
    """
    Creates a mock for the api client and returns it.
    """
    mock_api: ptm.MockType = mocker.Mock(spec=ApiClient)
    # Simulating the like-tweet method.
    mock_api.like_tweet.return_value = True
    mocker.patch(
        "src.infrastructure.api_clients.twitter.ApiClient",
        return_value=mock_api,
    )

    return mock_api
