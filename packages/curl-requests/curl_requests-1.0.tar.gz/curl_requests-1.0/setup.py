from setuptools import setup, find_packages

setup(
    name='curl_requests',
    version='1.0',
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        '': ['main.cpp', 'CMakeLists.txt'], 
        'curl_requests': ['*'], 
    },
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
    ],
)
