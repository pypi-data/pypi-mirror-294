from setuptools import setup, find_packages

setup(
    name="log_abstractor",
    version="1.1.6",
    packages=find_packages(),
    install_requires=[
        "structlog>=24.4.0", "piidata>=1.0.0",#"scrubadub==2.0.0","regex",
        "re",
    ],
    description="Optimized anonymizer with pre-scrubbing.",
    author="Dipanjan Mazumder",
    author_email="javahub@yahoo.com",
    url="https://github.com/SMART2016/logger",  # Optional: Link to your project repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
