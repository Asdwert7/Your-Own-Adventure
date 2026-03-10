// graph.cpp
#include "graph.hpp"

// ============================================================
// Построение обратного графа
// ============================================================
Graph build_reverse_graph(const Graph& graph) {
    Graph reverse_graph;
    
    // Шаг 1: Добавить все вершины (даже без рёбер)
    for (const auto& [vertex, neighbors] : graph) {
        if (reverse_graph.find(vertex) == reverse_graph.end()) {
            reverse_graph[vertex] = {};
        }
    }
    
    // Шаг 2: Развернуть рёбра: A->B становится B->A
    for (const auto& [vertex, neighbors] : graph) {
        for (const auto& neighbor : neighbors) {
            // Гарантируем, что сосед существует в обратном графе
            if (reverse_graph.find(neighbor) == reverse_graph.end()) {
                reverse_graph[neighbor] = {};
            }
            // Добавляем обратное ребро
            reverse_graph[neighbor].push_back(vertex);
        }
    }
    
    return reverse_graph;
}

// ============================================================
// BFS: поиск достижимых до end по обратному графу
// ============================================================
std::unordered_set<std::string> find_reachable_to_end(
    const Graph& reverse_graph,
    const std::string& end_label
) {
    std::unordered_set<std::string> visited;
    std::queue<std::string> queue;
    
    // Если end нет в графе — возвращаем пустое множество
    if (reverse_graph.find(end_label) == reverse_graph.end()) {
        return visited;
    }
    
    // Инициализация BFS
    visited.insert(end_label);
    queue.push(end_label);
    
    // Основной цикл BFS
    while (!queue.empty()) {
        std::string current = queue.front();
        queue.pop();
        
        // Обходим всех соседей в обратном графе
        auto it = reverse_graph.find(current);
        if (it != reverse_graph.end()) {
            for (const auto& neighbor : it->second) {
                if (visited.find(neighbor) == visited.end()) {
                    visited.insert(neighbor);
                    queue.push(neighbor);
                }
            }
        }
    }
    
    return visited;
}

// ============================================================
// Поиск тупиков: комнаты, НЕ достижимые до end
// ============================================================
std::vector<std::string> find_deadlocks(
    const Graph& graph,
    const std::string& end_label
) {
    std::vector<std::string> deadlocks;
    
    // Шаг 1: Построить обратный граф
    Graph rev_graph = build_reverse_graph(graph);
    
    // Шаг 2: Найти достижимые до end
    auto reachable = find_reachable_to_end(rev_graph, end_label);
    
    // Шаг 3: Собрать тупики (вершины, которых нет в reachable)
    for (const auto& [label, neighbors] : graph) {
        if (reachable.find(label) == reachable.end()) {
            deadlocks.push_back(label);
        }
    }
    
    // Сортировка для стабильного вывода (опционально, но удобно)
    std::sort(deadlocks.begin(), deadlocks.end());
    
    return deadlocks;
}
