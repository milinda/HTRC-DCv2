from setuptools import setup

setup(
    name='sdg',
    packages=['sdg'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'libvirt-python',
        'Flask-SQLAlchemy',
        'Flask-Testing',
        'Flask-Bootstrap',
        'daemons'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
