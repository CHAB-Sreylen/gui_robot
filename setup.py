from setuptools import setup

package_name = 'my_robot_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ('share/' + package_name + '/msg', ['msg/Data.msg']),  # add Data.msg
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dona',
    maintainer_email='dona@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "draw_circle = my_robot_gui.draw_circle:main",
            "pose_subscriber = my_robot_gui.pose_subscriber:main",
            "data_publisher = my_robot_gui.data_publisher:main",
            "test = my_robot_gui.test:main"
        ],
    },
)
