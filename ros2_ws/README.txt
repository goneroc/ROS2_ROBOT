=============================================
智能传感与检测系统 — 大作业二：自主导航避障小车
=============================================

环境要求：
  - Ubuntu 22.04 LTS
  - ROS2 Humble

安装依赖：
  sudo apt-get update
  sudo apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-cartographer-ros \
    ros-humble-nav2-bringup \
    ros-humble-nav2-map-server \
    ros-humble-nav2-amcl \
    ros-humble-teleop-twist-keyboard \
    ros-humble-rviz2 \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    ros-humble-tf2-tools

编译：
  cd ros2_ws
  colcon build
  source install/setup.bash

使用步骤：

  1. 验证机器人模型（可选）：
     ros2 launch robot_description display_robot.launch.py

  2. 启动场景 + SLAM 建图：
     ros2 launch gazebo_scene bringup.launch.py mode:=slam
     另开终端：ros2 run teleop_twist_keyboard teleop_twist_keyboard
     用键盘控制机器人走S形覆盖全场

  3. 保存地图：
     ros2 run nav2_map_server map_saver_cli -f maps/map
     将生成的 map.pgm 和 map.yaml 复制到 nav_bringup/config/ 目录

  4. 启动场景 + 导航：
     ros2 launch gazebo_scene bringup.launch.py mode:=nav
     在 RViz2 中点击 "Nav2 Goal" 设置目标点 (7.5, 2.5)

场景说明：
  - 场地：8m x 5m，y范围 0~5
  - 入口：左侧 (x=0, y=1.9~3.1)
  - 出口：右侧 (x=8, y=1.9~3.1)
  - 机器人起点：(0.5, 2.5)
  - 5个障碍物（黑色）：
    1. Box 0.6x0.6x0.6m @ (2.5, 1.5)
    2. Box 0.6x0.6x0.6m @ (2.5, 3.5)
    3. Box 0.8x0.4x0.3m @ (4.5, 2.0)
    4. Box 0.8x0.4x0.3m @ (4.5, 3.0)
    5. Cylinder φ0.5m @ (6.0, 2.5)
