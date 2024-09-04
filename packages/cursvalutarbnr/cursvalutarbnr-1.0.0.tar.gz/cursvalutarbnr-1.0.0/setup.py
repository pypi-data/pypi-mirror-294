from setuptools import setup, find_packages

# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload * -u __token__ -p pypi-token

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as r:
    install_requires = r.readlines()


setup(
    name="cursvalutarbnr",
    version="1.0.0",
    description="Afla cursul valutar in RON de la BNR.",
    url="https://github.com/ClimenteA/curs-valutar-bnr",
    author="Climente Alin",
    author_email="climente.alin@gmail.com",
    license="MIT",
    py_modules=["cursvalutarbnr"],
    install_requires=install_requires,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
)