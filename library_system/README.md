# Лабораторна робота №5 — Система управління бібліотекою

## Опис проєкту

Консольна система управління бібліотекою, реалізована на **Python 3.12** з дотриманням архітектурного шаблону **Controller → Service → Repository**.

---

## Бізнес-сценарії

| # | Сценарій | Клас / Метод |
|---|----------|-------------|
| 1 | Реєстрація користувача | `LibraryService.register_user()` |
| 2 | Видача книги читачу | `LibraryService.issue_book()` |
| 3 | Повернення книги | `LibraryService.return_book()` |
| 4 | Пошук книги за назвою / автором | `LibraryService.find_books_by_title/author()` |

### Бізнес-правила

**Реєстрація користувача**
- Ім'я і email є обов'язковими полями.
- Email має бути унікальним у системі.

**Видача книги**
- Книга і користувач мають існувати в системі.
- Книга має бути доступною (не видана іншому читачу).
- Після видачі фіксується час та ID читача.

**Повернення книги**
- Книга і користувач мають існувати.
- Повернути книгу може лише той читач, якому вона була видана.
- Після повернення книга стає знову доступною.

**Пошук книг**
- Пошук виконується за частковим збігом (без урахування регістру).
- Рядок пошуку не може бути порожнім.

---

## Структура проєкту

```
library_system/
├── main.py                          # Точка входу (CLI-демонстрація)
├── run_tests.py                     # Запуск юніт-тестів
├── README.md
├── src/
│   ├── models/
│   │   ├── book.py                  # Модель Book
│   │   └── user.py                  # Модель User
│   ├── dto/
│   │   └── library_dto.py           # Data Transfer Objects
│   ├── repositories/
│   │   ├── book_repository.py       # Репозиторій книг
│   │   └── user_repository.py       # Репозиторій користувачів
│   ├── services/
│   │   └── library_service.py       # Бізнес-логіка (головний шар)
│   └── controllers/
│       └── library_controller.py    # Контролер (CLI-точка входу)
└── tests/
    └── test_library_service.py      # Юніт-тести (pytest-сумісні)
```

---

## Запуск

### Демонстрація роботи системи

```bash
cd library_system
python3 main.py
```

### Запуск тестів (вбудований runner)

```bash
python3 run_tests.py
```

### Запуск тестів через pytest (якщо встановлений)

```bash
pip install pytest
pytest tests/ -v
```

---

## Лог тестів

```
=================================================================
  ЗАПУСК ЮНІТ-ТЕСТІВ — Система управління бібліотекою
=================================================================
  Зібрано тестів: 14
-----------------------------------------------------------------
  ✅ PASSED  test_01_successful_user_registration
  ✅ PASSED  test_02_duplicate_email_raises_error
  ✅ PASSED  test_03_empty_name_raises_error
  ✅ PASSED  test_04_successful_book_issue
  ✅ PASSED  test_05_user_book_list_updated_after_issue
  ✅ PASSED  test_06_issue_already_borrowed_book
  ✅ PASSED  test_07_issue_to_nonexistent_user
  ✅ PASSED  test_08_issue_nonexistent_book
  ✅ PASSED  test_09_successful_book_return
  ✅ PASSED  test_10_return_book_not_borrowed_by_user
  ✅ PASSED  test_11_find_by_title_case_insensitive
  ✅ PASSED  test_12_find_by_author
  ✅ PASSED  test_13_find_by_title_no_results
  ✅ PASSED  test_14_find_by_empty_title_raises_error
-----------------------------------------------------------------
  Результат: 14 passed, 0 failed з 14 тестів
=================================================================

✅ Усі тести пройшли успішно!
```

---

## Залежності

- Python 3.12+
- Стандартна бібліотека (`dataclasses`, `datetime`, `typing`)
- `pytest` — опціонально (для запуску `tests/test_library_service.py`)
