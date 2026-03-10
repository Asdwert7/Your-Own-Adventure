#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .world import World


def _print_room(room):
    print(f"\n{room.title}")
    print("-" * len(room.title))
    if room.description:
        print(room.description)


def run_game(world: World):
    current_label = world.start_room
    if not current_label or current_label not in world.rooms:
        print("❌ Ошибка: стартовая комната не найдена")
        return

    while True:
        room = world.get_room(current_label)
        if room is None:
            print(f"❌ Ошибка: комната '{current_label}' не найдена")
            return

        _print_room(room)

        if room.label == world.end_room:
            print("\n✅ Конец игры.")
            return

        if not room.actions:
            print("\n⚠️  В этой комнате нет действий. Игра завершена.")
            return

        print("\nДействия:")
        for idx, action in enumerate(room.actions, start=1):
            print(f"{idx}. {action.text}")
        print("0. Выйти")

        choice = input("> ").strip().lower()
        if choice in {"0", "q", "quit", "exit"}:
            print("👋 Выход из игры.")
            return

        if not choice.isdigit():
            print("⚠️  Введите номер действия.")
            continue

        index = int(choice) - 1
        if index < 0 or index >= len(room.actions):
            print("⚠️  Неверный номер действия.")
            continue

        current_label = room.actions[index].target
