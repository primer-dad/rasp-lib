from setuptools import setup, find_packages

setup(
    name="rasp-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "google-cloud-logging",
        "pytz"
    ],
)
