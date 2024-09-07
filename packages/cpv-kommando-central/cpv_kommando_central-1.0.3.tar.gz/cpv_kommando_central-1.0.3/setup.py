from setuptools import find_packages, setup

setup(
    name='cpv-kommando-central',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'flask_jwt_extended', 'flask_cors'
    ],
)