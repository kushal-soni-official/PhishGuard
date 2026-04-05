from setuptools import setup, find_packages

setup(
    name="phishguard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-SocketIO",
        "Flask-Cors",
        "scikit-learn",
        "pandas",
        "numpy",
        "nltk",
        "joblib",
        "requests",
        "beautifulsoup4",
        "email-validator",
        "dnspython",
        "pytest",
    ],
)
