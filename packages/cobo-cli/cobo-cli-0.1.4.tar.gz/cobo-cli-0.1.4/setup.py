from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name="cobo-cli",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "cobo=cobo_cli.commands:cli",
        ],
    },
)
