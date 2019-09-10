from setuptools import setup, find_packages

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="LUNCHSCRAPER", 
    version="1.5.0",
    description="Fetches and email daily menus for restaurants",
    author="Vojtech Kotek",
    author_email="vojtech@kotek.co",
    url="https://web.kotek.co/lunch-scraper",
    install_requires=install_requires,
    packages=find_packages()
)
