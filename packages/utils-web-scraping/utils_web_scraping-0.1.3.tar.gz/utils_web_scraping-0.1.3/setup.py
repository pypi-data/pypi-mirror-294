import shutil

from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Custom clean command to remove the 'dist' directory."""
    description = "remove the 'dist' directory"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('dist', ignore_errors=True)
        print("Removed 'dist' directory.")


setup(
    name="utils_web_scraping",
    version="0.1.3",
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
    cmdclass={
      'clean': CleanCommand
    },
    python_requires='>=3.6',
)
