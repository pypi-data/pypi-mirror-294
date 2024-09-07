from setuptools import setup, find_packages

setup(
    name="ezy_io",
    version="1.0.1",
    license="MIT",
    author="Ayoub A.",
    author_email="aberbach.me@gmail.com",
    description="A CLI tool that manages files and directories.",
    long_description="List, Create, and Delete files and directories. Show the content of every file.",
    packages=find_packages(),
    requires=["click", "colorama"],
    py_modules=["ezy_io", "utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["ezy_io = ezy_io:cli"]},
    url="https://github.com/ayoub-aberbach/ezy_io",
)
