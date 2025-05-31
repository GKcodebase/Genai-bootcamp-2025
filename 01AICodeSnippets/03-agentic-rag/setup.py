from setuptools import setup, find_packages

setup(
    name="agentic-rag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.1",
        "langchain-core>=0.1.0",
        "langchain-groq>=0.0.1",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "pdfminer.six>=20221105",
        "python-dotenv>=1.0.0",
        "unstructured>=0.10.0",
        "markdown>=3.4.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Agentic RAG system combining document retrieval with autonomous agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
) 