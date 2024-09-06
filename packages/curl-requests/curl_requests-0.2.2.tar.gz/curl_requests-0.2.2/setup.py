from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


setup(
    name='curl_requests',
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,  # Включаем дополнительные файлы
    package_data={
        '': ['main.cpp', 'CMakeLists.txt'],  # Включение файлов в корне
        'curl_requests': ['*'],  # Включение всех файлов из папки curl_requests
    },
    install_requires=[

    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
    ],
)
