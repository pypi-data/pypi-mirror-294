from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mem0rylol',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-groq",
        "langchain-openai",
        "pymilvus",
        "neo4j",
        "python-dotenv",
        "pydantic",
        "loguru",
        "asyncio"
    ],
    description='A specialized memory layer for building long-term memory solutions for agentic AI apps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/oracle-ai-companion/memorylayer',
    author='anthoeknee',
    author_email='pacyheb@protonmail.com',
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.7',
)