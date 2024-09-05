import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="aicacia-document-exporter",
    version="0.1.3",
    description="Aicacia document exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="collaborative-earth",
    author_email="team@collaborative.earth",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "src"},
    python_requires=">=3.8, <4",
    install_requires=[
        "tzlocal>=5.2"
    ],
    extras_require={
        "test": [
            "simhash>=2.1.2",
            "langchain-huggingface>=0.0.3"
        ],
    },
    project_urls={
        "Website": "https://www.collaborative.earth/"
    }
)