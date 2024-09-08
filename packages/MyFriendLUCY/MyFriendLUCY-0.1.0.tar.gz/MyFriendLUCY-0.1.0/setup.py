from setuptools import setup, find_packages

setup(
    name="MyFriendLUCY",
    version="0.1.0",                  # Package version
    author="Your Name",
    author_email="isaiahjpeterson007@gmail.com",
    description="Ethereum Price Prediction Package for Short-Term Trading",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LUCY-1986-2009-project-ethereum-market-prediction-unit-limit_uncertainty,control_yourself--OurFriendLucy",  # GitHub link or project link
    packages=find_packages(),         # Automatically find and include all packages
    include_package_data=True,        # Include other files specified in MANIFEST.in
    install_requires=[
        "tensorflow>=2.0",
        "pandas",
        "ccxt",
        "pandas-ta",
        "numpy",
        "joblib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',          # Minimum Python version required
)
