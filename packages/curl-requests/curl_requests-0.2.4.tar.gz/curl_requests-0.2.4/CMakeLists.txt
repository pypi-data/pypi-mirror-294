cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set CMake to prefer static libraries over shared ones (for cURL, not for the output library)
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a" ".lib")
set(BUILD_SHARED_LIBS OFF)

# Find the cURL package, prefer static library
find_package(CURL REQUIRED)

# Add a shared library (DLL/SO) for the Python bindings
add_library(my_library SHARED main.cpp)

# Link the static cURL library to your library
target_link_libraries(my_library PRIVATE CURL::libcurl)

# If you're using Windows, ensure static linking of the runtime libraries
if (MSVC)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
endif()
