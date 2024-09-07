from setuptools import setup

setup(
    name="WebScrapingTool",
    version="1.1",
    description="A toolkit to install essential web scraping libraries with one command.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohit180497/WebScrapingTool",
    author="Rohit Kosamkar",
    author_email="rohitkosamkar97@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    install_requires=[
    'pandas',
    'numpy',
    'webdriver_manager',
    'beautifulsoup4',  # HTML and XML parsing
    'scrapy',  # Web scraping framework
    'requests',  # HTTP requests for accessing web pages
    'lxml',  # Parsing HTML and XML
    'parsel',  # Scrapy's data extraction library
    'httpx',  # HTTP client with async support
    'fake-useragent',  # Simulating different browsers
    'cchardet',  # Encoding detection for faster parsing
    'aiohttp',  # Asynchronous HTTP client
    'pyppeteer',  # Headless browser automation (similar to Puppeteer)
    'selenium',  # Web browser automation for dynamic pages,
    'tqdm'

],
)