cmake_minimum_required(VERSION 3.22)

if(NOT DEFINED BOD_RST_SEL OR NOT "${BOD_RST_SEL}" MATCHES "^[01]$")
    message(FATAL_ERROR "BOD_RST_SEL must be explicitly 0 or 1")
endif()
execute_process(COMMAND git -C "$ENV{IDF_PATH}" rev-parse HEAD
                OUTPUT_VARIABLE actual_idf OUTPUT_STRIP_TRAILING_WHITESPACE
                RESULT_VARIABLE idf_status)
if(NOT idf_status EQUAL 0 OR NOT actual_idf STREQUAL "fff9895c82d744c7237be8847347bdd1b07c6643")
    message(FATAL_ERROR "The diagnostic requires the exact admitted ESP-IDF commit")
endif()
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
idf_build_set_property(MINIMAL_BUILD ON)
project(s3_bod_selector)
