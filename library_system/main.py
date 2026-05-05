"""Main entry point - demonstrates the library system via CLI."""

from src.controllers.library_controller import LibraryController
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.services.library_service import LibraryService


def main() -> None:
    """Bootstrap the application and run a demonstration."""
    # Dependency injection: wire up layers manually
    book_repo = BookRepository()
    user_repo = UserRepository()
    service = LibraryService(book_repo=book_repo, user_repo=user_repo)
    controller = LibraryController(service=service)

    print("=" * 55)
    print("        СИСТЕМА УПРАВЛІННЯ БІБЛІОТЕКОЮ")
    print("=" * 55)

    # --- Register users ---
    print("\n📝 Реєстрація користувачів:")
    controller.handle_register_user("Тарас Мельник", "taras@lib.ua")
    controller.handle_register_user("Оксана Іваненко", "oksana@lib.ua")
    controller.handle_register_user("Тарас Мельник", "taras@lib.ua")  # дубль — помилка

    # --- Add books ---
    print("\n📖 Додавання книг:")
    controller.handle_add_book("Кобзар", "Тарас Шевченко", "978-966-01-0001-1")
    controller.handle_add_book("Тіні забутих предків", "Михайло Коцюбинський", "978-966-01-0002-2")
    controller.handle_add_book("Захар Беркут", "Іван Франко", "978-966-01-0003-3")

    # --- List all books ---
    print("\n📚 Каталог книг:")
    controller.handle_list_books()

    # --- Search ---
    print("\n🔍 Пошук за назвою 'Кобзар':")
    controller.handle_search_by_title("Кобзар")

    print("\n🔍 Пошук за автором 'франко':")
    controller.handle_search_by_author("франко")

    # --- Issue books ---
    print("\n📤 Видача книг:")
    controller.handle_issue_book(book_id=1, user_id=1)
    controller.handle_issue_book(book_id=1, user_id=2)  # вже видана — помилка
    controller.handle_issue_book(book_id=2, user_id=2)
    controller.handle_issue_book(book_id=3, user_id=999)  # немає користувача

    # --- List books after issuing ---
    print("\n📚 Каталог після видачі:")
    controller.handle_list_books()

    # --- Return book ---
    print("\n📥 Повернення книг:")
    controller.handle_return_book(book_id=1, user_id=1)
    controller.handle_return_book(book_id=2, user_id=1)  # не та людина — помилка

    print("\n📚 Каталог після повернення:")
    controller.handle_list_books()

    print("\n👥 Зареєстровані користувачі:")
    controller.handle_list_users()

    print("\n" + "=" * 55)
    print("                 Демонстрацію завершено")
    print("=" * 55)


if __name__ == "__main__":
    main()
