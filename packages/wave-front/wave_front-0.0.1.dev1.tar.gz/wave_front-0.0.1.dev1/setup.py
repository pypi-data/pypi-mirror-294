from setuptools import setup, find_packages

setup(
    name="wave-front",
    version="0.0.1.dev1",
    packages=find_packages(),
    install_requires=[
        "h2o-wave==1.5.0",
    ],
)
