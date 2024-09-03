from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name="sam-test-cobo-cli",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "cobo=sam_test_cobo_cli.commands:cli",
        ],
    },
)
