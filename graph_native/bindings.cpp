// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // Для автоматической конвертации STL-контейнеров
#include "graph.hpp"

namespace py = pybind11;

PYBIND11_MODULE(analyzer_cpp, m) {
    m.doc() = "C++ модуль для анализа графа игры: поиск тупиков";
    
    // Экспортируем функцию find_deadlocks в Python
    m.def("find_deadlocks", 
          &find_deadlocks,
          "Найти комнаты, из которых нельзя дойти до END",
          py::arg("graph"),           // dict[str, list[str]]
          py::arg("end_label")        // str
    );
    
    // Опционально: экспортируем вспомогательные функции для отладки
    m.def("build_reverse_graph", 
          &build_reverse_graph,
          "Построить обратный граф",
          py::arg("graph")
    );
}
