# setup.py
from setuptools import setup, find_packages

setup(
    name="higuard-sdk",
    version="0.1.9",
    author="Derek Li",
    author_email="derekli11204@gmail.com",
    description="Python SDK for Error Dashboard",
    url="https://github.com/HiQ-Apps/error_dashboard_python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[[
        "certifi>=2024.7.4",
        "charset-normalizer>=3.3.2",
        "idna>=3.7",
        "requests>=2.32.3",
        "ua-parser>=0.18.0",
        "urllib3>=2.2.2",
        "user-agents>=2.2.0",
    ]],
)
