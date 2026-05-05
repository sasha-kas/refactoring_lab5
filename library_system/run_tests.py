"""
Lightweight test runner - runs all tests without external dependencies.
Usage: python run_tests.py
"""

import sys
import traceback
from typing import Callable, List, Tuple

# ── Import everything we need ────────────────────────────────────────────────
sys.path.insert(0, "/home/claude/library_system")

from src.dto.library_dto import AddBookDTO, IssueBookDTO, RegisterUserDTO, ReturnBookDTO
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


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_service() -> LibraryService:
    return LibraryService(book_repo=BookRepository(), user_repo=UserRepository())


def make_service_with_data() -> LibraryService:
    svc = make_service()
    svc.register_user(RegisterUserDTO(name="Іван Франко", email="ivan@example.com"))
    svc.add_book(AddBookDTO(title="Кобзар", author="Тарас Шевченко", isbn="978-966-01-0001-1"))
    svc.add_book(AddBookDTO(title="Тіні забутих предків", author="Михайло Коцюбинський", isbn="978-966-01-0002-2"))
    return svc


def assert_eq(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg} | expected={expected!r}, got={actual!r}")


def assert_raises(exc_type, fn: Callable):
    try:
        fn()
    except exc_type:
        return  # correct
    raise AssertionError(f"Expected {exc_type.__name__} to be raised, but it was not.")


# ── Test functions ────────────────────────────────────────────────────────────

def test_01_successful_user_registration():
    """Тест 1: Успішна реєстрація нового користувача."""
    svc = make_service()
    user = svc.register_user(RegisterUserDTO(name="Леся Українка", email="lesia@example.com"))
    assert_eq(user.user_id, 1, "user_id")
    assert_eq(user.name, "Леся Українка", "name")
    assert_eq(user.email, "lesia@example.com", "email")
    assert_eq(user.borrowed_book_ids, [], "borrowed_book_ids")


def test_02_duplicate_email_raises_error():
    """Тест 2: Реєстрація з дублікатом email → EmailAlreadyRegisteredError."""
    svc = make_service()
    svc.register_user(RegisterUserDTO(name="Перший", email="same@example.com"))
    assert_raises(
        EmailAlreadyRegisteredError,
        lambda: svc.register_user(RegisterUserDTO(name="Другий", email="same@example.com")),
    )


def test_03_empty_name_raises_error():
    """Тест 3: Реєстрація з порожнім ім'ям → LibraryServiceError."""
    svc = make_service()
    assert_raises(
        LibraryServiceError,
        lambda: svc.register_user(RegisterUserDTO(name="", email="test@example.com")),
    )


def test_04_successful_book_issue():
    """Тест 4: Успішна видача доступної книги користувачу."""
    svc = make_service_with_data()
    book = svc.issue_book(IssueBookDTO(book_id=1, user_id=1))
    assert_eq(book.is_available, False, "is_available")
    assert_eq(book.borrowed_by_user_id, 1, "borrowed_by_user_id")
    if book.borrowed_at is None:
        raise AssertionError("borrowed_at should not be None")


def test_05_user_book_list_updated_after_issue():
    """Тест 5: Після видачі книга з'являється в списку книг користувача."""
    svc = make_service_with_data()
    svc.issue_book(IssueBookDTO(book_id=1, user_id=1))
    users = svc.get_all_users()
    if 1 not in users[0].borrowed_book_ids:
        raise AssertionError("book_id=1 should be in user's borrowed list")


def test_06_issue_already_borrowed_book():
    """Тест 6: Видача вже виданої книги → BookAlreadyBorrowedError."""
    svc = make_service_with_data()
    svc.issue_book(IssueBookDTO(book_id=1, user_id=1))
    assert_raises(
        BookAlreadyBorrowedError,
        lambda: svc.issue_book(IssueBookDTO(book_id=1, user_id=1)),
    )


def test_07_issue_to_nonexistent_user():
    """Тест 7: Видача книги неіснуючому користувачу → UserNotFoundError."""
    svc = make_service_with_data()
    assert_raises(
        UserNotFoundError,
        lambda: svc.issue_book(IssueBookDTO(book_id=1, user_id=999)),
    )


