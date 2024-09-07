import setuptools
import os

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

github_ref_name = os.environ.get("GITHUB_REF_NAME")
version = github_ref_name.replace("v", "")

setuptools.setup(
    name = "fintalk_logger",
    version = version,
    author = "fintalk",
    description = "Fintalk Python logger",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8",
    install_requires=[
        "requests",
        "pydantic",
        "loguru",
    ]
)