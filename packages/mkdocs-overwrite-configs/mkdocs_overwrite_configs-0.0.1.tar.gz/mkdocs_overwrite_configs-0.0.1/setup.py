import io

from setuptools import find_packages, setup

setup(
    name="mkdocs-overwrite-configs",
    version="0.0.1",
    description="Overwrite MkDocs configuration files with a single file",
    long_description=io.open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords="mkdocs backstage techdocs mkdocs-overwrite-configs",
    url="https://github.com/carneirofc/mkdocs-overwrite-configs",
    author="carneirofc",
    author_email="claudiofcarneiro@hotmail.com",
    license="MIT",
    python_requires=">=3.6",
    install_requires=["mkdocs>=1.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "mkdocs.plugins": [
            "overwrite-configs = mkdocs_overwrite_configs.plugin:OverwriteConfigsPlugin"
        ]
    },
)
