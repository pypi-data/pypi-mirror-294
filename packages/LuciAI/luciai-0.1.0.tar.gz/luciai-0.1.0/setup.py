from setuptools import setup, find_packages

with open("readme.mD", "r") as fh:
    long_description = fh.read()

setup(
    name="LuciAI",
    version="0.1.0",
    description='The First AI-Based Medical Agent Designed to Automate All Medical Processes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "cerina",
        "openai",
        "together",
        "langchain-together",
        "langchain-core",
        "langchain-community",
        "ijson",
        "pydantic",
    ],
    author="wbavishek",
    author_email="wbavishek@gmail.com",  # Replace with the actual support email
    url="https://revmaxx.co",  # Replace with the actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  
    package_data={
       'logo': ['*.png'],  
    },
)
