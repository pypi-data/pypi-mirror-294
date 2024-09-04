#----------------------------------------------------------------
# Generated CMake target import file for configuration "relwithdebinfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sphericart" for configuration "relwithdebinfo"
set_property(TARGET sphericart APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(sphericart PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libsphericart.so.0.5.0"
  IMPORTED_SONAME_RELWITHDEBINFO "libsphericart.so.0.5"
  )

list(APPEND _cmake_import_check_targets sphericart )
list(APPEND _cmake_import_check_files_for_sphericart "${_IMPORT_PREFIX}/lib/libsphericart.so.0.5.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
