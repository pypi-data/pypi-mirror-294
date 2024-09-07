from setuptools import setup, find_packages

setup(
    name='bvlogger',
    version='1.0.0',
    description='A Python SDK for logging of connector and endpoint management',
    author='Obaid ur Rehman',
    author_email='obaid_mailbox@yahoo.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)