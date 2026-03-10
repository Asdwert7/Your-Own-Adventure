#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyTextGame — текстовая игра с графовой логикой.
Точка входа в проект.

Использование:
    python main.py play              # Запустить игру
    python main.py export            # Экспортировать граф в DOT
    python main.py analyze           # Найти тупики в сюжете
    python main.py play game/other.md  # Указать свой файл
"""

import sys
import os
from pathlib import Path

from engine import parse_game, run_game, World
from graphviz import build_dot, save_dot

# Пробуем загрузить C++ модуль из graph_native, если скомпилирован
try:
    sys.path.append(str(Path(__file__).parent / "graph_native"))
    from analyzer_cpp import find_deadlocks as cpp_find_deadlocks
    HAS_NATIVE = True
except ImportError:
    HAS_NATIVE = False


# ============================================================
# Команда: play — запуск игры
# ============================================================
def cmd_play(filepath: str):
    """Загружает мир и запускает игровой цикл."""
    # Проверяем существование файла
    if not Path(filepath).exists():
        print(f"❌ Файл не найден: {filepath}")
        print("💡 Попробуй: python main.py play game/game.md")
        return 1
    
    print(f"🎮 Загрузка игры из {filepath}...")
    
    try:
        # Парсим мир
        world = parse_game(filepath)
        
        # Проверка валидности мира
        if not world or not world.start_room:
            print("❌ Ошибка: некорректный файл игры (нет START)")
            return 1
            
        print(f"✅ Мир загружен: {len(world.rooms)} комнат")
        print(f"   Старт: {world.start_room}, Финиш: {world.end_room}")
        print("─" * 50)
        
        # Запускаем движок
        run_game(world)
        return 0
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1


# ============================================================
# Команда: export — экспорт графа в DOT
# ============================================================
def cmd_export(filepath: str, output: str):
    """Генерирует .dot файл для визуализации в Graphviz."""
    if not Path(filepath).exists():
        print(f"❌ Файл не найден: {filepath}")
        return 1
    
    print(f"📦 Загрузка мира из {filepath}...")
    
    try:
        world = parse_game(filepath)
        
        print("🔧 Генерация DOT-кода...")
        # Функция из graphviz/__init__.py
        dot_code = build_dot(world, add_labels=True)
        
        # Функция из graphviz/__init__.py
        save_dot(output, dot_code)
        
        print(f"✅ Экспорт завершён: {output}")
        print(f"\n💡 Визуализировать граф можно командой:")
        print(f"   dot -Tpng {output} -o graph.png")
        print(f"   (требуется установленный Graphviz)")
        return 0
        
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")
        return 1


# ============================================================
# Команда: analyze — поиск тупиков (Deadlocks)
# ============================================================
def cmd_analyze(filepath: str):
    """Находит комнаты, из которых невозможно попасть в END."""
    if not Path(filepath).exists():
        print(f"❌ Файл не найден: {filepath}")
        return 1
    
    print(f"🔍 Анализ графа: {filepath}...")
    
    try:
        world = parse_game(filepath)
        
        graph = {}
        for label, room in world.rooms.items():
            targets = [action.target for action in room.actions]
            graph[label] = targets
        
        if HAS_NATIVE:
            print("🚀 Используем C++ модуль (graph_native)...")
            deadlocks = cpp_find_deadlocks(graph, world.end_room)
        else:
            print("⚠️  C++ модуль не найден, использую Python-реализацию...")
            try:
                from engine.parser import find_deadlocks_python
                deadlocks = find_deadlocks_python(world)
            except ImportError:
                deadlocks = _find_deadlocks_python_impl(graph, world.end_room)
        
        print(f"\n📊 Результаты анализа:")
        print(f"   Всего комнат: {len(world.rooms)}")
        print(f"   Финиш: {world.end_room}")
        
        if deadlocks:
            print(f"\n🚫 Найдено тупиков: {len(deadlocks)}")
            print("   (Комнаты, из которых НЕЛЬЗЯ дойти до финала):")
            for label in deadlocks:
                room = world.rooms.get(label)
                title = room.title if room else "???"
                print(f"   • {label} — {title}")
        else:
            print(f"\n✅ Тупиков не найдено!")
            print("   Все комнаты ведут к финалу (или достижимы из него).")
            
        return 0
        
    except Exception as e:
        print(f"❌ Ошибка при анализе: {e}")
        import traceback
        traceback.print_exc()
        return 1


# ============================================================
# Вспомогательная: чистая реализация поиска тупиков на Python
# (Фоллбэк, если C++ модуль не скомпилирован и нет отдельного файла)
# ============================================================
def _find_deadlocks_python_impl(graph: dict, end_label: str):
    """BFS по обратному графу для поиска недостижимых вершин."""
    from collections import deque
    
    # 1. Строим обратный граф
    reverse = {}
    for v in graph:
        reverse.setdefault(v, [])
    for v, neighbors in graph.items():
        for n in neighbors:
            reverse.setdefault(n, [])
            reverse[n].append(v)
    
    # 2. BFS от end
    visited = set()
    queue = deque()
    
    if end_label in reverse:
        visited.add(end_label)
        queue.append(end_label)
    
    while queue:
        curr = queue.popleft()
        for neighbor in reverse.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # 3. Собираем тупики
    return sorted([v for v in graph if v not in visited])


# ============================================================
# Справка
# ============================================================
def print_help():
    """Выводит справку по использованию."""
    print(__doc__)  # Выводим docstring из начала файла


# ============================================================
# Точка входа
# ============================================================
def main():
    # Если аргументов нет — показываем справку
    if len(sys.argv) < 2:
        print_help()
        return 0
    
    command = sys.argv[1].lower()
    
    # === Обработчик команд ===
    if command == "play":
        # python main.py play [путь_к_файлу]
        filepath = sys.argv[2] if len(sys.argv) > 2 else "game/game.md"
        return cmd_play(filepath)
        
    elif command == "export":
        # python main.py export [вход] [выход]
        infile = sys.argv[2] if len(sys.argv) > 2 else "game/game.md"
        outfile = sys.argv[3] if len(sys.argv) > 3 else "game.dot"
        return cmd_export(infile, outfile)
        
    elif command == "analyze":
        # python main.py analyze [путь_к_файлу]
        filepath = sys.argv[2] if len(sys.argv) > 2 else "game/game.md"
        return cmd_analyze(filepath)
        
    elif command in ["help", "-h", "--help"]:
        print_help()
        return 0
        
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("💡 Используй 'python main.py help' для справки")
        return 1


if __name__ == "__main__":
    # Запускаем и возвращаем код выхода для shell
    exit_code = main()
    sys.exit(exit_code)
