cmake_minimum_required(VERSION 3.16)
project(GAMEX_MACRO VERSION 1.2.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Qt6 — definir CMAKE_PREFIX_PATH si besoin, ex: C:/Qt/6.8.0/msvc2022_64
if(DEFINED ENV{QT_DIR})
    list(PREPEND CMAKE_PREFIX_PATH "$ENV{QT_DIR}")
endif()

find_package(Qt6 REQUIRED COMPONENTS Widgets Svg)

set(GAMEX_SOURCES
    main.cpp
    app/Application.cpp
    app/ThemeManager.cpp
    app/SettingsManager.cpp
    app/NavigationManager.cpp
    core/Logger.cpp
    core/DebugManager.cpp
    core/EventBus.cpp
    core/AppState.cpp
    core/AssetGenerator.cpp
    windows/MainWindow.cpp
    windows/SplashScreen.cpp
    windows/AboutWindow.cpp
    windows/SettingsWindow.cpp
    pages/Dashboard/DashboardPage.cpp
    pages/DeviceCenter/DeviceCenterPage.cpp
    pages/MacroStudio/MacroStudioPage.cpp
    pages/MacroLibrary/MacroLibraryPage.cpp
    pages/ProfileManager/ProfileManagerPage.cpp
    pages/LightingEngine/LightingPage.cpp
    pages/Analytics/AnalyticsPage.cpp
    pages/MobileCommand/MobileCommandPage.cpp
    widgets/sidebar/SidebarWidget.cpp
    widgets/sidebar/SidebarButton.cpp
    widgets/titlebar/TitleBarWidget.cpp
    widgets/cards/InfoCard.cpp
    widgets/cards/StatsCard.cpp
    widgets/cards/DeviceCard.cpp
    widgets/keyboard/KeyboardWidget.cpp
    widgets/keyboard/KeyWidget.cpp
    widgets/keyboard/KeyAnimator.cpp
    widgets/mouse/MouseWidget.cpp
    widgets/mouse/MouseButtonWidget.cpp
    widgets/rgb/RGBPanelWidget.cpp
    widgets/rgb/RGBPreviewWidget.cpp
    widgets/rgb/ColorPickerWidget.cpp
    widgets/stats/StatsPanelWidget.cpp
    widgets/stats/CounterWidget.cpp
    widgets/dock/DeviceDockWidget.cpp
    widgets/dock/DockDeviceItem.cpp
    widgets/charts/CpuChartWidget.cpp
    widgets/charts/RamChartWidget.cpp
    animations/FadeAnimation.cpp
    animations/GlowAnimation.cpp
    animations/HoverAnimation.cpp
    graphics/GlowEffect.cpp
    graphics/ShadowEffect.cpp
    graphics/BlurEffect.cpp
    models/DeviceModel.cpp
    models/MacroModel.cpp
    models/ProfileModel.cpp
    services/DeviceService.cpp
    services/MacroService.cpp
    services/MacroEngine.cpp
    services/ProfileService.cpp
    services/RGBService.cpp
    resources/gamex.qrc
)

file(GLOB_RECURSE GAMEX_HEADERS CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/app/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/core/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/windows/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/pages/*/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/widgets/*/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/widgets/*/*/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/models/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/services/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/animations/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/graphics/*.h"
)

add_executable(GAMEX_MACRO ${GAMEX_SOURCES} ${GAMEX_HEADERS})

target_include_directories(GAMEX_MACRO PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/app
    ${CMAKE_CURRENT_SOURCE_DIR}/core
)

target_link_libraries(GAMEX_MACRO PRIVATE Qt6::Widgets Qt6::Svg)

target_compile_definitions(GAMEX_MACRO PRIVATE GAMEX_SOURCE_DIR="${CMAKE_SOURCE_DIR}")
target_compile_definitions(GAMEX_MACRO PRIVATE $<$<CONFIG:Debug>:GAMEX_DEBUG>)

if(WIN32)
    set_target_properties(GAMEX_MACRO PROPERTIES WIN32_EXECUTABLE TRUE)
endif()

# Tests optionnels (requiert Qt Test) — desactive par defaut
option(GAMEX_BUILD_TESTS "Build GAMEX_MACRO unit tests" OFF)
find_package(Qt6 COMPONENTS Test QUIET)
if(GAMEX_BUILD_TESTS AND Qt6Test_FOUND)
    enable_testing()
    add_executable(GAMEX_MACRO_tests tests/WidgetTests.cpp tests/ThemeTests.cpp tests/DeviceTests.cpp)
    target_link_libraries(GAMEX_MACRO_tests PRIVATE Qt6::Widgets Qt6::Test)
    add_test(NAME GAMEX_MACRO_tests COMMAND GAMEX_MACRO_tests)
endif()
