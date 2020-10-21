cmake_minimum_required(VERSION 3.15)

project(redispp_test VERSION 0.0.1)
execute_process(COMMAND conan install ${CMAKE_SOURCE_DIR} --build=missing -pr=gateway)

# Specify the output directories for libraries and binaries
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# add conan fetched packges
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(main main.cpp)
target_link_libraries(main ${CONAN_LIBS} pthread)
