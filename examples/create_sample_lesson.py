#!/usr/bin/env python3
"""Пример создания урока"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lesson_builder import LessonBuilder


def create_example():
    builder = LessonBuilder(
        lesson_id="example_001",
        title="Пример урока",
        subject="математика",
        grade=5
    )

    lesson = (builder
        .set_introduction("Демонстрация системы")
        .set_duration(30)
        .set_difficulty("easy")
        .add_theory_section("Теория", "Содержание...", key_points=["Пункт 1"])
        .add_example("Пример", "Решение...")
        .add_task("2 + 2 = ?", ["3", "4", "5", "6"], 1, "2 + 2 = 4", points=5)
    )

    output = Path(__file__).parent.parent / 'lessons' / 'examples' / 'sample.json'
    if builder.save(str(output)):
        print(f"\n✨ Создан: {output}")


if __name__ == "__main__":
    create_example()
