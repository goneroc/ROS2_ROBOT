import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    """验证机器人模型：启动 RSP + 关节滑块 + RViz2 可视化"""
    pkg_share = get_package_share_directory('robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.xacro')

    # 处理 xacro，生成 URDF 字符串
    robot_description_content = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([
        DeclareLaunchArgument(
            'model',
            default_value=xacro_file,
            description='机器人 xacro 文件路径'
        ),
        # 发布 TF 坐标变换（base_link → 各link）
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),
        # 关节滑块 GUI，可手动调节轮子转动
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        # RViz2 可视化
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(pkg_share, 'config', 'display.rviz')]
        ),
    ])
