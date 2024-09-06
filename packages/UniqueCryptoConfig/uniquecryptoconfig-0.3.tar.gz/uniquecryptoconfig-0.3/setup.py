from setuptools import setup, find_packages

setup(
    name='UniqueCryptoConfig',
    version='0.3',  # Start with version 0.1
    packages=find_packages(),
    description='A unique package for crypto configurations',
    author='Terry Li',
    author_email='terry@eonlabs.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)