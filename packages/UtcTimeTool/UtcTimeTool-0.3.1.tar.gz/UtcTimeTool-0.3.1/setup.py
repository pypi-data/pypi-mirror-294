from setuptools import setup, find_packages

setup(
    name="UtcTimeTool",
    version="0.3.1",
    author="PC BAZ",
    author_email="pc.baz1617@gmail.com",
    description="A tool to retrieve UTC timezones by country.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/UtcTimeTool",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
