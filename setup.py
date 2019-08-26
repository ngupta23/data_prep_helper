import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_prep_helper",
    version="0.0.3",
    author="Nikhil Gupta",
    author_email="mywork.ng@gmail.com",
    description="A helper library for data prepration from multiple sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngupta23/data_prep_helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)