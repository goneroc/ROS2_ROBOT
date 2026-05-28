import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """导航模式：加载地图 → AMCL 定位 → Nav2 路径规划与跟踪"""
    pkg_nav = get_package_share_directory('nav_bringup')
    pkg_robot_desc = get_package_share_directory('robot_description')

    nav2_params_file = os.path.join(pkg_nav, 'config', 'nav2_params.yaml')
    map_yaml_file = os.path.join(pkg_nav, 'config', 'map.yaml')
    xacro_file = os.path.join(pkg_robot_desc, 'urdf', 'robot.xacro')

    # 用 xacro 处理机器人描述
    import xacro
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # Nav2 核心启动（含 AMCL、planner、controller、behavior server 等）
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch', 'bringup_launch.py'
            )
        ),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': nav2_params_file,
            'use_sim_time': 'true',
            'autostart': 'true',
        }.items()
    )

    # 发布机器人 TF
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

    # RViz2（加载 Nav2 默认可视化配置）
    rviz_config = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'rviz', 'nav2_default_view.rviz'
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        robot_state_pub,
        nav2_bringup,
        rviz_node,
    ])
