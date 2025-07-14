from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsonport",
    version="0.1.0",
    author="Luan Schons",
    description="Uma biblioteca Python para serialização e deserialização de objetos Python para JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luan1schons/jsonport",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
) 