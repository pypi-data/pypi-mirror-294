from setuptools import setup, find_packages

setup(
    name='GeneMaster',
    version='0.1.4',
    packages=find_packages(include=['GeneMaster', 'GeneMaster.*']),
    install_requires=[
        'numpy',
    ],
    description='A comprehensive package for DNA, RNA, and protein sequence analysis and visualization.',
    author='Ahmed Osama Taha',
    author_email='ahmedosamaofficial13@gmail.com',
    url='https://github.com/AhmedOs13/GeneMaster',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)