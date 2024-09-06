from setuptools import setup, find_packages

setup(
    name="briefer",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "briefer=briefer.__main__:main",  # Create a command-line entry point
        ],
    },
    classifiers=[
        # TODO
    ],
    python_requires='>=3.9',  # Specify Python version support
)
