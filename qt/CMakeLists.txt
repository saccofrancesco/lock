cmake_minimum_required(VERSION 3.21)

project(lock_qt VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Qt6 REQUIRED COMPONENTS Widgets Sql)

add_executable(lock_qt
    src/main.cpp
    src/main_window.cpp
    src/theme.cpp
    src/path_utils.cpp
)

target_include_directories(lock_qt PRIVATE include)

target_link_libraries(lock_qt PRIVATE Qt6::Widgets Qt6::Sql)
