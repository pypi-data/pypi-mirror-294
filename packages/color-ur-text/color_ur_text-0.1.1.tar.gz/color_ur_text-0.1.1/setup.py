from setuptools import setup, find_packages

setup(
    name="color_ur_text",
    version="0.1.1",
    author="Basit Ahmad Ganie",
    author_email="basitahmed1412@gmail.com",
    description="A module for printing colored text in the terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/basitganie",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
