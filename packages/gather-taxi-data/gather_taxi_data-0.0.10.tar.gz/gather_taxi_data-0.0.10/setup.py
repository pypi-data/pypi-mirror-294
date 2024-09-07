from setuptools import setup, find_packages

setup(
    name="gather_taxi_data",  # Replace with your package name
    version="0.0.10",  # Replace with your package version
    author="Wayne Bennett",
    author_email="wayne.bennett@live.com",
    description="Export data from web portals and save to database.",
    long_description=open("README.md").read(),  # Make sure you have a README.md file
    long_description_content_type="text/markdown",  # If you use Markdown for README
    url="https://github.com/WayneBennett666/gather-taxi-data",  # Replace with your project URL
    packages=find_packages(where="src"),  # Exclude 'tests' package  , exclude=["tests", "tests.*"]
    package_dir={"": "src"},  # Root ('') of the packages is under 'src'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Replace with the minimum Python version required
    install_requires=[
        "taxi_data_core",
        "selenium",
        "pydantic",
        "beautifulsoup4"
        # "google-auth",
        # "google-auth-oauthlib",
        # "google-api-python-client",
        # "xero-python"
        # Add more dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "gather-taxi-data=gather_taxi_data.gather_all_data:main",  # Replace with your CLI commands if needed
        ],
    },
)