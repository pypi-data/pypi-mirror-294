from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


setup(
    name='curl_requests',
    version='0.2.4',
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        '': ['main.cpp', 'CMakeLists.txt'], 
        'curl_requests': ['*'], 
    },
    install_requires=[
        "tqdm"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
    ],
)
