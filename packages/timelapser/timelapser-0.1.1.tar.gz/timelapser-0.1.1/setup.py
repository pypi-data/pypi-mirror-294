from setuptools import setup, find_packages

setup(
    name="timelapser",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "typer",
        "numpy",
        "opencv-python-headless",
        "mss",
        "pynput",
        "rich",
    ],
    entry_points={"console_scripts": ["timelapser=timelapser.main:app"]},
    author="Asib Hossen",
    author_email="dev.asib@proton.me",
    description="Record and save time-lapse videos while you work.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/asibhossen897/TimeLapser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
