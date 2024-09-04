from setuptools import setup, find_packages

setup(
    name="file-content-extractor",
    version="0.3.6",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fce=src.main:main', 
        ],
    },
    install_requires=['anytree'],
    author="Daniel",
    author_email="daniel@udit.one",
    description="A tool to extract content from text files in a directory, with options to ignore certain files and directories.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/joonheeu/file-content-extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
