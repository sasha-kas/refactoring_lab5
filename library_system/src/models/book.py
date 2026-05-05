"""Book model for the library system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    """Represents a book in the library."""

    book_id: int
    title: str
    author: str
    isbn: str
    is_available: bool = True
    borrowed_by_user_id: Optional[int] = None
    borrowed_at: Optional[datetime] = None

    def __str__(self) -> str:
        status = "доступна" if self.is_available else f"видана (користувач #{self.borrowed_by_user_id})"
        return f"[{self.book_id}] '{self.title}' - {self.author} | {status}"
