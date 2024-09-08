from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CodeConsolidator",
    version="0.1.0",
    author="Kamil Stanuch",
    description="Consolidates and analyzes codebases for insights.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamilstanuch/CodeConsolidator",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="code analysis, codebase, consolidation, visualization",
    install_requires=[
        "tiktoken",
        "colorama",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "codeconsolidator=CodeConsolidator.app:main",
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        "CodeConsolidator": ["*.md"],
    },
)