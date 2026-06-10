cmake_minimum_required(VERSION 3.16)
project(GameXClicker LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(GX_SOURCES
    src/main.cpp
    src/control_panel.cpp
    src/process_launcher.cpp
    src/core/win32_input.cpp
    src/core/engine.cpp
    src/core/rgb_engine.cpp
)

add_executable(GameXClicker WIN32 ${GX_SOURCES})

target_include_directories(GameXClicker PRIVATE src)
target_link_libraries(GameXClicker PRIVATE user32 gdi32 shell32 comctl32)

if(MSVC)
    target_compile_options(GameXClicker PRIVATE /W4 /utf-8)
endif()

add_custom_command(TARGET GameXClicker POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:GameXClicker>
        ${CMAKE_SOURCE_DIR}/../GameXClicker.exe
    COMMENT "Copy GameXClicker.exe to project root"
)
