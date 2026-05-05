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
============================= test session starts ==============================
collecting ... collected 53 items

test_cases.py::TestValidateCustomer::test_empty_city PASSED              [  1%]
test_cases.py::TestValidateCustomer::test_empty_country PASSED           [  3%]
test_cases.py::TestValidateCustomer::test_empty_email PASSED             [  5%]
test_cases.py::TestValidateCustomer::test_empty_name PASSED              [  7%]
test_cases.py::TestValidateCustomer::test_invalid_email PASSED           [  9%]
test_cases.py::TestValidateCustomer::test_none_name PASSED               [ 11%]
test_cases.py::TestValidateCustomer::test_valid PASSED                   [ 13%]
test_cases.py::TestValidateProduct::test_empty_name PASSED               [ 15%]
test_cases.py::TestValidateProduct::test_neg_qty PASSED                  [ 16%]
test_cases.py::TestValidateProduct::test_valid PASSED                    [ 18%]
test_cases.py::TestValidateProduct::test_zero_price PASSED               [ 20%]
test_cases.py::TestValidateProduct::test_zero_qty PASSED                 [ 22%]
test_cases.py::TestDiscount::test_above_large PASSED                     [ 24%]
test_cases.py::TestDiscount::test_large PASSED                           [ 26%]
test_cases.py::TestDiscount::test_medium PASSED                          [ 28%]
test_cases.py::TestDiscount::test_no_discount PASSED                     [ 30%]
test_cases.py::TestDiscount::test_small PASSED                           [ 32%]
test_cases.py::TestTax::test_ca PASSED                                   [ 33%]
test_cases.py::TestTax::test_intl PASSED                                 [ 35%]
test_cases.py::TestTax::test_uk PASSED                                   [ 37%]
test_cases.py::TestTax::test_us_ca PASSED                                [ 39%]
test_cases.py::TestTax::test_us_default PASSED                           [ 41%]
test_cases.py::TestTax::test_us_ny PASSED                                [ 43%]
test_cases.py::TestTax::test_us_tx PASSED                                [ 45%]
test_cases.py::TestShipping::test_intl_heavy PASSED                      [ 47%]
test_cases.py::TestShipping::test_uk_mid PASSED                          [ 49%]
test_cases.py::TestShipping::test_us_heavy PASSED                        [ 50%]
test_cases.py::TestShipping::test_us_light PASSED                        [ 52%]
test_cases.py::TestCreateOrder::test_bad_customer_none PASSED            [ 54%]Validation error: Customer name is required

test_cases.py::TestCreateOrder::test_bad_product_none PASSED             [ 56%]Validation error: Product name is required

test_cases.py::TestCreateOrder::test_id_increments PASSED                [ 58%]
test_cases.py::TestCreateOrder::test_returns_order PASSED                [ 60%]
test_cases.py::TestCreateOrder::test_starts_pending PASSED               [ 62%]
test_cases.py::TestAdvanceStatus::test_delivered_no_advance PASSED       [ 64%]
test_cases.py::TestAdvanceStatus::test_nonexistent PASSED                [ 66%]
test_cases.py::TestAdvanceStatus::test_to_confirmed PASSED               [ 67%]
test_cases.py::TestAdvanceStatus::test_to_shipped PASSED                 [ 69%]
test_cases.py::TestCancelOrder::test_cancel_pending PASSED               [ 71%]
test_cases.py::TestCancelOrder::test_no_cancel_delivered PASSED          [ 73%]
test_cases.py::TestCancelOrder::test_nonexistent PASSED                  [ 75%]
test_cases.py::TestCancelOrder::test_returns_bool PASSED                 [ 77%]
test_cases.py::TestPromo::test_bad_code PASSED                           [ 79%]
test_cases.py::TestPromo::test_confirmed_order PASSED                    [ 81%]
test_cases.py::TestPromo::test_save10 PASSED                             [ 83%]
test_cases.py::TestPromo::test_save20 PASSED                             [ 84%]
test_cases.py::TestPromo::test_short_code PASSED                         [ 86%]
test_cases.py::TestFiltering::test_by_email PASSED                       [ 88%]
test_cases.py::TestFiltering::test_by_name PASSED                        [ 90%]
test_cases.py::TestFiltering::test_by_product PASSED                     [ 92%]
test_cases.py::TestFiltering::test_no_match PASSED                       [ 94%]
test_cases.py::TestReport::test_count PASSED                             [ 96%]
test_cases.py::TestReport::test_empty PASSED                             [ 98%]
test_cases.py::TestReport::test_revenue PASSED                           [100%]

============================== 53 passed in 0.08s ==============================

---

## Залежності

- Python 3.12+
- Стандартна бібліотека (`dataclasses`, `datetime`, `typing`)
- `pytest` — опціонально (для запуску `tests/test_library_service.py`)
