from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="wrapper-mysql-connector",
    version="0.0.2",
    license="MIT License",
    author="Renan de Souza Rodrigues",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="renanrodrigues7110@gmail.com",
    keywords=[
        "mysql",
        "mysql-connector",
        "wrapper",
        "wrapper-mysql",
        "wrapper-mysql-connector",
    ],
    description="Wrapper não oficial do mysql-connector",
    packages=["wrapper_connector"],
    install_requires=["mysql-connector-python"],
)
