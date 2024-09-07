from setuptools import setup, find_packages

setup(
    name="cloey",  # New package name
    version="0.1.0",
    description="Cloey is a simple framework to create USSD applications using FastAPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jose Machava",
    author_email="jose.s.machava@gmail.com",
    url="https://github.com/josesmachava/cloey",  # Update this link
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)