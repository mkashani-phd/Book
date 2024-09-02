from setuptools import setup, find_packages

setup(
    name="book",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=['numpy'],
    author="Your Name",
    author_email="mkashani.phd@gmail..com",
    description="A package for managing books, pages, and packets.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mkashani-phd/Book.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
