from setuptools import setup, find_packages

setup(
    name="weather_analysis_thomashansen",
    version="0.1.0",
    packages=find_packages(),
    description="A package for loading and analyzing weather data using CSV and Pandas.",
    author="Thomas Hansen",
    author_email="rotes-screen-0o@icloud.com",
    url="http://example.com",  # Placeholder valid URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "csv"
    ],
)