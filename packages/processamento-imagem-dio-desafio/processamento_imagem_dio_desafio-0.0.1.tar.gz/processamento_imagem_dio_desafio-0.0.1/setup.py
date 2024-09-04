from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processamento_imagem_dio_desafio",
    version="0.0.1",
    author="raifreire",
    description="Image Processing Package Using SKimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raifreire/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5', 
)
