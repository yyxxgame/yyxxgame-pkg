# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/2/28

import setuptools

filepath = 'README.md'

setuptools.setup(
    name="yyxx-game-pkg",
    version="0.0.3b",
    author="yyxxgame",
    description="yyxx game custom module",
    long_description_content_type='text/markdown',
    long_description=open(filepath, encoding='utf-8').read(),
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "opentelemetry-api>=1.16.0",
        "opentelemetry-exporter-jaeger>=1.16.0",
        "opentelemetry-sdk>=1.16.0",
        "opentelemetry-instrumentation-requests>=0.37b0"
    ]
)