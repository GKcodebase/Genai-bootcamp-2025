from setuptools import setup, find_packages

setup(
    name="agentic_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'groq==0.4.2',
        'python-dotenv==1.0.1',
        'duckduckgo-search==5.1.0',
        'wikipedia==1.4.0',
        'requests==2.31.0',
        'python-dateutil==2.9.0',
    ],
) 