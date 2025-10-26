from setuptools import setup, find_packages

setup(
    name="fantasy-goat",
    version="0.1.0",
    description="Fantasy basketball stat tracker and analysis tool",
    author="Fantasy GOAT Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
        "pydantic>=2.0.0",
        "click>=8.1.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "fantasy-goat=fantasy_goat.cli:main",
        ],
    },
)
