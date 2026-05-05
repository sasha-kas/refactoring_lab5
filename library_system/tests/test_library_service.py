"""Unit tests for LibraryService business logic."""

import pytest

from src.dto.library_dto import (
    AddBookDTO,
    IssueBookDTO,
    RegisterUserDTO,
    ReturnBookDTO,
)
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.services.library_service import (
    BookAlreadyBorrowedError,
    BookNotBorrowedByUserError,
    BookNotFoundError,
    EmailAlreadyRegisteredError,
    LibraryService,
    LibraryServiceError,
    UserNotFoundError,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def service() -> LibraryService:
    """Create a fresh LibraryService with empty repositories for each test."""
    return LibraryService(
        book_repo=BookRepository(),
        user_repo=UserRepository(),
    )


@pytest.fixture
def service_with_data(service: LibraryService) -> LibraryService:
    """Service pre-populated with one user and two books."""
    service.register_user(RegisterUserDTO(name="Іван Франко", email="ivan@example.com"))
    service.add_book(AddBookDTO(title="Кобзар", author="Тарас Шевченко", isbn="978-966-01-0001-1"))
    service.add_book(AddBookDTO(title="Тіні забутих предків", author="Михайло Коцюбинський", isbn="978-966-01-0002-2"))
    return service


# ---------------------------------------------------------------------------
# Test 1: Успішна реєстрація нового користувача
# ---------------------------------------------------------------------------

class TestRegisterUser:
    def test_successful_registration(self, service: LibraryService) -> None:
        """Реєстрація користувача з валідними даними повинна повертати об'єкт User."""
        user = service.register_user(RegisterUserDTO(name="Леся Українка", email="lesia@example.com"))

        assert user.user_id == 1
        assert user.name == "Леся Українка"
        assert user.email == "lesia@example.com"
        assert user.borrowed_book_ids == []

    def test_duplicate_email_raises_error(self, service: LibraryService) -> None:
        """Реєстрація з вже існуючим email має викликати EmailAlreadyRegisteredError."""
        service.register_user(RegisterUserDTO(name="Перший", email="same@example.com"))

        with pytest.raises(EmailAlreadyRegisteredError):
            service.register_user(RegisterUserDTO(name="Другий", email="same@example.com"))

    def test_empty_name_raises_error(self, service: LibraryService) -> None:
        """Реєстрація з порожнім ім'ям має викликати LibraryServiceError."""
        with pytest.raises(LibraryServiceError):
            service.register_user(RegisterUserDTO(name="", email="test@example.com"))


# ---------------------------------------------------------------------------
# Test 2: Успішна видача книги
# ---------------------------------------------------------------------------

class TestIssueBook:
    def test_successful_issue(self, service_with_data: LibraryService) -> None:
        """Видача доступної книги існуючому користувачу повинна змінити стан книги."""
        book = service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))

        assert book.is_available is False
        assert book.borrowed_by_user_id == 1
        assert book.borrowed_at is not None

    def test_user_book_list_updated_after_issue(self, service_with_data: LibraryService) -> None:
        """Після видачі книга повинна з'явитись у списку книг користувача."""
        service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))

        users = service_with_data.get_all_users()
        assert 1 in users[0].borrowed_book_ids

    def test_issue_already_borrowed_book_raises_error(self, service_with_data: LibraryService) -> None:
        """Спроба видати книгу, яка вже видана, має викликати BookAlreadyBorrowedError."""
        service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))

        with pytest.raises(BookAlreadyBorrowedError):
            service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))

    def test_issue_to_nonexistent_user_raises_error(self, service_with_data: LibraryService) -> None:
        """Видача книги неіснуючому користувачу має викликати UserNotFoundError."""
        with pytest.raises(UserNotFoundError):
            service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=999))

    def test_issue_nonexistent_book_raises_error(self, service_with_data: LibraryService) -> None:
        """Видача неіснуючої книги має викликати BookNotFoundError."""
        with pytest.raises(BookNotFoundError):
            service_with_data.issue_book(IssueBookDTO(book_id=999, user_id=1))


# ---------------------------------------------------------------------------
# Test 3: Повернення книги
# ---------------------------------------------------------------------------

class TestReturnBook:
    def test_successful_return(self, service_with_data: LibraryService) -> None:
        """Повернення книги повинне відновити її доступність."""
        service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))
        book = service_with_data.return_book(ReturnBookDTO(book_id=1, user_id=1))

        assert book.is_available is True
        assert book.borrowed_by_user_id is None
        assert book.borrowed_at is None

    def test_user_book_list_updated_after_return(self, service_with_data: LibraryService) -> None:
        """Після повернення книга повинна зникнути зі списку книг користувача."""
        service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=1))
        service_with_data.return_book(ReturnBookDTO(book_id=1, user_id=1))

        users = service_with_data.get_all_users()
        assert 1 not in users[0].borrowed_book_ids

    def test_return_book_not_borrowed_by_user_raises_error(self, service_with_data: LibraryService) -> None:
        """Повернення книги, яку користувач не брав, має викликати BookNotBorrowedByUserError."""
        # Реєструємо другого користувача і видаємо йому книгу
        service_with_data.register_user(RegisterUserDTO(name="Другий", email="second@example.com"))
        service_with_data.issue_book(IssueBookDTO(book_id=1, user_id=2))

        # Перший користувач намагається повернути не свою книгу
        with pytest.raises(BookNotBorrowedByUserError):
            service_with_data.return_book(ReturnBookDTO(book_id=1, user_id=1))


# ---------------------------------------------------------------------------
# Test 4: Пошук книг
# ---------------------------------------------------------------------------

class TestSearchBooks:
    def test_find_by_title_returns_matching_books(self, service_with_data: LibraryService) -> None:
        """Пошук за назвою повинен повертати відповідні книги (без урахування регістру)."""
        results = service_with_data.find_books_by_title("кобзар")

        assert len(results) == 1
        assert results[0].title == "Кобзар"

    def test_find_by_author_returns_matching_books(self, service_with_data: LibraryService) -> None:
        """Пошук за автором повинен повертати відповідні книги."""
        results = service_with_data.find_books_by_author("шевченко")

        assert len(results) == 1
        assert results[0].author == "Тарас Шевченко"

    def test_find_by_title_no_results(self, service_with_data: LibraryService) -> None:
        """Пошук за назвою, якої не існує, повинен повертати порожній список."""
        results = service_with_data.find_books_by_title("Гаррі Поттер")

        assert results == []

    def test_find_by_empty_title_raises_error(self, service_with_data: LibraryService) -> None:
        """Пошук за порожнім рядком має викликати LibraryServiceError."""
        with pytest.raises(LibraryServiceError):
            service_with_data.find_books_by_title("")
