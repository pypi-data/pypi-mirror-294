from setuptools import setup, find_packages

setup(
    name="tech1200",  # Replace with your module's name
    version="0.0.2",  # Updated version
    description="A module with course info, current time, and planetary data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mymodule",  # Your module's repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas>=1.0.0"
    ],
    python_requires='>=3.6',
)
