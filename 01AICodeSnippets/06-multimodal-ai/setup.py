from setuptools import setup, find_packages

setup(
    name="multimodal-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
        "python-dotenv>=0.19.0",
        "pydantic>=1.8.2",
        "google-generativeai>=0.3.0",
        "Pillow>=9.0.0",
        "openai-whisper>=20231117",
        "torch>=2.0.0",
        "numpy>=1.21.0",
        "python-jose>=3.3.0",
        "requests>=2.26.0",
    ],
    python_requires=">=3.9",
) 