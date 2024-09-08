from setuptools import setup, find_packages

setup(
    name="km_nlp",  # Your package name
    version="0.2",  # Updated version number
    author="Krishna Mishra",
    author_email="admin@krishna.com",
    description="A Python library for basic Nepali text preprocessing.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/krishnamishra8848",  # Link to your project (GitHub, etc.)
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
