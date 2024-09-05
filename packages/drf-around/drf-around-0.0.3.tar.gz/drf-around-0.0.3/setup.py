from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="drf-around",
    version="0.0.3",
    author="iamkorniichuk",
    author_email="iamkorniichuk@gmail.com",
    description="A helper for small features that your project needs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    include_package_data=True,
    install_requires=["djangorestframework>=3.15.2"],
    project_urls={
        "Source": "https://github.com/iamkorniichuk/drf-around",
        "Tracker": "https://github.com/iamkorniichuk/drf-around/issues",
    },
)
