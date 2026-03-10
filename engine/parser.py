#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .world import World, Room, Action


def load_text(filepath):
    """Читает файл и возвращает список строк без символа '\n' в конце."""
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.rstrip("\n") for line in file]


def save_current_room(rooms, current_room):
    """Сохраняет текущую комнату в словарь rooms."""
    if current_room is None:
        return

    room_label = current_room.get("label")
    if not room_label:
        return

    description = " ".join(current_room["description_lines"]).strip()

    actions = [Action(text, target) for text, target in current_room["actions"]]
    rooms[room_label] = Room(
        label=room_label,
        title=current_room.get("title", ""),
        description=description,
        actions=actions,
    )


def parse_game(filepath):
    """Основная функция парсинга. Возвращает объект World."""
    lines = load_text(filepath)
    
    start_room = None
    end_room = None
    rooms = {}
    
    current = None
    
    for raw_line in lines:
        line = raw_line.strip()
        
        if not line:
            continue
        
        if line.startswith("START:"):
            start_room = line.split(":", 1)[1].strip()
            continue
            
        if line.startswith("END:"):
            end_room = line.split(":", 1)[1].strip()
            continue
        
        if line.startswith("## ROOM:"):
            if current is not None:
                save_current_room(rooms, current)
            
            label = line.split(":", 1)[1].strip()
            
            current = {
                "label": label,
                "title": None,
                "description_lines": [],
                "actions": []
            }
            continue
        
        if current is None:
            continue
        
        if line.startswith("TITLE:"):
            current["title"] = line.split(":", 1)[1].strip()
            continue
        
        if line.startswith("-"):
            action_raw = line[2:].strip()
            
            if " => " in action_raw:
                text, target = action_raw.split(" => ", 1)
                current["actions"].append((text.strip(), target.strip()))
            continue
        
        current["description_lines"].append(line)
    
    if current is not None:
        save_current_room(rooms, current)
    
    if not start_room:
        print("⚠️  Warning: START не найден в файле")
    if not end_room:
        print("⚠️  Warning: END не найден в файле")
    if not rooms:
        print("⚠️  Warning: Комнаты не найдены")
    
    for label, room in rooms.items():
        for action in room.actions:
            target = action.target
            if target not in rooms:
                print(f"⚠️  Warning: Комната '{label}' ссылается на несуществующую '{target}'")
    
    return World(start_room=start_room, end_room=end_room, rooms=rooms)


def find_deadlocks_python(world: World):
    """BFS по обратному графу для поиска недостижимых вершин."""
    from collections import deque

    graph = {}
    for label, room in world.rooms.items():
        graph[label] = [action.target for action in room.actions]

    reverse = {}
    for v in graph:
        reverse.setdefault(v, [])
    for v, neighbors in graph.items():
        for n in neighbors:
            reverse.setdefault(n, [])
            reverse[n].append(v)

    visited = set()
    queue = deque()

    if world.end_room in reverse:
        visited.add(world.end_room)
        queue.append(world.end_room)

    while queue:
        curr = queue.popleft()
        for neighbor in reverse.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return sorted([v for v in graph if v not in visited])


if __name__ == "__main__":
    import sys
    
    filename = sys.argv[1] if len(sys.argv) > 1 else "game.md"
    
    print(f"🔍 Парсинг файла: {filename}\n")
    
    try:
        world = parse_game(filename)
        
        print(f"✅ Start комната: {world.start_room}")
        print(f"✅ End комната:   {world.end_room}")
        print(f"✅ Всего комнат:  {len(world.rooms)}\n")
        
        print("📋 Список комнат:")
        for label, room in world.rooms.items():
            print(f"\n  [{label}] {room.title}")
            print(f"     Описание: {room.description[:60]}...")
            print(f"     Действия ({len(room.actions)}):")
            for action in room.actions:
                print(f"       • {action.text} => {action.target}")
        
        print(f"\n🔗 Проверка переходов:")
        start = world.start_room
        if start and start in world.rooms:
            print(f"   Старт '{start}' найден в списке комнат: ОК")
        else:
            print(f"   ⚠️  Старт '{start}' не найден в комнатах!")
            
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{filename}' не найден")
    except Exception as e:
        print(f"❌ Критическая ошибка при парсинге: {e}")