def test_08_issue_nonexistent_book():
    """Тест 8: Видача неіснуючої книги → BookNotFoundError."""
    svc = make_service_with_data()
    assert_raises(
        BookNotFoundError,
        lambda: svc.issue_book(IssueBookDTO(book_id=999, user_id=1)),
    )


def test_09_successful_book_return():
    """Тест 9: Успішне повернення книги відновлює доступність."""
    svc = make_service_with_data()
    svc.issue_book(IssueBookDTO(book_id=1, user_id=1))
    book = svc.return_book(ReturnBookDTO(book_id=1, user_id=1))
    assert_eq(book.is_available, True, "is_available")
    assert_eq(book.borrowed_by_user_id, None, "borrowed_by_user_id")
    assert_eq(book.borrowed_at, None, "borrowed_at")


def test_10_return_book_not_borrowed_by_user():
    """Тест 10: Повернення чужої книги → BookNotBorrowedByUserError."""
    svc = make_service_with_data()
    svc.register_user(RegisterUserDTO(name="Другий", email="second@example.com"))
    svc.issue_book(IssueBookDTO(book_id=1, user_id=2))
    assert_raises(
        BookNotBorrowedByUserError,
        lambda: svc.return_book(ReturnBookDTO(book_id=1, user_id=1)),
    )


def test_11_find_by_title_case_insensitive():
    """Тест 11: Пошук за назвою без урахування регістру."""
    svc = make_service_with_data()
    results = svc.find_books_by_title("кобзар")
    assert_eq(len(results), 1, "result count")
    assert_eq(results[0].title, "Кобзар", "title")


def test_12_find_by_author():
    """Тест 12: Пошук за автором."""
    svc = make_service_with_data()
    results = svc.find_books_by_author("шевченко")
    assert_eq(len(results), 1, "result count")
    assert_eq(results[0].author, "Тарас Шевченко", "author")


def test_13_find_by_title_no_results():
    """Тест 13: Пошук відсутньої книги повертає порожній список."""
    svc = make_service_with_data()
    results = svc.find_books_by_title("Гаррі Поттер")
    assert_eq(results, [], "no results")


def test_14_find_by_empty_title_raises_error():
    """Тест 14: Пошук за порожнім рядком → LibraryServiceError."""
    svc = make_service_with_data()
    assert_raises(
        LibraryServiceError,
        lambda: svc.find_books_by_title(""),
    )


# ── Runner ────────────────────────────────────────────────────────────────────

TESTS: List[Callable] = [
    test_01_successful_user_registration,
    test_02_duplicate_email_raises_error,
    test_03_empty_name_raises_error,
    test_04_successful_book_issue,
    test_05_user_book_list_updated_after_issue,
    test_06_issue_already_borrowed_book,
    test_07_issue_to_nonexistent_user,
    test_08_issue_nonexistent_book,
    test_09_successful_book_return,
    test_10_return_book_not_borrowed_by_user,
    test_11_find_by_title_case_insensitive,
    test_12_find_by_author,
    test_13_find_by_title_no_results,
    test_14_find_by_empty_title_raises_error,
]


def run_all() -> None:
    passed: List[str] = []
    failed: List[Tuple[str, str]] = []

    print("=" * 65)
    print("  ЗАПУСК ЮНІТ-ТЕСТІВ — Система управління бібліотекою")
    print("=" * 65)
    print(f"  Зібрано тестів: {len(TESTS)}")
    print("-" * 65)

    for test_fn in TESTS:
        name = test_fn.__name__
        doc = (test_fn.__doc__ or "").strip()
        try:
            test_fn()
            print(f"  ✅ PASSED  {name}")
            passed.append(name)
        except Exception as exc:
            tb = traceback.format_exc(limit=3)
            print(f"  ❌ FAILED  {name}")
            print(f"            {exc}")
            failed.append((name, tb))

    print("-" * 65)
    print(f"  Результат: {len(passed)} passed, {len(failed)} failed з {len(TESTS)} тестів")
    print("=" * 65)

    if failed:
        print("\n📋 Деталі невдалих тестів:")
        for name, tb in failed:
            print(f"\n  ── {name} ──")
            print(tb)
        sys.exit(1)
    else:
        print("\n✅ Усі тести пройшли успішно!\n")


if __name__ == "__main__":
    run_all()
