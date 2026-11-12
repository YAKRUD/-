#!/usr/bin/env python3
"""
Валидатор размера и структуры JSON уроков
Проверяет лимит 100 КБ и корректность JSON
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Tuple
import argparse


class JSONSizeValidator:
    """Валидатор JSON файлов"""

    def __init__(self, max_size_kb: int = 100):
        self.MAX_SIZE_KB = max_size_kb
        self.MAX_SIZE_BYTES = max_size_kb * 1024

    def check_file(self, file_path: str) -> Tuple[bool, float, str]:
        """Проверить один файл"""
        try:
            if not os.path.exists(file_path):
                return False, 0, f"Файл не найден: {file_path}"

            size_kb = os.path.getsize(file_path) / 1024

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                return False, size_kb, f"Невалидный JSON: {e}"

            if size_kb > self.MAX_SIZE_KB:
                return False, size_kb, f"Превышен лимит: {size_kb:.2f} > {self.MAX_SIZE_KB} КБ"

            return True, size_kb, f"OK: {size_kb:.2f} КБ"

        except Exception as e:
            return False, 0, f"Ошибка: {e}"

    def check_directory(self, directory: str, recursive: bool = True) -> Dict:
        """Проверить все JSON в директории"""
        results = {'total': 0, 'valid': 0, 'invalid': 0, 'results': []}

        pattern = "**/*.json" if recursive else "*.json"
        json_files = list(Path(directory).glob(pattern))
        results['total'] = len(json_files)

        for json_file in json_files:
            is_valid, size_kb, message = self.check_file(str(json_file))
            results['results'].append({
                'file': str(json_file),
                'valid': is_valid,
                'size_kb': size_kb,
                'message': message
            })
            if is_valid:
                results['valid'] += 1
            else:
                results['invalid'] += 1

        return results

    def print_report(self, results: Dict, verbose: bool = True):
        """Вывести отчет"""
        print("=" * 70)
        print("📊 ОТЧЕТ ВАЛИДАЦИИ JSON")
        print("=" * 70)
        print(f"Максимум: {self.MAX_SIZE_KB} КБ")
        print(f"Всего: {results['total']}")
        print(f"✅ Валидных: {results['valid']}")
        print(f"❌ Невалидных: {results['invalid']}")
        print("=" * 70)

        if verbose or results['invalid'] > 0:
            print("\n📁 ДЕТАЛИ:")
            for result in results['results']:
                status = "✅" if result['valid'] else "❌"
                print(f"{status} {Path(result['file']).name}")
                print(f"   {result['size_kb']:.2f} КБ - {result['message']}")

        return results['invalid'] == 0


def main():
    parser = argparse.ArgumentParser(description='Валидатор JSON уроков')
    parser.add_argument('path', help='Путь к файлу или директории')
    parser.add_argument('--max-size', type=int, default=100, help='Макс размер (КБ)')
    parser.add_argument('--recursive', action='store_true', help='Рекурсивно')
    parser.add_argument('--quiet', action='store_true', help='Тихий режим')

    args = parser.parse_args()
    validator = JSONSizeValidator(max_size_kb=args.max_size)

    if os.path.isfile(args.path):
        is_valid, size_kb, message = validator.check_file(args.path)
        print(f"{'✅' if is_valid else '❌'} {args.path}")
        print(f"Размер: {size_kb:.2f} КБ")
        print(message)
        sys.exit(0 if is_valid else 1)

    elif os.path.isdir(args.path):
        results = validator.check_directory(args.path, recursive=args.recursive)
        success = validator.print_report(results, verbose=not args.quiet)
        sys.exit(0 if success else 1)

    else:
        print(f"❌ Путь не найден: {args.path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
