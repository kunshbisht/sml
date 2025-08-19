from setuptools import setup, find_packages

setup(
    name="smlc",
    version="0.1",
    packages=find_packages(),
    py_modules=["smlc", "parser"],
    entry_points={
        "console_scripts": [
            "smlc = smlc:main",
        ],
    },
)