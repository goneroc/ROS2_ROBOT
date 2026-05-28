import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    GroupAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    """总启动文件：一键启动 Gazebo + 机器人 + SLAM 或 导航（通过 mode 参数切换）"""
    pkg_gazebo_scene = get_package_share_directory('gazebo_scene')
    pkg_robot_desc = get_package_share_directory('robot_description')
    pkg_slam = get_package_share_directory('slam_bringup')
    pkg_nav = get_package_share_directory('nav_bringup')

    world_file = os.path.join(pkg_gazebo_scene, 'worlds', 'obstacle_course.world')
    xacro_file = os.path.join(pkg_robot_desc, 'urdf', 'robot.xacro')
    nav2_params = os.path.join(pkg_nav, 'config', 'nav2_params.yaml')
    map_yaml = os.path.join(pkg_nav, 'config', 'map.yaml')

    robot_description_content = xacro.process_file(xacro_file).toxml()

    # 启动模式切换：slam=建图模式, nav=导航模式
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='slam',
        description='启动模式: slam=建图模式, nav=导航模式'
    )

    # ---- Gazebo ----
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

    # ---- Robot State Publisher ----
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

    # ---- Spawn Robot ----
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'diff_drive_robot',
            '-x', '0.5',
            '-y', '2.5',
            '-z', '0.2',
            '-Y', '0.0',
        ]
    )

    # ---- SLAM 模式：Cartographer 建图 ----
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam, 'launch', 'slam.launch.py')
        ),
        condition=IfCondition(PythonExpression(["'", LaunchConfiguration('mode'), "' == 'slam'"]))
    )

    # ---- Nav 模式：Nav2 自主导航 ----
    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav, 'launch', 'nav.launch.py')
        ),
        condition=IfCondition(PythonExpression(["'", LaunchConfiguration('mode'), "' == 'nav'"]))
    )

    return LaunchDescription([
        mode_arg,
        gazebo,
        robot_state_pub,
        spawn_entity,
        slam_launch,
        nav_launch,
    ])
