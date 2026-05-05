"""Library service - core business logic layer."""

from datetime import datetime
from typing import List, Optional

from src.models.book import Book
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.dto.library_dto import (
    AddBookDTO,
    IssueBookDTO,
    RegisterUserDTO,
    ReturnBookDTO,
)


class LibraryServiceError(Exception):
    """Base exception for library business logic errors."""


class BookNotFoundError(LibraryServiceError):
    """Raised when a requested book does not exist."""


class UserNotFoundError(LibraryServiceError):
    """Raised when a requested user does not exist."""


class BookAlreadyBorrowedError(LibraryServiceError):
    """Raised when trying to issue a book that is already borrowed."""


class BookNotBorrowedByUserError(LibraryServiceError):
    """Raised when a user tries to return a book they did not borrow."""


class EmailAlreadyRegisteredError(LibraryServiceError):
    """Raised when registering a user with a duplicate email."""


class LibraryService:
    """
    Implements core library business scenarios:
      - Register user
      - Add book
      - Issue book to user
      - Return book
      - Search books by title or author
    """

    def __init__(
        self,
        book_repo: BookRepository,
        user_repo: UserRepository,
    ) -> None:
        self._book_repo = book_repo
        self._user_repo = user_repo

    # ------------------------------------------------------------------
    # Scenario 1: Register user
    # ------------------------------------------------------------------
    def register_user(self, dto: RegisterUserDTO) -> User:
        """
        Register a new library user.

        Business rules:
        - Email must be unique across all users.
        - Name and email must not be empty.
        """
        if not dto.name or not dto.email:
            raise LibraryServiceError("Ім'я та email є обов'язковими полями.")

        if self._user_repo.get_by_email(dto.email) is not None:
            raise EmailAlreadyRegisteredError(
                f"Email '{dto.email}' вже зареєстрований."
            )

        return self._user_repo.add(name=dto.name, email=dto.email)

    # ------------------------------------------------------------------
    # Scenario 2: Add book
    # ------------------------------------------------------------------
    def add_book(self, dto: AddBookDTO) -> Book:
        """Add a new book to the library catalogue."""
        if not dto.title or not dto.author or not dto.isbn:
            raise LibraryServiceError("Назва, автор та ISBN є обов'язковими.")
        return self._book_repo.add(title=dto.title, author=dto.author, isbn=dto.isbn)

    # ------------------------------------------------------------------
    # Scenario 3: Issue book to user
    # ------------------------------------------------------------------
    def issue_book(self, dto: IssueBookDTO) -> Book:
        """
        Issue a book to a user.

        Business rules:
        - The book must exist.
        - The user must exist.
        - The book must currently be available (not borrowed).
        """
        book = self._book_repo.get_by_id(dto.book_id)
        if book is None:
            raise BookNotFoundError(f"Книгу з ID={dto.book_id} не знайдено.")

        user = self._user_repo.get_by_id(dto.user_id)
        if user is None:
            raise UserNotFoundError(f"Користувача з ID={dto.user_id} не знайдено.")

        if not book.is_available:
            raise BookAlreadyBorrowedError(
                f"Книга '{book.title}' вже видана іншому читачу."
            )

        # Update book state
        book.is_available = False
        book.borrowed_by_user_id = user.user_id
        book.borrowed_at = datetime.now()
        self._book_repo.save(book)

        # Update user state
        user.borrowed_book_ids.append(book.book_id)
        self._user_repo.save(user)

        return book

    # ------------------------------------------------------------------
    # Scenario 4: Return book
    # ------------------------------------------------------------------
    def return_book(self, dto: ReturnBookDTO) -> Book:
        """
        Process the return of a book from a user.

        Business rules:
        - The book must exist.
        - The user must exist.
        - The book must currently be borrowed by this specific user.
        """
        book = self._book_repo.get_by_id(dto.book_id)
        if book is None:
            raise BookNotFoundError(f"Книгу з ID={dto.book_id} не знайдено.")

        user = self._user_repo.get_by_id(dto.user_id)
        if user is None:
            raise UserNotFoundError(f"Користувача з ID={dto.user_id} не знайдено.")

        if book.borrowed_by_user_id != user.user_id:
            raise BookNotBorrowedByUserError(
                f"Книга '{book.title}' не є виданою користувачу '{user.name}'."
            )

        # Restore book to available state
        book.is_available = True
        book.borrowed_by_user_id = None
        book.borrowed_at = None
        self._book_repo.save(book)

        # Remove from user's list
        user.borrowed_book_ids.remove(book.book_id)
        self._user_repo.save(user)

        return book

    # ------------------------------------------------------------------
    # Scenario 5: Search books
    # ------------------------------------------------------------------
    def find_books_by_title(self, title: str) -> List[Book]:
        """Search books by title (partial, case-insensitive)."""
        if not title:
            raise LibraryServiceError("Рядок пошуку не може бути порожнім.")
        return self._book_repo.find_by_title(title)

    def find_books_by_author(self, author: str) -> List[Book]:
        """Search books by author name (partial, case-insensitive)."""
        if not author:
            raise LibraryServiceError("Ім'я автора не може бути порожнім.")
        return self._book_repo.find_by_author(author)

    def get_all_books(self) -> List[Book]:
        """Return all books in the library."""
        return self._book_repo.get_all()

    def get_all_users(self) -> List[User]:
        """Return all registered users."""
        return self._user_repo.get_all()
