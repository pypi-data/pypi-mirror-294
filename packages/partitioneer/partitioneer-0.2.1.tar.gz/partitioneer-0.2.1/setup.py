from setuptools import setup, find_packages

setup(
    name='partitioneer',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pyarrow'
    ],
    # author='Your Name',
    # author_email='your.email@example.com',
    description='A library for reading and writing partitioned data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lachlancahill/partitioneer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)