#!/usr/bin/env python

import io
import os

from setuptools import find_packages, setup

setup(
    name='flutter-driver',
    version='1.0',
    description='An flutter automation driver for python',
    long_description=io.open(os.path.join(os.path.dirname('__file__'), 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    keywords=[
        'flutter windows',
        'python client',
        'ui automation'
    ],
    author='ndaeqa-wang',
    author_email='183181731@qq.com',
    url='https://github.com/183181731/flutter-driver',
    packages=find_packages(include=['flutter-driver*']),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing'
    ]
)