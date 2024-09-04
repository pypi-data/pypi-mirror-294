#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rstats" for configuration "Release"
set_property(TARGET rstats APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(rstats PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/rstats.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/rstats.dll"
  )

list(APPEND _cmake_import_check_targets rstats )
list(APPEND _cmake_import_check_files_for_rstats "${_IMPORT_PREFIX}/lib/rstats.lib" "${_IMPORT_PREFIX}/bin/rstats.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
