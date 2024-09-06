from setuptools import setup, find_packages

setup(
    name='UniqueCryptoConfig',
    version='0.4',  # Incremented version number
    packages=find_packages(include=['CryptoConfig', 'CryptoConfig.*']),
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