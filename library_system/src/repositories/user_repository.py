"""User repository - handles all user data operations."""

from typing import Dict, List, Optional
from src.models.user import User


class UserRepository:
    """Manages user storage and retrieval."""

    def __init__(self) -> None:
        self._users: Dict[int, User] = {}
        self._next_id: int = 1

    def add(self, name: str, email: str) -> User:
        """Register a new user."""
        user = User(user_id=self._next_id, name=name, email=email)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Return a user by their ID, or None if not found."""
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """Return a user by email, or None if not found."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_all(self) -> List[User]:
        """Return all registered users."""
        return list(self._users.values())

    def save(self, user: User) -> User:
        """Persist an updated user object."""
        self._users[user.user_id] = user
        return user
