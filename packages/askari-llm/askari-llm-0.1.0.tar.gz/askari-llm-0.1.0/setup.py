from setuptools import setup, find_packages

setup(
    name="askari-llm",
    version="0.1.0",
    description="A package to create AI guardrails for LLM applications using YAML-defined policies.",
    author="mgasa",
    author_email="mgasa.loucat1@gmail.com",
    packages=find_packages(),
    include_package_data=True,  # Ensures policies.yaml is included
    package_data={
        '': ['*.yaml'],  # Includes all .yaml files in the package
    },
    install_requires=[
        "pyyaml",  # Add any other dependencies here
    ],
)
