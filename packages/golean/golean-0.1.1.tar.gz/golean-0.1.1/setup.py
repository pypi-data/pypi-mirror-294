from setuptools import setup, find_packages

setup(
    name="golean",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    description="A Python package for interacting with the GoLean API service.",
    long_description="GoLean is a proprietary Python package for interacting with the GoLean API service. It provides tools for prompt compression and optimization.",
    author="Connor Peng",
    author_email="jinghong.peng@golean.ai",
    url="https://golean.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)