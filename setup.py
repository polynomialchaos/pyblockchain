from setuptools import setup

setup(
    name='pyblockchain',
    version='1.0',
    description='A simple python package for blockchain development.',
    author='Florian',
    author_email='polynomialchaos@gmail.com',
    packages=['pyblockchain'],
    entry_points={
        "console_scripts": [
            'pyBlockchain=pyblockchain.bin.pyBlockchain:main',
        ]
    }
)