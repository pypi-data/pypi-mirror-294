from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="isozero",
    version="0.1.0",
    author="Jazmia Henry",
    author_email="jazmiahenry@example.com",
    description="Enhance LLM Zero-Shot Responses through multi-step reasoning and document analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iso-ai/isozero",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "anthropic",  
        "openai",     
        "transformers", 
        "torch",     
        "numpy",      
        "pandas",     
        "tqdm",       
        "requests",   
        "beautifulsoup4", 
        "python-dotenv", 
        "scikit-learn",
        "matplotlib",  
        "jsonschema", 
    ],
    entry_points={
        "console_scripts": [
            "isozero=isozero.cli:main",
        ],
    },
)