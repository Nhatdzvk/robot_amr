cmake_minimum_required(VERSION 3.8)
project(factory_delivery_amr)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  urdf
  worlds
  DESTINATION share/${PROJECT_NAME}
)

install(FILES ../../README-robot-guide.md
  DESTINATION share/${PROJECT_NAME}
  RENAME README.md
)

ament_package()