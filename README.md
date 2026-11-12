# School Learning App 📚

Android приложение для школьного обучения с модульной системой JSON уроков.

## 🎯 Особенности

- **Модульная архитектура** - каждый урок = JSON файл ≤ 100 КБ
- **Python инструменты** - генератор и валидатор уроков
- **GitHub Actions** - автоматическая валидация при коммите
- **Готовая структура** - теория + примеры + задачи

## 📁 Структура

```
school-learning-app/
├── lessons/              # JSON уроки
│   ├── math/
│   │   └── grade_8/
│   ├── physics/
│   └── chemistry/
├── scripts/              # Python инструменты
│   ├── lesson_builder.py
│   ├── validate_lessons.py
│   └── requirements.txt
├── .github/workflows/    # CI/CD
└── examples/             # Примеры
```

## 🚀 Быстрый старт

### Создание урока

```python
from scripts.lesson_builder import LessonBuilder

builder = LessonBuilder(
    lesson_id="math_5_fractions",
    title="Дроби",
    subject="математика",
    grade=5
)

lesson = (builder
    .set_introduction("Изучаем дроби...")
    .add_theory_section("Что такое дробь", "Дробь это...")
    .add_example("Пример 1", "1/2 + 1/4 = 3/4")
    .add_task(
        "Вычислите 1/3 + 1/6",
        ["1/2", "1/6", "2/9", "1/9"],
        0,
        "1/3 + 1/6 = 2/6 + 1/6 = 1/2"
    )
    .build()
)

builder.save("lessons/math/grade_5/fractions.json")
```

### Валидация

```bash
# Один файл
python scripts/validate_lessons.py lessons/math/grade_8/quadratic_equations.json

# Все уроки
python scripts/validate_lessons.py lessons/ --recursive

# С лимитом
python scripts/validate_lessons.py lessons/ --recursive --max-size 50
```

## 📊 Формат JSON

```json
{
  "id": "unique_id",
  "title": "Название",
  "subject": "математика",
  "grade": 8,
  "duration_minutes": 45,
  "introduction": "...",
  "theory_sections": [...],
  "examples": [...],
  "tasks": [...],
  "tags": ["тег1", "тег2"],
  "difficulty_level": "medium"
}
```

## 🔧 Требования

- Python 3.8+
- Git

## 🤝 Вклад

1. Fork репозитория
2. Создайте ветку (`git checkout -b feature/new-lesson`)
3. Commit (`git commit -m 'Add lesson'`)
4. Push (`git push origin feature/new-lesson`)
5. Pull Request

Все уроки проверяются автоматически на:
- Валидность JSON
- Размер ≤ 100 КБ

## 📝 Лицензия

MIT License

## 👥 Авторы

School Learning App Team

---

Сделано с ❤️ для образования
