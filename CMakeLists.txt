cmake_minimum_required(VERSION 3.7)
project(codetemplategen)

set(CMAKE_CXX_STANDARD 11)
set(CAMAKE_C_STANDARD 11)

SET(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules" ${CMAKE_MODULE_PATH})
SET(SRC ${PROJECT_NAME})


message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

set(SOURCE_FILES ${SRC}/main.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_build_linux.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_build_mac.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_build_windows.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_cmakelists.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_disclaimer.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/template_readme.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/vscode_launch.c)
set(SOURCE_FILES ${SOURCE_FILES} ${SRC}/vscode_tasks.c)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

install(TARGETS ${PROJECT_NAME} DESTINATION bin)

set(CMAKE_CXX_FLAGS "-g -")

# ==================== PATHS TO SPECIFY! ==================== #

