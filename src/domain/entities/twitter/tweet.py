from datetime import datetime, timezone
from typing import Union
from typing_extensions import TypeAlias

Id: TypeAlias = Union[str, int]


class Tweet:
    """
    Represents a tweet and corresponding business logic.
    """

    def __init__(
        self,
        tweet_id: Id,
        author_id: Id,
        content: str,
        created_at: datetime,
        like_count: int = 0,
    ) -> None:
        self.tweet_id: Id = tweet_id
        self.author_id: Id = author_id
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tweet):
            return False
        return (
            self.tweet_id == other.tweet_id
            and self.content == other.content
            and self.author_id == other.author_id
            and self.created_at == other.created_at
            and self.like_count == other.like_count
        )
