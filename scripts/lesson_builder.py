#!/usr/bin/env python3
"""
Генератор структуры уроков для Android школьного приложения
Версия: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """Задача для самопроверки"""
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str
    points: int


@dataclass
class Example:
    """Практический пример"""
    title: str
    description: str
    code: str = ""
    image_url: str = ""
    notes: str = ""


@dataclass
class TheorySection:
    """Секция теоретического материала"""
    title: str
    content: str
    subsections: List[Dict[str, str]] = None
    key_points: List[str] = None

    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []
        if self.key_points is None:
            self.key_points = []


@dataclass
class Lesson:
    """Полная структура урока"""
    id: str
    title: str
    subject: str
    grade: int
    duration_minutes: int
    version: str
    created_at: str
    updated_at: str
    introduction: str
    theory_sections: List[TheorySection]
    examples: List[Example]
    tasks: List[Task]
    prerequisites: List[str]
    tags: List[str]
    difficulty_level: str
    author: str

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        result = asdict(self)
        result['theory_sections'] = [asdict(s) for s in self.theory_sections]
        result['examples'] = [asdict(e) for e in self.examples]
        result['tasks'] = [asdict(t) for t in self.tasks]
        return result

    def to_json(self, indent: int = 2) -> str:
        """Экспорт в JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def get_size_kb(self) -> float:
        """Размер в КБ"""
        return len(self.to_json(indent=None).encode('utf-8')) / 1024

    def validate_size(self, max_kb: int = 100) -> tuple:
        """Валидация размера"""
        size_kb = self.get_size_kb()
        return (size_kb <= max_kb, size_kb)


class LessonBuilder:
    """Билдер для создания уроков"""

    def __init__(self, lesson_id: str, title: str, subject: str, grade: int):
        self.lesson = Lesson(
            id=lesson_id, title=title, subject=subject, grade=grade,
            duration_minutes=45, version="1.0.0",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            introduction="", theory_sections=[], examples=[], tasks=[],
            prerequisites=[], tags=[], difficulty_level="medium",
            author="Автор не указан"
        )

    def set_introduction(self, text: str):
        self.lesson.introduction = text
        return self

    def set_duration(self, minutes: int):
        self.lesson.duration_minutes = minutes
        return self

    def set_difficulty(self, level: str):
        self.lesson.difficulty_level = level
        return self

    def set_author(self, author: str):
        self.lesson.author = author
        return self

    def add_prerequisites(self, *lesson_ids: str):
        self.lesson.prerequisites.extend(lesson_ids)
        return self

    def add_tags(self, *tags: str):
        self.lesson.tags.extend(tags)
        return self

    def add_theory_section(self, title: str, content: str, 
                          subsections: List[Dict[str, str]] = None,
                          key_points: List[str] = None):
        section = TheorySection(title, content, subsections or [], key_points or [])
        self.lesson.theory_sections.append(section)
        return self

    def add_example(self, title: str, description: str, 
                   code: str = "", image_url: str = "", notes: str = ""):
        example = Example(title, description, code, image_url, notes)
        self.lesson.examples.append(example)
        return self

    def add_task(self, question: str, options: List[str], 
                correct_answer: int, explanation: str,
                difficulty: str = "medium", points: int = 10):
        task = Task(question, options, correct_answer, explanation, difficulty, points)
        self.lesson.tasks.append(task)
        return self

    def build(self) -> Lesson:
        self.lesson.updated_at = datetime.now().isoformat()
        return self.lesson

    def save(self, output_path: str, force: bool = False) -> bool:
        """Сохранить урок с валидацией"""
        lesson = self.build()
        is_valid, size_kb = lesson.validate_size()

        if not is_valid and not force:
            print(f"❌ Размер {size_kb:.2f} КБ превышает лимит 100 КБ!", file=sys.stderr)
            return False

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lesson.to_json())

        print(f"✅ Урок сохранен: {output_path}")
        print(f"📊 Размер: {size_kb:.2f} КБ")
        return True


if __name__ == "__main__":
    print("Lesson Builder v1.0.0")
    print("Используйте для создания уроков программно")
