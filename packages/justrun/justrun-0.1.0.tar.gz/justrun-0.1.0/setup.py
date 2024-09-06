import setuptools


setuptools.setup(
    name="justrun",
    version="0.1.0",
    author="buggist",
    author_email="316114933@qq.com",
    description="The simplest way to enable multiple python environment work togather. ",
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Buggist/Just-Run",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
