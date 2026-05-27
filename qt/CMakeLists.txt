cmake_minimum_required(VERSION 3.21)

project(lock_qt VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Qt6 REQUIRED COMPONENTS Widgets Sql)
find_package(OpenSSL REQUIRED)

add_executable(lock_qt
    src/main.cpp
    src/main_window.cpp
    src/theme.cpp
    src/path_utils.cpp
    src/widgets/password_field.cpp
    src/dialogs/create_dialog.cpp
    src/dialogs/update_dialog.cpp
    src/dialogs/delete_dialog.cpp
    src/dialogs/search_form_widget.cpp
    src/dialogs/search_dialog.cpp
    src/dialogs/list_dialog.cpp
    src/data/password_store.cpp
    src/crypto/encryptor.cpp
)

target_include_directories(lock_qt PRIVATE include)

target_link_libraries(lock_qt PRIVATE Qt6::Widgets Qt6::Sql OpenSSL::Crypto)

add_executable(lock_qt_crypto_probe
    src/crypto_probe.cpp
    src/crypto/encryptor.cpp
)

target_include_directories(lock_qt_crypto_probe PRIVATE include)

target_link_libraries(lock_qt_crypto_probe PRIVATE Qt6::Core OpenSSL::Crypto)
