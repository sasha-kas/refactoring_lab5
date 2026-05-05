"""Library controller - CLI interface, delegates all logic to LibraryService."""

from src.dto.library_dto import (
    AddBookDTO,
    IssueBookDTO,
    RegisterUserDTO,
    ReturnBookDTO,
)
from src.services.library_service import LibraryService, LibraryServiceError


class LibraryController:
    """
    Entry point for the library application.
    Handles user input/output and delegates business logic to LibraryService.
    Contains NO business logic itself.
    """

    def __init__(self, service: LibraryService) -> None:
        self._service = service

    def handle_register_user(self, name: str, email: str) -> None:
        """Handle register-user command."""
        try:
            user = self._service.register_user(RegisterUserDTO(name=name, email=email))
            print(f"✅ Користувача зареєстровано: {user}")
        except LibraryServiceError as exc:
            print(f"❌ Помилка реєстрації: {exc}")

    def handle_add_book(self, title: str, author: str, isbn: str) -> None:
        """Handle add-book command."""
        try:
            book = self._service.add_book(AddBookDTO(title=title, author=author, isbn=isbn))
            print(f"✅ Книгу додано: {book}")
        except LibraryServiceError as exc:
            print(f"❌ Помилка додавання книги: {exc}")

    def handle_issue_book(self, book_id: int, user_id: int) -> None:
        """Handle issue-book command."""
        try:
            book = self._service.issue_book(IssueBookDTO(book_id=book_id, user_id=user_id))
            print(f"✅ Книга видана: {book}")
        except LibraryServiceError as exc:
            print(f"❌ Помилка видачі: {exc}")

    def handle_return_book(self, book_id: int, user_id: int) -> None:
        """Handle return-book command."""
        try:
            book = self._service.return_book(ReturnBookDTO(book_id=book_id, user_id=user_id))
            print(f"✅ Книгу повернено: {book}")
        except LibraryServiceError as exc:
            print(f"❌ Помилка повернення: {exc}")

    def handle_search_by_title(self, title: str) -> None:
        """Handle search-by-title command."""
        try:
            books = self._service.find_books_by_title(title)
            if books:
                print(f"📚 Знайдено книг ({len(books)}):")
                for book in books:
                    print(f"   {book}")
            else:
                print("📭 Книг за запитом не знайдено.")
        except LibraryServiceError as exc:
            print(f"❌ Помилка пошуку: {exc}")

    def handle_search_by_author(self, author: str) -> None:
        """Handle search-by-author command."""
        try:
            books = self._service.find_books_by_author(author)
            if books:
                print(f"📚 Знайдено книг ({len(books)}):")
                for book in books:
                    print(f"   {book}")
            else:
                print("📭 Книг за запитом не знайдено.")
        except LibraryServiceError as exc:
            print(f"❌ Помилка пошуку: {exc}")

    def handle_list_books(self) -> None:
        """Handle list-all-books command."""
        books = self._service.get_all_books()
        if books:
            print(f"📚 Усі книги ({len(books)}):")
            for book in books:
                print(f"   {book}")
        else:
            print("📭 Каталог порожній.")

    def handle_list_users(self) -> None:
        """Handle list-all-users command."""
        users = self._service.get_all_users()
        if users:
            print(f"👥 Усі користувачі ({len(users)}):")
            for user in users:
                print(f"   {user}")
        else:
            print("👥 Користувачів немає.")
