from setuptools import setup, find_packages

setup(
    name="utils_web_scraping",
    version="0.1.0",
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[],  # List dependencies here
    author="Lucas Garcia",
    author_email="l.garcia.tyke@opes.com.co",
    description="All the functions that are shared between all the web scrappers",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Optional, add your package's homepage or GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
