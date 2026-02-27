from setuptools import setup, find_packages

setup(
    name="audio-renamer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mutagen>=1.45.0",
        "PyYAML>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "audio-renamer=audio_renamer.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool to rename audio files with duration information",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audio-renamer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)