from setuptools import setup, find_packages

setup(
    name='GeneMaster',
    version='1.0.1',
    packages=find_packages(),
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
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)