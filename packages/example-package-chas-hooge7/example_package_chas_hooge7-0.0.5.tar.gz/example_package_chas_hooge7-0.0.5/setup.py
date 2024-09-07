from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="example_package_chas_hooge7",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[],  # "numpy", "pandas"
    # this is the CLI command--
    # just type example_package_chas_hooge7 to run hello
    entry_points={
        "console_scripts": [
            "hello=example_package_chas_hooge7.main:hello",
            "goodbye=example_package_chas_hooge7.main:goodbye",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
