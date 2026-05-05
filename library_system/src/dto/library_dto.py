"""Data Transfer Objects for the library system."""

from dataclasses import dataclass


@dataclass
class RegisterUserDTO:
    """DTO for user registration."""

    name: str
    email: str


@dataclass
class AddBookDTO:
    """DTO for adding a new book."""

    title: str
    author: str
    isbn: str


@dataclass
class IssueBookDTO:
    """DTO for issuing a book to a user."""

    book_id: int
    user_id: int


@dataclass
class ReturnBookDTO:
    """DTO for returning a book."""

    book_id: int
    user_id: int
