from setuptools import setup, find_packages

setup(
    name='bsedebtmarket',
    version='0.1.0',
    description='A library to scrape BSE Debt Market and convert them to JSON.',
    author='Sagar Chand Agarwla',
    author_email='sagar.agarwal@beyondirr.tech',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'bsedebtmarket=bsedebtmarket.parser:table_to_json',
        ],
    },
)
