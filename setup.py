from setuptools import setup

setup(
    name='dcv2',
    packages=['dcv2'],
    include_package_data=True,
    install_requires=[
        'flask',
        'libvirt-python',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
