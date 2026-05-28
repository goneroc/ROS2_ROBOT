#!/bin/bash
# 一键安装所有依赖 — Ubuntu 22.04 + ROS2 Humble
set -e  # 任何命令失败立即退出

if [ -z "$ROS_DISTRO" ]; then
    echo "请先 source ROS2: source /opt/ros/humble/setup.bash"
    exit 1
fi

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
    ros-humble-tf2-tools \
    ros-humble-tf-transformations

pip3 install transforms3d  # Python 坐标变换库

echo "=== 依赖安装完成 ==="
echo "下一步: cd ros2_ws && colcon build && source install/setup.bash"
