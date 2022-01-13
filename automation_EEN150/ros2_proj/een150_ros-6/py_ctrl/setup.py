from setuptools import find_packages, setup

package_name = 'py_ctrl'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kristofer',
    maintainer_email='kristofer@sekvensa.se',
    description='A simple control system that can control the Course simulator',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'go = runner.ctrl:run',
            'random = runner.random_ctrl:run',
        ],
    },
)
