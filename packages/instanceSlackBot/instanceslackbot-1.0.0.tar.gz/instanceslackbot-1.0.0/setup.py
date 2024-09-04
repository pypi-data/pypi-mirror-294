from setuptools import setup, find_packages

NAME = "instanceSlackBot"
AUTHOR = "Daichi Matsumoto"
AUTHOR_EMAIL = "s1f102200828@iniad.org"
URL = "https://github.com/Dai-H15/InstanceSlackBot"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/Dai-H15/InstanceSlackBot"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.10"
INSTALL_REQUIRES = [
    "slack_sdk >=3.31.0",
]
with open("README.md", "r") as fh:
    ld = fh.read()

PACKAGES = find_packages()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    long_description=ld,
    long_description_content_type="text/markdown",
)