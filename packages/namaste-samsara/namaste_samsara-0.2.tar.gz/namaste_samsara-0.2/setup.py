from setuptools import setup, find_packages

setup(
    name = "namaste_samsara",
    version = "0.2",
    packages = find_packages(),
    entry_points = {
        "console_scripts" : [
            "namaste-samsara = namaste_samsara:hello"
        ],
    },
    install_requires = [
        # Nothing, this is just a learning project
    ],
)