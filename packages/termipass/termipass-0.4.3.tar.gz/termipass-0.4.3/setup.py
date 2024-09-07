# setup.py
import io

from setuptools import setup, find_packages

with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name='termipass',
    version='0.4.3',
    author="Mahmoud Raouf",
    author_email="mahmoud.raouf21@gmail.com",
    description="provides secure displays **** for password input for both Windows and Unix-like systems.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    install_requires=[],
    packages=find_packages(include=["termipass", "termipass.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
