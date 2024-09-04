from setuptools import setup, find_packages

with open("README.md", 'r') as readme:
    description = readme.read()
setup(
    name = "namaste_samsara",
    version = "0.3",
    packages = find_packages(),
    entry_points = {
        "console_scripts" : [
            "namaste-samsara = namaste_samsara:hello"
        ],
    },
    install_requires = [
        # Nothing, this is just a learning project
    ],
    long_description = description,
    long_description_content_type = "text/markdown",
)