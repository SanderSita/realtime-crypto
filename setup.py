from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="realtime-crypto",
    version="0.0.1",
    author="SanderSita",
    author_email="sandersekreve@gmail.com",
    description="A simple CoinmarketCap API for getting cryptocurrency prices and data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SanderSita/realtime-crypto",
    project_urls={"Source": "https://github.com/SanderSita/realtime-crypto"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "websockets",
    ],
)
