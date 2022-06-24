from setuptools import setup

NAME = "label_maker_server"
VERSION = "1.0.0"

setup(
    name=NAME,
    version=VERSION,
    packages=['label_maker_server'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)