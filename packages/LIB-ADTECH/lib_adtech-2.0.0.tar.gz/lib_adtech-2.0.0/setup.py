from setuptools import setup, find_packages

setup(
    name="LIB_ADTECH",
    version="2.0.0",
    packages=find_packages(),
    description="Melhorias para automação web.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Alan Ribeiro",
    author_email="desenvolvimento@adpromotora.com.br",
    url="https://github.com/Pnda0/Adlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)