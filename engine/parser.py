#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def load_text(filepath):
    """
    Читает файл и возвращает список строк без символа '\n' в конце.
    """
    file = open(filepath, "r", encoding="utf-8")

    try:
        lines = [line.rstrip("\n") for line in file]
    finally:
        file.close()

    return lines


def save_current_room(rooms, current_room):
    """
    Сохраняет текущую комнату в словарь rooms.
    """
    if current_room is None:
        return

    room_label = current_room.get("label")
    if not room_label:
        return

    description = " ".join(current_room["description_lines"]).strip()

    rooms[room_label] = {
        "label": room_label,
        "title": current_room.get("title", ""),
        "description": description,
        "actions": current_room["actions"]
    }


def parse_game(filepath):
    """
    Основная функция парсинга.
    Возвращает словарь со структурой мира.
    """
    lines = load_text(filepath)
    
    # === Глобальные переменные мира ===
    start_room = None
    end_room = None
    rooms = {}
    
    # === Переменные текущей комнаты ===
    current = None  # Будет словарём, когда начнём собирать комнату
    
    # === Цикл по строкам ===
    for raw_line in lines:
        line = raw_line.strip()  # Убираем пробелы по краям для сравнения
        
        # Пропускаем пустые строки (они работают как разделители)
        if not line:
            continue
        
        # === Блок #1: Глобальные настройки игры ===
        if line.startswith("START:"):
            # split(":", 1) делит строку только по первому двоеточию
            start_room = line.split(":", 1)[1].strip()
            continue
            
        if line.startswith("END:"):
            end_room = line.split(":", 1)[1].strip()
            continue
        
        # === Блок #2: Начало новой комнаты ===
        if line.startswith("## ROOM:"):
            # Если уже собирали комнату — сохрани её перед началом новой!
            if current is not None:
                save_current_room(rooms, current)
            
            # Извлекаем метку новой комнаты
            label = line.split(":", 1)[1].strip()
            
            # Инициализируем словарь для сбора данных
            current = {
                "label": label,
                "title": None,
                "description_lines": [],
                "actions": []
            }
            continue
        
        # === Блок #3: Мы внутри комнаты ===
        # Если current is None, значит мы в "шапке" файла и игнорируем остальное
        if current is None:
            continue
        
        if line.startswith("TITLE:"):
            current["title"] = line.split(":", 1)[1].strip()
            continue
        
        if line.startswith("-"):
            # Разбираем действие: "- текст => метка"
            # Убираем "- " в начале (2 символа)
            action_raw = line[2:].strip()
            
            # Разделяем по разделителю " => "
            if " => " in action_raw:
                text, target = action_raw.split(" => ", 1)
                # Добавляем кортеж (что видит игрок, куда переходим)
                current["actions"].append((text.strip(), target.strip()))
            continue
        
        # === Блок #4: Всё остальное — часть описания ===
        # Если строка не подошла ни под одно правило выше, это текст описания
        current["description_lines"].append(line)
    
    # === После цикла: не забудь последнюю комнату! ===
    # Это частая ошибка: последняя комната не сохраняется автоматически
    if current is not None:
        save_current_room(rooms, current)
    
    # === Базовая валидация ===
    if not start_room:
        print("⚠️  Warning: START не найден в файле")
    if not end_room:
        print("⚠️  Warning: END не найден в файле")
    if not rooms:
        print("⚠️  Warning: Комнаты не найдены")
    
    # Проверка ссылок: все ли действия ведут в существующие комнаты?
    for label, room in rooms.items():
        for text, target in room["actions"]:
            if target not in rooms:
                print(f"⚠️  Warning: Комната '{label}' ссылается на несуществующую '{target}'")
    
    return {
        "start_room": start_room,
        "end_room": end_room,
        "rooms": rooms
    }


# === Точка входа для тестов ===
if __name__ == "__main__":
    import sys
    
    # Позволяем передать имя файла через аргумент командной строки
    filename = sys.argv[1] if len(sys.argv) > 1 else "game.md"
    
    print(f"🔍 Парсинг файла: {filename}\n")
    
    try:
        world = parse_game(filename)
        
        # === Красивый вывод результата ===
        print(f"✅ Start комната: {world['start_room']}")
        print(f"✅ End комната:   {world['end_room']}")
        print(f"✅ Всего комнат:  {len(world['rooms'])}\n")
        
        print("📋 Список комнат:")
        for label, room in world["rooms"].items():
            print(f"\n  [{label}] {room['title']}")
            print(f"     Описание: {room['description'][:60]}...")
            print(f"     Действия ({len(room['actions'])}):")
            for text, target in room["actions"]:
                print(f"       • {text} => {target}")
        
        # === Быстрая проверка связности ===
        print(f"\n🔗 Проверка переходов:")
        start = world["start_room"]
        if start and start in world["rooms"]:
            print(f"   Старт '{start}' найден в списке комнат: ОК")
        else:
            print(f"   ⚠️  Старт '{start}' не найден в комнатах!")
            
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{filename}' не найден")
    except Exception as e:
        print(f"❌ Критическая ошибка при парсинге: {e}")
