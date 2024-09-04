from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="O_money",
    version="0.0.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "O_money=O_money.o_webpay:main",
        ],
    },
    author="Ibrahim Bilaly DICKO",
    author_email="dicko.dev@gmail.com",
    description="This Package is created with the aim of facilitating the integration of web payment by orange money into python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddicko/O_money",
    licence="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
