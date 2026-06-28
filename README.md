# Тестирование F-Bank

## Запуск
cd dist
python -m http.server 8000

Открыть: http://localhost:8000/?balance=30000&reserved=20001

## Найденные дефекты
- BUG-001: Отрицательная и нулевая сумма
- BUG-002: Перевод больше баланса
- BUG-003: Неправильная комиссия

## Автотесты
pip install -r tests/requirements.txt
pytest tests/ -v