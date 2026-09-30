"""Start Gazebo Classic and spawn the concept-stage AMR model."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = Path(get_package_share_directory('factory_delivery_amr'))
    urdf_file = share / 'urdf' / 'factory_delivery_amr.urdf'
    world_file = share / 'worlds' / 'factory_aisle.world'
    gazebo_launch = Path(get_package_share_directory('gazebo_ros')) / 'launch' / 'gazebo.launch.py'

    robot_description = urdf_file.read_text(encoding='utf-8')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(gazebo_launch)),
        launch_arguments={
            'world': str(world_file),
            'gui': LaunchConfiguration('gui'),
        }.items(),
    )

    state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_factory_delivery_amr',
        output='screen',
        arguments=[
            '-entity', 'factory_delivery_amr',
            '-file', str(urdf_file),
            '-x', '0', '-y', '0', '-z', '0',
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true', description='Show the Gazebo Classic GUI.'),
        gazebo,
        state_publisher,
        # Allow gzserver and the Gazebo ROS factory service time to start.
        TimerAction(period=5.0, actions=[spawn_robot]),
    ])