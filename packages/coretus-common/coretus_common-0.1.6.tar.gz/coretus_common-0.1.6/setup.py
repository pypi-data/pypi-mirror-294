from setuptools import setup, find_packages

setup(
    name="coretus-common",
    version="0.1.6",
    description="Centralized error handling package for FastAPI applications.",
    author="sandeep",
    author_email="sandeep@coretus.com",
    url="https://github.com/coretus-technologies/python-common.git",
    packages=find_packages(where="src/coretus_common"),
    package_dir={"": "src/coretus_common"},
    install_requires=[
        "fastapi>=0.112.2",
    ],
    extras_require={  # Optional dependencies go here
        "mongo": ["pymongo>=4.8.0"],
        "jwt": ["PyJWT>=2.9.0"],
        "test": ["pytest>=8.3.2",
        "pytest-asyncio>=0.24.0",
        "pytest-tornasync>=0.6.0.post2",
        "pytest-trio>=0.8.0",
        "pytest-twisted>=1.14.2",  "anyio>=4.4.0", "uvicorn>=0.30.6"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
)
