# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/2/28

import setuptools
import os

root_path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(root_path, 'README.MD')

setuptools.setup(
    name="yyxx-game-pkg",
    use_scm_version={
        #"root": "..",
        "relative_to": __file__,
        "local_scheme": lambda ver: ''
    },
    setup_requires=['setuptools_scm'],
    author="yyxxgame",
    description="yyxx game custom module",
    long_description_content_type='text/markdown',
    long_description=open(filepath, encoding='utf-8').read(),
    url="https://github.com/yyxxgame/yyxxgame-pkg",
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