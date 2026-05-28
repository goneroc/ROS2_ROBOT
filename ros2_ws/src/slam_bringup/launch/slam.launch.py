import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """SLAM 建图：Cartographer 节点 + 占用栅格发布节点"""
    pkg_slam = get_package_share_directory('slam_bringup')
    config_dir = os.path.join(pkg_slam, 'config')
    lua_config = os.path.join(config_dir, 'cartographer_config.lua')

    return LaunchDescription([
        # Cartographer 核心节点：接收激光+里程计，输出位姿和子图
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': True}],
            arguments=[
                '-configuration_directory', config_dir,
                '-configuration_basename', 'cartographer_config.lua',
            ],
            remappings=[
                ('scan', '/scan'),  # 订阅激光话题
            ]
        ),

        # 占用栅格节点：将子图转换为 /map 话题（供 RViz 和 map_saver 使用）
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'resolution': 0.05,  # 栅格分辨率 5cm
            }],
        ),
    ])
