import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlpandas", # Replace with your own username
    version="0.0.1",
    author="Anubrij Chandra",
    author_email="anubrij@live.com",
    description="to query the pandas Dataframe in natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "spacy"
    ],
    python_requires='>=3.6',
)