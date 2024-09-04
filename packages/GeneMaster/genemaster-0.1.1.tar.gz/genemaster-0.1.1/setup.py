from setuptools import setup, find_packages

setup(
    name="GeneMaster",
    version="0.1.1",
    author="Ahmed Osama Taha",
    author_email="ahmedosamaofficial13@gmail.com",  # Replace with your email
    description="A comprehensive package for DNA, RNA, and protein sequence analysis and visualization.",
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhmedOs13/GeneMaster",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
    ],
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    }
)
