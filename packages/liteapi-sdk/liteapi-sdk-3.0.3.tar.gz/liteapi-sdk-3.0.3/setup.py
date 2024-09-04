from setuptools import setup, find_packages

setup(
    name="liteapi-sdk",
    version="3.0.3",
    description="A Python SDK for interacting with the LiteApi travel platform",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
