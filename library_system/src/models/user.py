"""User model for the library system."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    """Represents a registered library user."""

    user_id: int
    name: str
    email: str
    borrowed_book_ids: List[int] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.user_id}] {self.name} ({self.email}) | Книг на руках: {len(self.borrowed_book_ids)}"
