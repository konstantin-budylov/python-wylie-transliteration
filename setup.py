"""
Setup configuration for Wylie Transliterator package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="wylie-transliterator",
    version="2.0.0",
    author="Python DDD Refactoring",
    description="Extended Wylie Transliteration for Tibetan Unicode (Domain-Driven Design)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wylie-transliterator",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Religion",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "mypy>=1.0",
            "pylint>=2.17",
        ],
    },
    entry_points={
        "console_scripts": [
            "wylie=wylie_transliterator.cli:main_interactive",
            "wylie-convert=wylie_transliterator.cli:main_file_processor",
        ],
    },
    keywords="tibetan wylie transliteration unicode ewts buddhism linguistics",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/wylie-transliterator/issues",
        "Documentation": "https://github.com/yourusername/wylie-transliterator/blob/main/README.md",
        "Source": "https://github.com/yourusername/wylie-transliterator",
    },
)

