// graph.hpp
#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <algorithm>

// Тип графа: метка комнаты -> список комнат, куда можно перейти
using Graph = std::unordered_map<std::string, std::vector<std::string>>;

// Построить обратный граф (развернуть все рёбра)
Graph build_reverse_graph(const Graph& graph);

// Найти все комнаты, из которых можно дойти до end (BFS по обратному графу)
std::unordered_set<std::string> find_reachable_to_end(
    const Graph& reverse_graph,
    const std::string& end_label
);

// Главная функция: найти тупики (комнаты, из которых нельзя дойти до end)
std::vector<std::string> find_deadlocks(
    const Graph& graph,
    const std::string& end_label
);
