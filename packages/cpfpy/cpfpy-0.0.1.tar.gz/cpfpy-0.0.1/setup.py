from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cpfpy",
    version="0.0.1",
    author="Adryan Freitas",
    author_email="adryansfreitas@gmail.com",
    description="This Python module validates and formats CPF numbers, ensuring they are correct and follow the standard Brazilian format.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adryansf/cpfpy",
    packages=find_packages(),
    python_requires='>=3.0',
)