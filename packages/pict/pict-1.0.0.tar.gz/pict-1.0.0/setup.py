from setuptools import setup, find_packages

setup(
    name="pict",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colorama",  # Include colorama for colored terminal output
    ],
    entry_points={
        "console_scripts": [
            "pict=pict.cli:main",  # Register 'pict' command
        ],
    },
    author="Kelyn Njeri",
    author_email="kelyn.njeri@gmail.com",
    description="A CLI tool to generate project folder structures for Golang, TypeScript, Rust, and Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheAlchemistKE/pict",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
