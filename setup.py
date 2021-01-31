import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="northpitchr",
    version="0.0.1",
    author="Devin Pleuler",
    description="Soccer Visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devinpleuler/northpitch",
    liscense="OSI Approved :: MIT License",
    packages=setuptools.find_packages(),
)
