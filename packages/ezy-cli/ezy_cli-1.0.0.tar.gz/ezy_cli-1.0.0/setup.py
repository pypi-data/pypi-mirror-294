from setuptools import setup, find_packages

setup(
    name="ezy-cli",
    version="1.0.0",
    author="Ayoub A.",
    author_email="aberbach.me@gmail.com",
    description="A CLI tool that manages files and directories.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    url="https://github.com/ayoub-aberbach/ez_cli",
)
