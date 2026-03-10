#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Action:
    """
    Представляет одно действие игрока: текст + переход в другую комнату.
    """
    def __init__(self, text, target):
        """
        Создаёт действие.
        
        Args:
            text: текст, который видит игрок (например, "Приказать: Включить связь")
            target: метка комнаты, куда ведёт это действие (например, "comms")
        """
        self.text = text
        self.target = target
    
    def __repr__(self):
        """
        Красивое строковое представление для отладки.
        """
        return f"Action(text='{self.text}', target='{self.target}')"


class Room:
    """
    Представляет одну комнату в игре.
    """
    def __init__(self, label, title, description, actions=None):
        """
        Создаёт комнату.
        
        Args:
            label: внутренняя метка комнаты (например, "start")
            title: заголовок, который видит игрок
            description: текстовое описание комнаты
            actions: список объектов Action (по умолчанию пустой)
        """
        self.label = label
        self.title = title
        self.description = description
        self.actions = actions if actions is not None else []
    
    def __repr__(self):
        """
        Красивое строковое представление для отладки.
        """
        return f"Room(label='{self.label}', title='{self.title}', actions={len(self.actions)})"


class World:
    """
    Представляет весь игровой мир: набор комнат, старт, финиш.
    """
    def __init__(self, start_room, end_room, rooms=None):
        """
        Создаёт мир.
        
        Args:
            start_room: метка стартовой комнаты
            end_room: метка финальной комнаты
            rooms: словарь {метка: Room} (по умолчанию пустой)
        """
        self.start_room = start_room
        self.end_room = end_room
        self.rooms = rooms if rooms is not None else {}
    
    def get_room(self, label):
        """
        Безопасно получает комнату по метке.
        
        Args:
            label: метка комнаты
            
        Returns:
            Room или None, если комната не найдена
        """
        return self.rooms.get(label)
    
    def __repr__(self):
        """
        Красивое строковое представление для отладки.
        """
        return f"World(start='{self.start_room}', end='{self.end_room}', rooms={len(self.rooms)})"
