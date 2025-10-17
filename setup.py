#!/usr/bin/env python3
"""
Setup script para el Sistema Mozo Virtual
Proyecto Final Integrador - CACIC 2025
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sistema-mozo-virtual",
    version="1.0.0",
    author="Rizzo",
    author_email="rizzo@example.com",
    description="Sistema multi-agente para asistencia en restaurantes con IA generativa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rizzofs/Cacic2025_Tp-final.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mozo-virtual=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
    },
    keywords="ai, agents, langchain, multi-agent, restaurant, chatbot, rag, notion, langsmith",
    project_urls={
        "Bug Reports": "https://github.com/rizzofs/Cacic2025_Tp-final/issues",
        "Source": "https://github.com/rizzofs/Cacic2025_Tp-final.git",
        "Documentation": "https://github.com/rizzofs/Cacic2025_Tp-final#readme",
        "LangSmith": "https://smith.langchain.com/projects/proyecto-final-agentes",
        "Notion": "https://notion.so/28815eefe92680389583cff88068af9e",
    },
)
