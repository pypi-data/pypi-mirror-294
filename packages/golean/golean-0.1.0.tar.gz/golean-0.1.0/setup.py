from setuptools import setup, find_packages

setup(
    name="golean",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    description="A Python package for interacting with the GoLean API service.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Connor Peng",
    author_email="jinghong.peng@golean.ai",
    url="https://github.com/golean-ai/golean-python",  # Updated URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)