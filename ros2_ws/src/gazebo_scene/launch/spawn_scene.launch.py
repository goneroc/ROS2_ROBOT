import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    """启动 Gazebo 场景 + 生成机器人（纯仿真，不含 SLAM/导航）"""
    pkg_gazebo_scene = get_package_share_directory('gazebo_scene')
    pkg_robot_desc = get_package_share_directory('robot_description')

    world_file = os.path.join(pkg_gazebo_scene, 'worlds', 'obstacle_course.world')
    xacro_file = os.path.join(pkg_robot_desc, 'urdf', 'robot.xacro')

    # 处理 xacro → URDF
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # 机器人出生点：入口处 (0.5, 2.5)，朝向 +x 方向
    spawn_x = '0.5'
    spawn_y = '2.5'
    spawn_z = '0.2'   # 略高于地面，防止卡进地面
    spawn_yaw = '0.0' # 朝向正 x 轴

    # 启动 Gazebo（加载世界文件）
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch', 'gazebo.launch.py'
            )
        ),
        launch_arguments={
            'world': world_file,
            'verbose': 'false',
            'gui': 'true',
        }.items()
    )

    # 发布机器人 TF（需要在 spawn 之前启动）
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True,
        }]
    )

    # 在 Gazebo 中生成机器人实体
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'diff_drive_robot',
            '-x', spawn_x,
            '-y', spawn_y,
            '-z', spawn_z,
            '-Y', spawn_yaw,
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        spawn_entity,
    ])
