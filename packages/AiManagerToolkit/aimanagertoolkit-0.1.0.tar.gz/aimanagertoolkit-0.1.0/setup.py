from setuptools import setup, find_packages

setup(
    name="AiManagerToolkit",
    version="0.1.0",
    author="Gustavo Inostroza",
    author_email="gusinostrozar@gmail.com",
    description="A toolkit for working with OpenAI and Azure OpenAI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Inostroza-Wingsoft/AiManagerToolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "openai",
        "pydantic",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'aimanagertoolkit=AiManagerToolkit:main',
        ],
    },
)