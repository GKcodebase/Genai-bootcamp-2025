from setuptools import setup, find_packages

setup(
    name="mcp-integration",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "groq==0.27.0",
        "python-dotenv==1.0.1",
        "pydantic==2.6.3",
        "typing-extensions>=4.10.0",
        "pytest==7.4.3",
        "requests==2.31.0",
        "aiohttp==3.9.3",
        "tenacity==8.2.3",
    ],
    python_requires=">=3.9",
) 