import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
    declare_arg_namespace = DeclareLaunchArgument(
        'namespace', default_value='', description='Set namespace for tf tree.'
    )
    declare_arg_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Set true to use sim time.'
    )

    urdf_file = os.path.join(
        get_package_share_directory('whill_description'), 'urdf', 'whill_model_cr2.urdf'
    )

    with open(urdf_file, 'r') as urdf:
        urdf_content = urdf.read()

    params = {
        'use_sim_time': LaunchConfiguration('use_sim_time'),
        'frame_prefix': [LaunchConfiguration('namespace'), '/'],
        'robot_description': urdf_content,
    }

    push_ns = PushRosNamespace([LaunchConfiguration('namespace')])

    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[params],
    )

    joint_state_pub_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
    )

    ld = LaunchDescription()

    ld.add_action(declare_arg_namespace)
    ld.add_action(declare_arg_use_sim_time)

    ld.add_action(push_ns)

    ld.add_action(robot_state_pub_node)
    ld.add_action(joint_state_pub_node)
    return ld
