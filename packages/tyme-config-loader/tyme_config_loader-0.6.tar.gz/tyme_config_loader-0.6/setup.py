from setuptools import setup, find_packages
setup(
    name="tyme_config_loader",  # The name of your library
    version="0.6",
    description="A simple Python library",
    author="Bao Tran",
    author_email="bao.tr0401@gmail.com",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=["pyyaml"]
)