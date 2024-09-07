from setuptools import setup, find_packages

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Descrição longa não disponível."

setup(
    name="imagic2u",
    version="1.0",
    description="Uma biblioteca para manipulação e edição de imagens usando Pillow.",
    author="R-gu3des",
    author_email="ruan.guedes789@hotmail.com",
    packages=find_packages(),
    install_requires=[
        "Pillow",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/R-gu3des",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
