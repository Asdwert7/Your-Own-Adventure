#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def escape_dot_string(s):
    """Экранирует строку для безопасного использования в DOT-файле."""
    safe = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{safe}"'


def build_dot(world, add_labels=True):
    """Строит строку DOT-кода для визуализации графа игры."""
    lines = []
    
    lines.append("digraph game {")
    lines.append("    rankdir=TB;           // сверху вниз")
    lines.append("    node [shape=box, style=rounded];")
    lines.append("")
    
    lines.append("    // Вершины: комнаты")
    
    rooms = world.rooms
    start_label = world.start_room
    end_label = world.end_room
    
    for label, room in rooms.items():
        if add_labels and room.title:
            title_escaped = escape_dot_string(room.title)
            if label == start_label:
                lines.append(f'    {label} [label={title_escaped}, fillcolor="#ffccff", style="rounded,filled"];')
            elif label == end_label:
                lines.append(f'    {label} [label={title_escaped}, fillcolor="#ccffcc", style="rounded,filled"];')
            else:
                lines.append(f'    {label} [label={title_escaped}];')
        else:
            lines.append(f"    {label};")
    
    lines.append("")
    
    lines.append("    // Рёбра: переходы между комнатами")
    
    for label, room in rooms.items():
        for action in room.actions:
            action_escaped = escape_dot_string(action.text)
            lines.append(f'    {label} -> {action.target} [label={action_escaped}];')
    
    lines.append("}")
    
    return "\n".join(lines)


def save_dot(filepath, dot_text):
    """Сохраняет DOT-код в файл с кодировкой UTF-8."""
    file = open(filepath, "w", encoding="utf-8")
    try:
        file.write(dot_text)
    finally:
        file.close()


if __name__ == "__main__":
    import sys
    from engine import parse_game
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "game.md"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "game.dot"
    
    print(f"📦 Загрузка мира из {input_file}...")
    
    try:
        world = parse_game(input_file)
        
        print("🔧 Генерация DOT-кода...")
        dot_code = build_dot(world, add_labels=True)
        
        print(f"\n📄 Превью {output_file}:")
        print("─" * 60)
        preview_lines = dot_code.split("\n")[:30]
        for line in preview_lines:
            print(line)
        if len(dot_code.split("\n")) > 30:
            print("  ...")
        print("─" * 60)
        
        save_dot(output_file, dot_code)
        print(f"✅ Файл сохранён: {output_file}")
        
        print(f"\n💡 Чтобы визуализировать граф, выполните в терминале:")
        print(f"   dot -Tpng {output_file} -o game.png")
        print(f"   (требуется установленный Graphviz: https://graphviz.org)")
        
    except FileNotFoundError:
        print(f"❌ Ошибка: файл '{input_file}' не найден.")
    except ImportError:
        print("❌ Ошибка: не удалось импортировать parser.py")
        print("   Убедитесь, что parser.py находится в той же папке.")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        # Для отладки:
        # import traceback
        # traceback.print_exc()
