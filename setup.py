from setuptools import setup, find_packages


NAME = "blackmaria"
DESCRIPTION = "Scraping webpages with natural language"
URL = "https://github.com/smyja/blackmaria"
EMAIL = "akpobimaro@gmail.com"
AUTHOR = "Maro Akpobi"
with open("README.md", "r") as fh:
    description = fh.read()
setup(
    name=NAME,
    version='0.1.2',
    packages=find_packages(),
    url= URL,
    license='MIT',
    author=AUTHOR,
    author_email=EMAIL,
    long_description=description,
    long_description_content_type="text/markdown",
    install_requires=[
        'bs4',
        'python-dotenv',
        "guardrails-ai==0.1.4",
        "gpt-index==0.4.39"
    ],
    
)
