from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="example_package_chas_hooge7",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[],  # "numpy", "pandas"
    entry_points={
        "console_scripts": [  # this is the CLI command--just type example_package_chas_hooge7 to run hello
            "example_package_chas_hooge7=example_package_chas_hooge7.main:hello"
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
