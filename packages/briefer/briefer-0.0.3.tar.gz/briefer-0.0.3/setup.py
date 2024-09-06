from setuptools import setup, find_packages

setup(
    name="briefer",
    version="0.0.3",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "briefer=briefer.__main__:main",
        ],
    },
    classifiers=[
        # TODO
    ],
    python_requires='>=3.9',
)
