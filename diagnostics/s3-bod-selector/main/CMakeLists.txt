idf_component_register(SRCS "main.c" INCLUDE_DIRS "." REQUIRES esp_system soc)
target_compile_definitions(${COMPONENT_LIB} PRIVATE BOD_RST_SEL=${BOD_RST_SEL})
