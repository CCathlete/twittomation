from datetime import datetime, timezone
from typing import Union


class Tweet:
    """
    Represents a tweet and correponding business logic.
    """

    def __init__(
        self,
        tweet_id: Union[str, int],
        author_id: Union[str, int],
        content: str,
        created_at: datetime,
        like_count: int = 0,
    ) -> None:
        self.tweet_id: Union[str, int] = tweet_id
        self.author_id: Union[str, int] = author_id
        self.content: str = content
        self.created_at: datetime = created_at
        self.like_count: int = like_count

    def like(self) -> None:
        """
        Each time the tweet is liked, count += 1
        """
        self.like_count += 1

    def unlike(self) -> None:
        """
        Each time the tweet is unliked, count -= 1
        """
        self.like_count -= 1

    def is_recent(
        self,
        threshold_in_min: int = 60,
    ) -> bool:
        """
        Checks if the tweet was posted in the last `threshold_in_min`
        minutes
        """
        return (
            datetime.now(timezone.utc) - self.created_at
        ).total_seconds() < threshold_in_min * 60

    def __repr__(self) -> str:
        return f"Tweet(tweet_id={self.tweet_id}, author_id={self.author_id}, content={self.content}, created_at={self.created_at}, like_count={self.like_count})"
