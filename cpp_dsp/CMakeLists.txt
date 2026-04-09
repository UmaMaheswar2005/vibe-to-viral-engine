cmake_minimum_required(VERSION 3.10)
project(VibeDSP)

# Use standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Create the executable from analyzer.cpp
add_executable(analyzer analyzer.cpp)

# Optimize for maximum speed (-O3)
target_compile_options(analyzer PRIVATE -O3)