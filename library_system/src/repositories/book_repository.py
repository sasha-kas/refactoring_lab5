"""Book repository - handles all book data operations."""

from typing import Dict, List, Optional
from src.models.book import Book


class BookRepository:
    """Manages book storage and retrieval."""

    def __init__(self) -> None:
        self._books: Dict[int, Book] = {}
        self._next_id: int = 1

    def add(self, title: str, author: str, isbn: str) -> Book:
        """Add a new book to the repository."""
        book = Book(
            book_id=self._next_id,
            title=title,
            author=author,
            isbn=isbn,
        )
        self._books[self._next_id] = book
        self._next_id += 1
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Return a book by its ID, or None if not found."""
        return self._books.get(book_id)

    def get_all(self) -> List[Book]:
        """Return all books."""
        return list(self._books.values())

    def find_by_title(self, title: str) -> List[Book]:
        """Return books whose title contains the search string (case-insensitive)."""
        query = title.lower()
        return [b for b in self._books.values() if query in b.title.lower()]

    def find_by_author(self, author: str) -> List[Book]:
        """Return books whose author contains the search string (case-insensitive)."""
        query = author.lower()
        return [b for b in self._books.values() if query in b.author.lower()]

    def save(self, book: Book) -> Book:
        """Persist an updated book object."""
        self._books[book.book_id] = book
        return book
