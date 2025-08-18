#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for cmd-helper package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Cmd Helper - Asistente inteligente para línea de comandos"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("pylint") and not line.startswith("black") and not line.startswith("flake8") and not line.startswith("isort"):
                    requirements.append(line)
            return requirements
    return [
        "google-generativeai>=0.3.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.14.1"
    ]

setup(
    name="cmd-helper",
    version="1.0.0",
    description="Asistente inteligente para línea de comandos con IA",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Xavier Leon",
    author_email="xavier@example.com",
    url="https://github.com/xleon/cmd-helper",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cmd_helper': ['locales/*/*.json'],
    },
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'cmd-helper=cmd_helper.main:main',
            'cmdh=cmd_helper.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="command-line ai assistant helper automation",
)
