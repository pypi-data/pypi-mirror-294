from setuptools import setup, find_packages

setup(
    name="apexnova-python-stubs",
    version="0.1.2",
    description="Python stubs __generated__ from gRPC protobuf definitions for Apex Nova services.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Apex Nova",
    author_email="damien_shen@apexnova.vc",
    url="https://github.com/apexnova-vc/proto",
    packages=find_packages(where="__generated__"),
    package_dir={"": "__generated__"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "grpcio",
        "protobuf",
    ],
    python_requires=">=3.6",
)
