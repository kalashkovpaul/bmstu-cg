cmake_minimum_required(VERSION 3.15)
project(lab04 LANGUAGES CXX)
set(Qt5_DIR "/usr/lib/x86_64-linux-gnu/qt5")
file(GLOB projectSrc "src/*.cpp")
file(GLOB projectInclude "src/*.h")
file(GLOB projectUI "ui/*.ui")

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

find_package(Qt5 REQUIRED COMPONENTS Widgets Core)

add_library(app STATIC ${projectSrc} ${projectInclude})

include_directories(
    ${PROJECT_SOURCE_DIR}/include 
)
include_directories(
    "/usr/include/x86_64-linux-gnu/qt5/"
)
add_executable(lab04
    main.cpp
    ${projectUI}
)

target_link_libraries(lab04 app)
target_link_libraries(lab04 Qt5::Widgets)
target_link_libraries(lab04 Qt5::Core)