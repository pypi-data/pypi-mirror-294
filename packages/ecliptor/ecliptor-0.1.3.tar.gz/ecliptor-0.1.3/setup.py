from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ecliptor",
    version="0.1.3",
    author="Nanki Grewal",
    author_email="nanki@ecliptor.ai",
    description="Python SDK for the Ecliptor API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ecliptor/ecliptor-python-sdk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "flake8>=3.9.0"],
    },
)